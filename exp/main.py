import settings as st
from stim import create_stimuli, show_trial

blck = st.get_block(0)
stim = create_stimuli()
# colors = st.shuffle_colors(stim)

N = 0
colors = ['red', 'green', 'yellow', 'blue']
cond_color = st.get_colors_from_square(colors, N)

for t in range(1, 4):
	show_trial(blck, stim, t, effect_colors=cond_color)
