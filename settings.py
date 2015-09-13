import random
import numpy as np

Kwadrat = np.array([
[0, 3, 2, 1],
[1, 0, 3, 2],
[2, 1, 0, 3],
[3, 2, 1, 0]
])

exp = dict()
exp['kwadrat'] = Kwadrat
exp['buttons'] = ['l', 'd']
exp['block trials'] = 72
exp['proportions'] = [3, 0.33333]


def shuffle_colors(stim):
	Kolory = []
	Kolory.append(stim['circle']['red'])
	Kolory.append(stim['circle']['green'])
	Kolory.append(stim['circle']['yellow'])
	Kolory.append(stim['circle']['blue'])

	# Randomize array Kolory:
	random.shuffle(Kolory)
	return Kolory

def get_colors_from_square(colors, N, exp=exp):
	names = ['lc', 'li', 'rc', 'ri']
	cond_colors = {cnd: colors[exp['kwadrat'][N, i]] 
		for i, cnd in enumerate(names)}
