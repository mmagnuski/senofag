# coding: utf-8

import numpy as np
import pandas as pd
import os
import os.path as op
import glob

PTH = r"C:\PhD_SoA_Study\senofag\exp\data"
fls = glob.glob(op.join(PTH, '*.csv'))

def DF_prep():
    df = pd.DataFrame()
    for file in fls:
        split_file = file.split('\\')[5]
        if 'regular' in split_file:
            person_nr = split_file.split('_')[2]
            group_nr = int(split_file.split('_')[1])

            # FIXME - przy nowych danych można usunąć "block_nr"
            block_nr = split_file.split('_')[-1].split('.')[0]
            df_person = pd.read_csv(os.path.join(PTH, file), sep=',')
            df_person.loc[:, 'subject_nr'] = person_nr
            df_person.loc[:, 'block_nr'] = block_nr
            df_person.loc[:, 'group_nr'] = group_nr
            df = df.append(df_person, ignore_index=True)


    # Counting groups:

    df_groups = {'Group_1': 0, 'Group_2': 0}

    for name in np.unique(df['subject_nr']):
        if np.unique(df.query('subject_nr == "{}"'.format(name)).group_nr) == 1:
            df_groups["Group_1"] += 1
        else:
            df_groups["Group_2"] += 1

    print("Number of rows =", len(df.index))
    print("Number of persons =", len(np.unique(df['subject_nr'])))
    print("Persons' numbers =", np.unique(df['subject_nr']))
    print(df_groups)

    return df


def DF_prime_prep():
    df2 = pd.DataFrame()
    for file in fls:
        # Below at home:
    #     split_file = file.split('\\')[6]
        # Below in the lab:
        split_file = file.split('\\')[5]
        if 'prime' in split_file:
            person_nr = split_file.split('_')[2]
            group_nr = split_file.split('_')[1]
            block_nr = split_file.split('_')[-1].split('.')[0]

            df2_person = pd.read_csv(os.path.join(PTH, file), sep=',')

            df2_person.loc[:, 'subject_nr'] = person_nr
            df2_person.loc[:, 'block_nr'] = block_nr
            df2_person.loc[:, 'group_nr'] = group_nr
            df2 = df2.append(df2_person, ignore_index=True)

    df2['ifcorr'] = df2['ifcorr'].map({False:0, True:1})

    print("Number of rows =", len(df2.index))
    print("Number of persons =", len(np.unique(df2['subject_nr'])))
    print("Persons' numbers =", np.unique(df2['subject_nr']))

    return df2
