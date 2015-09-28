import stim
import numpy as np
import pandas as pd

df = pd.DataFrame(data=np.array([50, 'pleft', 'tright', 'green']).reshape(1,4),
	columns=['fixTime', 'prime', 'target', 'effect'], index=[1])
df.loc[:, 'fixTime'] = df.loc[:, 'fixTime'].astype('int32')
print df
print df.dtypes
stim.show_trial(df, stim.stim, 1)
