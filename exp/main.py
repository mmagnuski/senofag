from settings import create_settings, create_block, get_colors_from_square
from stim import create_stimuli, show_trial

settings = create_settings()
stim = create_stimuli()
# colors = st.shuffle_colors(stim)

N = 0
blck = create_block(N, settings=settings)
colors = ['red', 'green', 'yellow', 'blue']
cond_color = get_colors_from_square(colors, N, settings=settings)

for t in range(1, 4):
	show_trial(blck, stim, t, effect_colors=cond_color)
