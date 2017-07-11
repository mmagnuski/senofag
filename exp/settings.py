# encoding: utf-8
import os
import random
import numpy as np
import pandas as pd


def create_settings():
	Kwadrat = np.array([[0, 3, 2, 1],
						[1, 0, 3, 2],
						[2, 1, 0, 3],
						[3, 2, 1, 0]])

	settings = dict()
	settings['kwadrat'] = Kwadrat
	settings['exp dir'] = os.path.dirname(__file__)
	settings['data dir'] = os.path.join(settings['exp dir'], 'data')

	# CHANGE:
	settings['buttons'] = ['l', 'd']
	settings['block trials'] = 72 # czy to jest w ogóle używane?
	settings['proportions'] = [(9, 3), (3, 9)]

	return settings


# experimental basic defs:
def shuffle_colors(stim):
	Kolory = list()
	for color in ['red', 'green', 'yellow', 'blue']:
		Kolory.append(stim['circle'][color])

	# Randomize array Kolory:
	random.shuffle(Kolory)
	return Kolory


def get_colors_from_square(colors, N, settings=None):
	names = ['lc', 'li', 'rc', 'ri']
	return {cnd: colors[settings['kwadrat'][N, i]]
			for i, cnd in enumerate(names)}


def shuffle_rows(df):
	df = df.reset_index(drop=True)
	ind = list(range(len(df)))
	random.shuffle(ind)
	df = df.loc[ind, :]
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df


def create_block(blockNum, settings=None):
	'''Creates block of trials.'''

	# define column names and dtypes
	columns=['block', 'cond', 'choiceType', 'fixTime', 'prime', 'target',
			 'effect', 'pos', 'corrResp', 'resp', 'ifcorr', 'RT', 'soa_rating', 'rating_RT']
	dtp = ['int32', 'category', 'category', 'int32', 'category', 'category',
		   'object', 'float64', 'object', 'object', 'bool', 'float64', 'int16', 'float64']

	# read template and select columns
	template = pd.read_excel('block_list.xls')
	temp_cols = [c for c in columns if c in template.columns]
	template = template.loc[:, temp_cols]

	# add position - top / bottom
	n_rows = template.shape[0]
	template = pd.concat([template, template])
	template.loc[:, 'pos'] = 0.7  # top
	template.iloc[:n_rows, 'pos'] = -0.7 # bottom

	# proportion of trials of Cued vs Free type
	prop = random.choice(settings['proportions'])
	df = pd.concat([template.query('choiceType == "Cued"')] * prop[0] +
				   [template.query('choiceType == "Free"')] * prop[1])
	df = shuffle_rows(df)

	# add rows that were not present in the template
	temp_cols = [c for c in columns if c not in template.columns]
	for c in temp_cols:
		df[c] = 0
	df['block'] = blockNum

	# make sure dtypes are correct
	for col, tp in zip(columns, dtp):
		df[col] = df[col].astype(tp)

	return df
