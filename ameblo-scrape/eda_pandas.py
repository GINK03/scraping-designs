import pandas as pd
import sys
import seaborn as sns
from matplotlib import pyplot
import pandas as pdo

if '--init' in sys.argv:
    df = pd.read_csv('./ameblo.csv')
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df.drop(['sha256'], axis=1, inplace=True)
    print(df.head())
    df.to_pickle('ameblo.pkl')

df = pd.read_pickle('ameblo.pkl')
df['time'] = df['time'].dt.tz_localize(None)
df['year_month'] = df['time'].apply(lambda x:f'{x.year:04d}_{x.month:02d}')
flags = []
for body in df['body']:
    #flags.append('台湾' in str(body) and '旅行' in str(body))
    flags.append('婚活' in str(body))
df['kankoku'] = pd.Series(flags).astype(int)
df['total_sample'] = 1
df = df[['year_month', 'kankoku', 'total_sample']].groupby('year_month').sum().reset_index()
df = df[df['year_month'] >= '2011-01']
print(df.sort_values(by=['year_month'], ascending=False).head(20),)
df['kankoku'] = df['kankoku']/df['total_sample']
pyplot.figure(figsize=(30, 30))
ax = sns.barplot(x="year_month", y="total_sample", data=df)
sns.set(font_scale=2)
ax.set(xlabel='year_month', ylabel='total_sample')
ax.set_xticklabels(labels=ax.get_xtickla