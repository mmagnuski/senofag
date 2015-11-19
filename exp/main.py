import settings as st
from stim import stim

blck = st.get_block(0)
colors = st.shuffle_colors(stim)

N = 0
cond2color = get_colors_from_square(colors, N)

for t in range(1, 4):
	stim.show_trial(blck, stim.stim, t)
