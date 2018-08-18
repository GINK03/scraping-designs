
from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_squared_error
from math import sqrt
import lightgbm as lgb
from sklearn.cross_validation import KFold
import pandas as pd
import numpy as np

def get_oof(clf, x_train, y, x_test):
    NFOLDS=5
    SEED=71
    kf = KFold(len(x_train), n_folds=NFOLDS, shuffle=True, random_state=SEED)
    oof_train = np.zeros((len(x_train),))
    oof_test = np.zeros((len(x_test),))
    oof_test_skf = np.empty((NFOLDS, len(x_test)))
    lgbm_params =  {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': 'rmse',
        # 'max_depth': 15,
        'num_leaves': 30,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.75,
        'bagging_freq': 4,
        'learning_rate': 0.016*5,
        #'max_bin':1023,
        'verbose': 0
    }
    for i, (train_index, test_index) in enumerate(kf):
        print('\nFold {}'.format(i))
        x_tr = x_train.iloc[train_index]
        y_tr = y[train_index]
        y_te = y[test_index]
        x_te = x_train.iloc[test_index]
        lgtrain = lgb.Dataset(x_tr, y_tr, feature_name=x_train.columns.tolist())
        lgvalid = lgb.Dataset(x_te, y_te, feature_name=x_train.columns.tolist())
                    #categorical_feature = categorical)
        lgb_clf = lgb.train(
            lgbm_params,
            lgtrain,
            num_boost_round=20000,
            valid_sets=[lgtrain, lgvalid],
            valid_names=['train','valid'],
            early_stopping_rounds=50,
            verbose_eval=50
        )
        oof_train[test_index] = lgb_clf.predict(x_te)
        oof_test_skf[i, :]    = lgb_clf.predict(x_test)

    oof_test[:] = oof_test_skf.mean(axis=0)
    return oof_train, oof_test

df = pd.read_csv('source.csv')
trainy = df['_stars_'].values
trainX = df.drop(['_stars_'], axis=1)

testX = pd.read_csv('./target.csv')
oof_train, oof_test = get_oof(None, trainX, np.log(trainy+2.0), testX.drop(['_hashval_'], axis=1))

rms = sqrt(mean_squared_error( np.log(trainy+2.0), oof_train))
print('LGB OOF RMSE: {}'.format(rms))
print("Modeling Stage")

testX['preds'] = np.exp(np.concatenate([oof_test])) - 2

testX[['_hashval_', 'preds']].to_csv('preds.csv', index=False)

