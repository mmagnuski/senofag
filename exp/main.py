import os
from settings import create_settings, create_block, get_colors_from_square
from stim import create_stimuli, show_trial

settings = create_settings()
stim = create_stimuli(fullscr=True)
# colors = st.shuffle_colors(stim)

block_number = 0
blck = create_block(block_number, settings=settings)
colors = ['red', 'green', 'yellow', 'blue']
cond_color = get_colors_from_square(colors, block_number, settings=settings)
data_fname = 'test_subject_block_{}.csv'.format(block_number)

for trial in range(1, 6):
	show_trial(blck, stim, trial, effect_colors=cond_color)
	blck.to_csv(os.path.join(settings['data dir'], data_fname))