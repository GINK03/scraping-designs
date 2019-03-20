import seaborn as sns
import pandas as pd
from matplotlib import pyplot
pyplot.figure(figsize=(15*3, 15))
sns.set(style="whitegrid")
# exit()
df = pd.read_csv('lexical_parsed.csv')
countries = set()
for country, subDf in df.groupby(by=['country']):
    if len(subDf) > 1000:
        print(country, subDf['yachin'].mean())
        countries.add(country)
df = df.sort_values(by=['country'])
df = df[df['country'].apply(lambda x:x in countries)]
ax = sns.violinplot(x="country", y='yachin', data=df)
pyplot.ylim(0, 20)
ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=90)
ax.figure.savefig('myfig.png')
