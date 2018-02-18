import os
import os.path as op
from random import shuffle

from settings import (create_settings, create_block, get_colors_from_square,
                     raise_error)
from stim import subject_id_gui, create_stimuli, run_block, Instructions


# quick settings
show_instructions = False
show_training = False
show_main_proc = False
show_prime_detection_task = True

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
block_args = dict(trigger=trigger, settings=settings)
if show_training:
    test_df = create_block(blockNum=block_num, settings=settings)
    cond_color = get_colors_from_square(colors, block_num, settings=settings)
    run_block(test_df, stim, effect_colors=cond_color, break_every=2,
              n_trials=2, show_effect=False, suffix='_training.csv',
              **block_args)

# INSTRUCTIONS between the training and main blocks
if show_instructions:
    instr.present(stop=12 + instr_offset)

# MAIN BLOCKS
if show_main_proc:
    for block_num in range(4):
        block_df = create_block(block_num, settings=settings)
        cond_color = get_colors_from_square(colors, block_num,
                                            settings=settings)
        run_block(block_df, stim, show_effect=True,
                  suffix='_regular_block_{}.csv'.format(block_num),
                  effect_colors=cond_color, **block_args)

    # show between-block instructions
    if show_instructions:
        instr.present(stop=14 + instr_offset)

# END INSTRUCTIONS:
# TODO add keyList 't' or 'n' to the available answers here and
# save them somewhere in the data (?) or add the last question to the
# next procedure (detection task)
if show_instructions:
    instr.present(stop=15 + instr_offset)

# prime detection task presentation:
# block_args['settings'] = settings_prime
if show_prime_detection_task:
    for block_num in range(4):
        block_df = create_block(block_num, settings=settings_prime)
        run_block(block_df, stim, prime_det=True, break_every=2,
                  suffix='_prime_detection_block_{}.csv'.format(block_num),
                  **block_args)
