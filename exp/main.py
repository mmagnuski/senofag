import os
from settings import create_settings, create_block, get_colors_from_square
from stim import create_stimuli, show_trial, Instructions

settings = create_settings()
stim = create_stimuli(fullscr=True)
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
	instr.present()


block_number = 0
blck = create_block(block_number, settings=settings)
colors = ['red', 'green', 'yellow', 'blue']
cond_color = get_colors_from_square(colors, block_number, settings=settings)
data_fname = 'test_subject_block_{}.csv'.format(block_number)

for trial in range(1, 6):
	show_trial(blck, stim, trial, effect_colors=cond_color)
	blck.to_csv(os.path.join(settings['data dir'], data_fname))
