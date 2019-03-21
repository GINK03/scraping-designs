import MeCab
import pandas as pd


df = pd.read_csv('./lexical_parsed.csv')


m = MeCab.Tagger('-Owakati')
m.parse("")
feat_freq = {}
for obj in df.to_dict('record'):
    # print(obj)
    com = obj['shuunou']
    try:
        for feat in set(m.parse(com).strip().split()):
            if feat_freq.get(feat) is None:
                feat_freq[feat] = 0
            feat_freq[feat] += 1
    except:
        ...
for feat, freq in sorted(feat_freq.items(), key=lambda x: x[1]):
    print(feat, freq)


('communication', 'インターネット接続,BS,CATV,地上デジタル,無料,光ファイバー')
('kitchen', '別,ガスコンロ,洗面化粧台,衛生的,温水洗浄便座')
('other', 'エアコン,フローリング,バルコニー,置き場,ベランダ')
('secure', 'モニター,フォン,オートロック,インターホン,宅配ボックス')
