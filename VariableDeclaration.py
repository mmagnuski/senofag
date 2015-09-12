#############
# to mozna potem wywalic:

from psychopy import core, visual, event, monitors
import os

PTH = r"C:\Users\LEON-NETB\Dropbox\LEON_CIECHANOWSKI\images" # MUST BE CHANGED LATER
os.chdir(PTH)

#############
# VariableDeclaration:
#############

import random
import numpy as np
import pandas as pd

import stim

#############

NUM_OBJECTS = 6

####

Kolory = []
Kolory.append(stim.stim['circle']['red'])
Kolory.append(stim.stim['circle']['green'])
Kolory.append(stim.stim['circle']['yellow'])
Kolory.append(stim.stim['circle']['blue'])
Kolory.append(stim.stim['circle']['orange'])
Kolory.append(stim.stim['circle']['purple'])

# Randomize array Kolory:
random.shuffle(Kolory)


# Generating the Latin Square

Kwadrat = np.array([
[0,1,2,3,4,5],
[1,2,3,4,5,0],
[2,3,1,4,0,5],
[3,4,2,5,1,0],
[4,5,0,1,2,3],
[5,0,4,1,3,2]
])

N = -1



#################################
# InLine1 (from 'BlockProc1'):
#################################

# To 'N' bedzie trzeba zamknac w ladna petle (w kazdym nowym bloku ma dodawac '+ 1'):
N = N + 1
BlockNumber = N + 1

# Definicja nie/kompatybilnosci
left_comp = Kolory[Kwadrat[N, 0]]
left_neut = Kolory[Kwadrat[N, 1]]
left_incomp = Kolory[Kwadrat[N, 2]]
right_comp = Kolory[Kwadrat[N, 3]]
right_neut = Kolory[Kwadrat[N, 4]]
right_incomp = Kolory[Kwadrat[N, 5]]


#################################
# InLine3 (from 'BlockProc1'):
#################################

# Draws a random number for waiting between the stimulus and the effect
WaitTime = random.randrange(1,4,1)*150

# Draws a random number for positioning the stimuli
Posit = random.choice([25, 75])



##############
# DEBUG
'''
Kolory[5].draw()
stim.win.flip()
event.waitKeys()
'''

'''
print "\nEverything's gonna be alright"
'''