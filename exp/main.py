import os
import os.path as op
from random import shuffle

from settings import create_settings, create_block, get_colors_from_square
from stim import subject_id_gui, create_stimuli, run_block, Instructions


# quick settings
show_instructions = True
show_training = True

colors = shuffle(['red', 'green', 'yellow', 'blue'])

settings = create_settings(short_test=False, send_triggers=False)
subject_id = subject_id_gui()
settings['subject name'] = subject_id
stim = create_stimuli(fullscr=True, settings=settings)
trigger = stim['trigger']

# make sure data dir exists
if not op.isdir(settings['data dir']):
    os.mkdir(settings['data dir'])

# show instructions
if show_instructions:
    instr_dir = op.join(os.getcwd(), 'instr')
    instructions = [op.join(instr_dir, f) for f in os.listdir(instr_dir)]
    instr = Instructions(stim['win'], instructions)
    instr.present(stop=10)

# TRAINING:
block_args = dict(trigger=trigger, settings=settings)

if show_training:
    block_num = 0
    test_df = create_block(blockNum=block_num, settings=settings)
    cond_color = get_colors_from_square(colors, block_num, settings=settings)
    run_block(test_df, stim, block_num, effect_colors=cond_color,
              show_effect=False, suffix='training', **block_args)

# INSTRUCTIONS between the training and main blocks
# 'start' should be smaller by 1 than the desired slide number
# here it starts from the slide 11 and ends with the 12
if show_instructions: instr.present(start=10, stop=12)

#MAIN BLOCKS
for block_num in range(4):
    block_df = create_block(block_num, settings=settings)
    cond_color = get_colors_from_square(colors, block_num, settings=settings)
    run_block(block_df, stim, block_num=block_num, effect_colors=cond_color,
              **block_args)

    # show between-block instructions
    instr.present(start=12, stop=14)

# END INSTRUCTIONS:
# TODO add keyList 't' or 'n' to the available answers here and
# save them somewhere in the data (?) or add the last question to the
# next procedure (detection task)
if show_instructions: instr.present(start=14, stop=16)
