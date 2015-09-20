# coding: utf-8

import numpy as np
import pandas as pd
import os


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
    d.reset_index(inplace=True, drop=True)

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
            if d.loc[i, 'TrialType'] == 'neut':
                colors.pop(colors.index(col))
                coldict[col] = 'neut_r' if d.loc[i, 'TargetSlide.RESP'] == 'r' else 'neut_l'
    return coldict

def firstletter(df, col):
    if isinstance(col, int):
        for i in range(df.shape[0]):
            try:
                df.iloc[i, col] = df.iloc[i, col].split('.')[0].split('_')[1][0]
            except:
                continue
    elif isinstance(col, str):
        for i in df.index:
            try:
                df.loc[i, col] = df.loc[i, col].split('.')[0].split('_')[1][0]
            except:
                continue


def get_block_list(df, n = 11):
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


##############################################################
# Adding RT to the DataFrame:

def get_RT(df):
    rr = all_colors(df)
    cols = ['Block', 'Effect', 'Prime', 'Target', 'TargetSlide.RESP', 'TrialType', 'TargetSlide.RT', 'Condition', 
        'comp_r_RT', 'comp_l_RT', 'incomp_r_RT', 'incomp_l_RT', 'neut_r_RT', 'neut_l_RT', 'comp_RT', 
        'incomp_RT', 'neut_RT']
    rt = df.loc[:, cols]
    def get_first_char(x):
        if not pd.isnull(x):
            return x.split('_')[1][0]

    for i in rt.index:
        rt.loc[i, 'Effect'] = get_first_char(rt.loc[i, 'Effect'])

    ind = rt.loc[:, 'Effect'].isnull()
    dff = rt.loc[~ind, :]

    mapping = {'l' : 'r', 'd' : 'l'}
    def use_map(x, mp = mapping):
        return mp[x]

    dff.loc[:, 'TargetSlide.RESP'] = dff.loc[:, 'TargetSlide.RESP'].map(use_map)
    dff.reset_index(inplace=True, drop=True)

    for block in dff.Block.unique():
        mapping = rr[block]
        block_df = dff.query('Block == {}'.format(block))
        al_colors = dff.Effect.unique()
        for c in al_colors:
            ind = block_df.Effect == c
            block_df.loc[ind, 'Condition'] = mapping[c]
            dff.loc[dff['Block'] == block, 'Condition'] = block_df.loc[block_df['Block'] == block, 'Condition']
    
    cond_list = ['comp_r', 'comp_l', 'incomp_r', 'incomp_l', 'neut_r', 'neut_l']
    for item in cond_list:
        dff.loc[:, '{}'.format(item+'_RT')] = np.mean(dff.loc[dff['Condition'] == item, 'TargetSlide.RT'])

    rt_base = pd.DataFrame()
    for item in cond_list:
        rt_base.loc[1, '{}'.format(item+'_RT')] = dff.loc[1, '{}'.format(item+'_RT')]

    for c in rt_base.columns:
        for i in rt_base.index:
            rt_base.loc[i, 'comp_RT'] = (rt_base.loc[i, 'comp_l_RT']+rt_base.loc[i, 'comp_r_RT'])/2
            rt_base.loc[i, 'incomp_RT'] = (rt_base.loc[i, 'incomp_l_RT']+rt_base.loc[i, 'incomp_r_RT'])/2
            rt_base.loc[i, 'neut_RT'] = (rt_base.loc[i, 'neut_l_RT']+rt_base.loc[i, 'neut_r_RT'])/2
    return rt_base
