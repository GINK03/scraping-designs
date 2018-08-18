
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error 
from math import sqrt

df = pd.read_csv('./source.csv')

y = np.log( df['_stars_'].values + 2)

y_mean = y.mean()
y_mean = [ y_mean for _ in y.tolist() ]


rms = sqrt( mean_squared_error(y_mean, y ))

print('LGB OOF RMSE: {}'.format(rms))
