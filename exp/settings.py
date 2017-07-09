import random
import numpy as np
import pandas as pd

Kwadrat = np.array([
[0, 3, 2, 1],
[1, 0, 3, 2],
[2, 1, 0, 3],
[3, 2, 1, 0]
])

exp = dict()
exp['kwadrat'] = Kwadrat
exp['buttons'] = ['l', 'd']
exp['block trials'] = 72 # actually, jest 48 przy obecnym prop
exp['proportions'] = [(9, 3), (3, 9)] # can change


# experimental basic defs:
def shuffle_colors(stim):
	Kolory = list()
	for color in ['red', 'green', 'yellow', 'blue']:
		Kolory.append(stim['circle'][color])

	# Randomize array Kolory:
	random.shuffle(Kolory)
	return Kolory


def get_colors_from_square(colors, N, exp=exp):
	names = ['lc', 'li', 'rc', 'ri']
	return {cnd: colors[exp['kwadrat'][N, i]]
			for i, cnd in enumerate(names)}


def shuffle_rows(df):
	df = df.reset_index(drop=True)
	ind = list(range(len(df)))
	random.shuffle(ind)
	df = df.loc[ind, :]
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df


def get_block(blockNum, prop=0, exp=exp):
	'''What does it do? Seems it creates block, not just gets it'''

	columns=['block', 'cond', 'choiceType', 'fixTime', 'prime', 'target',
		'effect', 'pos', 'corrResp', 'resp', 'ifcorr']
	dtp = ['int32', 'category', 'category', 'int32', 'category', 'category',
		'object', 'float64', 'object', 'object', 'bool']

	template = pd.read_excel('block_list.xls')
	temp_cols = [c for c in columns if c in template.columns]
	template = template.loc[:, temp_cols]

	# content
	# what is prop? - proportion of trials of given type?
	# CHANGE prop to specific
	prop = random.choice(exp['proportions'])
	df = pd.concat([template.query('choiceType == "Cued"')] * prop[0] +
		[template.query('choiceType == "Free"')] * prop[1])
	df = shuffle_rows(df)

	# add missing rows - what kind of missing rows?
	temp_cols = [c for c in columns if c not in template.columns]
	for c in temp_cols:
		df[c] = 0
	df['block'] = blockNum

	for col, tp in zip(columns, dtp):
		df[col] = df[col].astype(tp)

	return df
