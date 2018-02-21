import os
import os.path as op
import pandas as pd
from random import shuffle

from settings import (create_settings, create_block, get_colors_from_square,
                     raise_error)
from stim import subject_id_gui, create_stimuli, run_block, Instructions
from psychopy import event, visual


# quick settings
debug_mode = True
show_instructions = True
show_training = False
show_main_proc = False
show_prime_detection_task = False

colors = ['red', 'green', 'yellow', 'blue']
shuffle(colors)

settings = create_settings(short_test=False, send_triggers=False)
settings_prime = create_settings(short_test=False, prime_task=True,
                          send_triggers=False)

subject_data = subject_id_gui()
settings['subject name'] = subject_data[0]
settings['subject group'] = subject_data[1]

stim = create_stimuli(fullscr=True, settings=settings)
trigger = stim['trigger']

# make sure data dir exists
if not op.isdir(settings['data dir']):
    os.mkdir(settings['data dir'])

# show instructions
def select_instructions(fname, group):
    return not 'b' in fname if group == '1' else not 'a' in fname

if show_instructions:
    instr_dir = op.join(os.getcwd(), 'instr')
    instructions = [op.join(instr_dir, f) for f in os.listdir(instr_dir)
                    if select_instructions(f, settings['subject group'])]
    instr = Instructions(stim['win'], instructions)
    instr_offset = int(settings['subject group']) - 1
    instr.present(stop=10 + instr_offset)


# TRAINING:
block_num = 0
n_trials = 2 if debug_mode else 14
break_every = 2 if debug_mode else 5
block_args = dict(trigger=trigger, settings=settings)
if show_training:
    test_df = create_block(blockNum=block_num, settings=settings)
    cond_color = get_colors_from_square(colors, block_num, settings=settings)
    run_block(test_df, stim, effect_colors=cond_color, show_effect=False,
              suffix='_training.csv', break_every=break_every, n_trials=2,
              **block_args)

# INSTRUCTIONS between the training and main blocks
if show_instructions:
    instr.present(stop=12 + instr_offset)

# MAIN BLOCKS
n_trials = 2 if debug_mode else None
break_every = 2 if debug_mode else None
if show_main_proc:
    for block_num in range(4):
        block_df = create_block(block_num, settings=settings)
        cond_color = get_colors_from_square(colors, block_num,
                                            settings=settings)
        run_block(block_df, stim, show_effect=True,
                  suffix='_regular_block_{}.csv'.format(block_num),
                  effect_colors=cond_color, break_every=break_every,
                  n_trials=2, **block_args)

        # show between-block instructions
        if show_instructions:
            instr.present(stop=14 + instr_offset)

# END INSTRUCTIONS:
if show_instructions:
    instr.present(stop=16 + instr_offset)

# show the slide with prime detection initial question
    # get response
    # FIXME prime_question is not displayed but the system waits for keys
    event.getKeys()
    prime_question = visual.ImageStim(stim['win'], image=instructions[26])
    prime_question.draw()
    keys = event.getKeys(keyList=['t', 'n'])
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['t', 'n'])
    if keys is not None:
        settings['prime seen'] = keys
# prime detection task instructions:
        instr.present(start=15 + instr_offset, stop=21 + instr_offset)


# prime detection task presentation:
# block_args['settings'] = settings_prime
if show_prime_detection_task:
    for block_num in range(4):
        block_df = create_block(block_num, settings=settings_prime)
        run_block(block_df, stim, prime_det=True,
                  suffix='_prime_detection_block_{}.csv'.format(block_num),
                  break_every=break_every, n_trials=n_trials, **block_args)
        # show between-block instructions
        if show_instructions:
            instr.present(stop=23 + instr_offset)

# END PROCEDURE INSTRUCTIONS:
if show_instructions:
    instr.present(stop=25 + instr_offset)

# saving settings to have the prime visibility question
settings_df = pd.DataFrame.from_dict(settings, orient='index')
settings_df_name = 'SoA_{}_{}'.format(
    settings['subject group'], settings['subject name']) + '_settings.csv'
settings_df.to_csv(os.path.join(settings['data dir'], settings_df_name))
