import re
import pandas as pd
import sys
import seaborn as sns
from matplotlib import pyplot
import pandas as pd
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor as PPE

TL = ['fgo', 'ffrk',  'グラブル', 'ワクチン', 'pairs', 'with', 'omiai', 'ゼクシィ']
TL += ['ワープア', '非正規', '派遣切り', '派遣']
TL += ['タピオカ']
TL += ['壁ドン']
TL += ['ユーチューバ']
TL += ['ガン', '闘病', 'うつ病']
TL += ['育児', '保育園', '幼稚園', '合格', '当選', '結婚', '出産']
TL += ['妖怪ウォッチ', '危険ドラッグ', 'マッチングアプリ', 'プログラミング', '勉強', 'tiktok', 'metoo', 'インスタ映え',
       '忖度', '婚活', 'line', '2ch', 'galaxy', '消費税', 'アラサー', 'アラフォー', 'android', '原発']
TL += ['iphone', '韓国', 'k-pop', 'インスタグラム', 'facebook', 'twitter']
TL += ['激おこぷんぷん丸', 'バカッター', 'ブラック企業']


def pmap_content(arg):
    idx, typeof, path = arg
    print(path)
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df.drop(['sha256'], axis=1, inplace=True)
    df['time'] = df['time'].dt.tz_localize(None)
    df = df[pd.notna(df['time'])]
    df['year_month'] = df['time'].apply(
        lambda x: f'{int(x.year):04d}_{int(x.month):02d}')
    df['user'] = df['canonical'].apply(lambda x: x.split('/')[-2])
    df['total_sample'] = 1
    for tar in TL:
        flags = []
        for body in df['body']:
            #flags.append('台湾' in str(body) and '旅行' in str(body))
            flags.append(str(body).lower().count(tar))
        df[f'tar_{tar}'] = flags
    df.drop(['title', 'body'], axis=1, inplace=True)
    df.to_pickle(f'tmp/{typeof}_{idx:04d}.pkl')


def pmap_profile(arg):
    idx, typeof, path = arg
    print(path)
    df = pd.read_csv(path)
    df.to_pickle(f'tmp/{typeof}_{idx:04d}.pkl')


if '--init' in sys.argv:
    args = [(idx, 'profile', path) for idx, path in enumerate(
        sorted(Path('./tmp').glob('ameblo_jsons_profile_*.csv')))]
    with PPE(max_workers=8) as exe:
        exe.map(pmap_profile, args)

    args = [(idx, 'content', path) for idx, path in enumerate(
        sorted(Path('./tmp').glob('ameblo_jsons_content_*.csv')))]
    with PPE(max_workers=8) as exe:
        exe.map(pmap_content, args)

if '--join' in sys.argv:
    dfProfile = [pd.read_pickle(path)
                 for path in Path('./tmp').glob('profile_*.pkl')]
    dfProfile = pd.concat(dfProfile, axis=0)

    dfContent = [pd.read_pickle(path)
                 for path in Path('./tmp').glob('content_*.pkl')]
    dfContent = pd.concat(dfContent, axis=0)

    df = dfContent.join(dfProfile.set_index('user'), on='user')
    df.drop_duplicates(subset="canonical", keep=False, inplace=True)
    #df.to_csv('tmp/ameblo_user.csv', index=None)
if '--agg' in sys.argv:

    def calc_age(r):
        year = int(r['year_month'].split('_')[0])
        bday = r['生年月日']
        if pd.isna(bday) :
            return None
        else:
            #print(bday)
            rage = year - int(re.search(r'(\d\d\d\d)', bday).group(1))
            return rage
    dfProfile = [pd.read_pickle(path)
                 for path in Path('./tmp').glob('profile_*.pkl')]
    dfProfile = pd.concat(dfProfile, axis=0)

    dfContent = [pd.read_pickle(path)
                 for path in Path('./tmp').glob('content_*.pkl')]
    dfContent = pd.concat(dfContent, axis=0)
    print('laod dataset')
    df = dfContent.join(dfProfile.set_index('user'), on='user')
    df.drop_duplicates(subset="canonical", keep=False, inplace=True)
    print('joined dataset')

    df['tar_age'] = df.apply(calc_age, axis=1)
    print('made age')
    #df = df[pd.notnull(df['性別'])]
    #df = df[df['性別'].apply(lambda x:x in ['男性', '女性'])]
    #df['tar_女性'] = df['性別'].apply(lambda x:1 if x=='女性' else 0)
    ''' 
    for tar in TL:
        dfMin = df[['year_month', '性別',f'tar_{tar}', 'total_sample']].groupby(by=['性別', 'year_month']).sum().reset_index()
        dfMin = dfMin[dfMin['year_month'] >= '2016-01']
        print(tar)
        print(dfMin.sort_values(by=['year_month'], ascending=False).head(20),)
        dfMin[f'tar_{tar}_r'] = dfMin[f'tar_{tar}']/dfMin['total_sample']
        pyplot.figure(figsize=(30, 30))
        ax = sns.barplot(x="year_month", y=f"tar_{tar}_r",hue='性別', data=dfMin)
        sns.set(font_scale=1.5)
        ax.margins(0.00, 0.00)
        #ax.set(xlabel='year_month', ylabel=f'{tar}')
        ax.set_title(f'{tar}', fontsize=50)
        ax.set_xlabel("year_month",fontsize=40)
        ax.set_ylabel(f'{tar}_freq', fontsize=40)
        ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
        ax.figure.savefig(f'pngs/g'ender_{tar}.png')
    '''
    for tar in TL + ['age']:
        if tar in ['age']:
            dfMin = df[pd.notnull(df['tar_age'])][['year_month', f'tar_{tar}', 'total_sample']].groupby(
                by=['year_month']).mean().reset_index()
        else:
            dfMin = df[['year_month', f'tar_{tar}', 'total_sample']].groupby(
                by=['year_month']).sum().reset_index()
        dfMin = dfMin[dfMin['year_month'] >= '2011-01']
        print(tar)
        print(dfMin.sort_values(by=['year_month'], ascending=False).head(20),)
        dfMin[f'tar_{tar}_r'] = dfMin[f'tar_{tar}']/dfMin['total_sample']
        pyplot.figure(figsize=(30, 30))
        ax = sns.barplot(x="year_month", y=f"tar_{tar}_r", data=dfMin)
        sns.set(font_scale=1.5)
        ax.margins(0.00, 0.00)
        #ax.set(xlabel='year_month', ylabel=f'{tar}')
        ax.set_title(f'{tar}', fontsize=50)
        ax.set_xlabel("year_month", fontsize=40)
        ax.set_ylabel(f'{tar}_freq', fontsize=40)
        ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
        ax.figure.savefig(f'pngs/{tar}.png')
