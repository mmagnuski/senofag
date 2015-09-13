import random
import numpy as np

Kwadrat = np.array([
[0,1,2,3,4,5],
[1,2,3,4,5,0],
[2,3,1,4,0,5],
[3,4,2,5,1,0],
[4,5,0,1,2,3],
[5,0,4,1,3,2]
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
	Kolory.append(stim['circle']['orange'])
	Kolory.append(stim['circle']['purple'])

	# Randomize array Kolory:
	random.shuffle(Kolory)
	return Kolory

def get_colors_from_square(colors, N, exp=exp):
	names = ['lc', 'ln', 'li', 'rc', 'rn', 'ri']
	cond_colors = {cnd: colors[exp['kwadrat'][N, i]] 
		for i, cnd in enumerate(names)}
