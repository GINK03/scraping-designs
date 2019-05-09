import pandas as pd
import sys
import seaborn as sns
from matplotlib import pyplot
import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor as PPE

TL = ['fgo', 'ffrk',  'グラブル', 'ワクチン']
TL += ['育児', '保育園', '幼稚園', '合格', '当選', '結婚', '出産']
TL += ['妖怪ウォッチ', '危険ドラッグ', 'マッチングアプリ', 'プログラミング', '勉強', 'tiktok', 'metoo', 'インスタ映え', '忖度', '婚活', 'line', '2ch', 'galaxy', '消費税', 'アラサー', 'アラフォー', 'android', '原発']
TL += ['iphone', '韓国', 'k-pop', 'インスタグラム', 'facebook', 'twitter']
TL += ['激おこぷんぷん丸', 'バカッター', 'ブラック企業']
def pmap(arg):
    idx, path = arg
    print(path)
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df.drop(['sha256'], axis=1, inplace=True)
    df['time'] = df['time'].dt.tz_localize(None)
    df = df[pd.notna(df['time'])]
    df['year_month'] = df['time'].apply(lambda x:f'{int(x.year):04d}_{int(x.month):02d}')
    df['total_sample'] = 1
    for tar in TL: 
        flags = []
        for body in df['body']:
            #flags.append('台湾' in str(body) and '旅行' in str(body))
            flags.append(str(body).lower().count(tar))
        df[f'tar_{tar}'] = flags
    df.drop(['title', 'body'], axis=1, inplace=True)
    df.to_pickle(f'tmp/{idx:04d}.pkl')

if '--init' in sys.argv:
    args = [(idx, path) for idx, path in enumerate(sorted(Path('./tmp').glob('ameblo_*.csv')))]
    with PPE(max_workers=8) as exe:
        exe.map(pmap, args)
df = [pd.read_pickle(path) for path in Path('./tmp').glob('*.pkl')]
df = pd.concat(df, axis=0)
df.drop_duplicates(subset='canonical', inplace=True)

for tar in TL:
    dfMin = df[['year_month', f'tar_{tar}', 'total_sample']].groupby('year_month').sum().reset_index()
    dfMin = dfMin[dfMin['year_month'] >= '2009-01']
    print(tar)
    print(dfMin.sort_values(by=['year_month'], ascending=False).head(20),)
    dfMin[f'tar_{tar}_r'] = dfMin[f'tar_{tar}']/dfMin['total_sample']
    pyplot.figure(figsize=(30, 30))
    ax = sns.barplot(x="year_month", y=f"tar_{tar}_r", data=dfMin)
    sns.set(font_scale=1.5)
    ax.margins(0.00, 0.00)
    #ax.set(xlabel='year_month', ylabel=f'{tar}')
    ax.set_title(f'{tar}', fontsize=50)
    ax.set_xlabel("year_month",fontsize=40)
    ax.set_ylabel(f'{tar}_freq', fontsize=40)
    ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
    ax.figure.savefig(f'pngs/{tar}.png')
