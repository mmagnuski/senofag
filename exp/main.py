import os
from settings import create_settings, create_block, get_colors_from_square
from stim import subject_id_gui, create_stimuli, run_block, Instructions


subject_id = subject_id_gui()
settings = create_settings(short_test=False, send_triggers=False)
settings['subject name'] = subject_id
stim = create_stimuli(fullscr=True, settings=settings)
trigger = stim['trigger']
colors = ['red', 'green', 'yellow', 'blue']
# colors = st.shuffle_colors(stim)

# make sure data dir exists
if not os.path.isdir(settings['data dir']):
    os.mkdir(settings['data dir'])

# show instructions
show_instructions = True
instr_dir = os.path.join(os.getcwd(), 'instr')
instructions = [os.path.join(instr_dir, f) for f in os.listdir(instr_dir)]
if len(instructions) > 0:
	instr = Instructions(stim['win'], instructions)
	instr.present(stop=10)

# TRAINING:
show_test = True
block_args = dict(trigger=trigger, settings=settings)

if show_test:
    block_num = 0
    test_df = create_block(blockNum=block_num, settings=settings)
    cond_color = get_colors_from_square(colors, block_num, settings=settings)
    run_block(test_df, stim, block_num, effect_colors=cond_color,
              show_effect=False, suffix='training', **block_args)

# INSTRUCTIONS between the training and main blocks
# 'start' should be smaller by 1 than the desired slide number
# here it starts from the slide 11 and ends with the 12
instr.present(start=10, stop=12)

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
instr.present(start=14, stop=16)
