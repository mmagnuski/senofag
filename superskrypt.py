# coding: utf-8

import numpy as np
import pandas as pd
import os

# ustawianie
# pth = r'C:\Users\LEON-NETB\Dropbox\eksperymentLC_final'
# fl = 'test.txt'
# fullfl = os.path.join(pth, fl)

# wczytywanie pliku
# print 'wczytywanie pliku:\n{}'.format(fullfl)
# df = pd.read_table(fullfl, sep='\t')

def ischar(x):
        return isinstance(x, str)


def give_coldict(df):
    '''
    Returns dictionary of mapping between colors
    and experimental conditions in passed dataframe.

    Usage:
    coldict = give_coldict(dataframe)
    '''
    # wybieramy tylko interesujace kolumny
    cols =['Effect', 'Prime', 'Target', 'TargetSlide.RESP', 'TrialType']
    d = df.loc[:, cols]

    # wywalamy braki/niepopr odp (this could be sped up)
    ind = ~(d.loc[:, 'Effect'] == ' ')
    ind = ind & d.loc[:, 'Effect'].map(ischar)
    d = d[ind]

    # skracanie nazw
    for j in range(0,3):
        for i in range(d.shape[0]):
            d.iloc[i, j] = d.iloc[i, j].split('.')[0].split('_')[1][0]

    # przemapowanie nazw klawiszy na left / right
    # could be done with d['TargetSlide.RESP'] == mapping[k] etc.
    mapping = {'l' : 'r', 'd' : 'l'}
    def use_map(x, mp = mapping):
        return mp[x]
    d['TargetSlide.RESP'] = d['TargetSlide.RESP'].map(use_map)

    # resetujemy index
    d.reset_index(inplace=True)

    # sprawdzamy kolory
    colors = list(d.loc[:,'Effect'].unique())
    coldict = {}

    for i, col in enumerate(d['Effect']):
        if col in colors:
            # if not neutral - remove from colors and test
            if not d.loc[i, 'TrialType'] == 'neut':
                colors.pop(colors.index(col))
                coldict[col] = 'comp' if d.loc[i, 'Prime'] == \
                    d.loc[i, 'TargetSlide.RESP'] else 'incomp'
                coldict[col] += '_' + d.loc[i, 'TargetSlide.RESP']

    # set rest to neut ! CHANGE HERE to neut_l and neut_r !
    for col in colors:
        coldict[col] = 'neut'
    return coldict


def get_block_list(df, n = 9):
    '''
    Gives list of unique block numbers that correspond
    to at least n rows in the passed dataframe.

    Usage:
    get_block_list(dataframe)
    get_block_list(dataframe, n=5)
    '''
    # bierzemy bloki
    blocks = df['Block'].unique()

    # robimy selekcje po ilosci triali w bloku
    blocklen = []
    for b in blocks:
        blocklen.append(df[df['Block'] == b].shape[0])
    blocks = blocks[np.array(blocklen) > n]
    return blocks

def all_colors(df):

    return {x: give_coldict(df[df['Block'] == x]) \
        for x in get_block_list(df)}


def get_sorted_colors(df, blocknum=1):

    checkColumn = 'GoalRespName1'
    tempcol = df.loc[df['Block'] == blocknum, checkColumn]

    ind = tempcol.map(ischar)
    tempdf = df.loc[df['Block'] == blocknum, :].loc[ind,:]
    
    # sprawdzamy jak oszacowana zostala sprawczość dla kolorów
    tbox = ['TBox{}'.format(i) for i in range(1, 7)]
    tb = tempdf.loc[:, tbox].iloc[1, :].values
    ratings = tb.astype("int")

    col = ['GoalRespName{}'.format(i) for i in range(1, 7)]
    coldf = df.loc[df['Block'] == blocknum, col].loc[ind,:].iloc[0]
    sorted_colors = [x.split('.')[0].split('_')[1][0] for x in coldf]
    return sorted_colors, ratings


def get_color_info(df):
    
    # get dict of colors:
    coldict = all_colors(df)

    blocks = get_block_list(df)
    ratings = {b : get_sorted_colors(df, b) for b in blocks}
    # howsorted = [coldict[2][x] for x in sorted_colors]
    
    rating_dict = {cnd : [] for cnd in coldict[3].values()}
    for b in ratings.keys():
        col_ord, rating = ratings[b]
        for c in coldict[b].keys():
            cond = coldict[b][c]
            col_ind = col_ord.index(c)
            rt = rating[col_ind]
            rating_dict[cond].append(rt)
    return rating_dict
