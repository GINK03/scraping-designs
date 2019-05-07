import pandas as pd
import sys
import seaborn as sns
from matplotlib import pyplot
import pandas as pd
from pathlib import Path
if '--init' in sys.argv:
    df = None
    for path in sorted(Path('./tmp').glob('ameblo_*.csv')):
        if df is None:
            df = pd.read_csv(path)
        else:
            df = df.append(pd.read_csv(path))
        print(path)
        print(len(df))
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df.drop(['sha256'], axis=1, inplace=True)
    print(df.head())
    df.to_pickle('ameblo.pkl')
    exit()

df = pd.read_pickle('ameblo.pkl')
df['time'] = df['time'].dt.tz_localize(None)
df = df[pd.notna(df['time'])]
df['year_month'] = df['time'].apply(lambda x:f'{int(x.year):04d}_{int(x.month):02d}')
df['total_sample'] = 1
for tar in ['マッチングアプリ', 'プログラミング', '勉強', 'tiktok', 'metoo', 'インスタ映え', '忖度', '婚活', 'line', '2ch', 'galaxy', '消費税', 'アラサー', 'アラフォー', 'android', '原発', 'iphone', '韓国', 'k-pop', 'インスタグラム', 'facebook', 'twitter']:
    flags = []
    for body in df['body']:
        #flags.append('台湾' in str(body) and '旅行' in str(body))
        flags.append(str(body).lower().count(tar))
    df['tar'] = flags
    dfMin = df[['year_month', 'tar', 'total_sample']].groupby('year_month').sum().reset_index()
    dfMin = dfMin[dfMin['year_month'] >= '2009-01']
    print(tar)
    print(dfMin.sort_values(by=['year_month'], ascending=False).head(20),)
    dfMin['tar_r'] = dfMin['tar']/dfMin['total_sample']
    pyplot.figure(figsize=(30, 30))
    ax = sns.barplot(x="year_month", y="tar_r", data=dfMin)
    sns.set(font_scale=1.5)
    ax.margins(0.00, 0.00)
    ax.set(xlabel='year_month', ylabel=f'{tar}')
    ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
    ax.figure.savefig(f'pngs/{tar}.png')

