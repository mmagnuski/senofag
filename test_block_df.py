import numpy as np
import pandas as pd
from settings import exp 

columns=['cond', 'choiceType', 'fixTime', 'prime', 'target',
	'effect', 'pos', 'corrResp', 'resp', 'ifcorr']
dtp = ['category', 'category', 'int32', 'category', 'category',
	'category', 'float64', 'category', 'category', 'bool']
data = np.zeros((72, len(columns)))

template = pd.read_excel('block_list.xls')
temp_cols = [c for c in columns if c in template.columns]
template = template.loc[:, temp_cols]

df = pd.DataFrame(data=data, columns=columns, index=range(1,73))

# content



for col, tp in zip(columns, dtp):
	df[col] = df[col].astype(tp)

# df.loc[:, 'fixTime'] = df.loc[:, 'fixTime'].astype('int32')