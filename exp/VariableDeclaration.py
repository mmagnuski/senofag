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
from stim import stim as s

#############

NUM_OBJECTS = 6

####


#################################
# InLine1 (from 'BlockProc1'):
#################################

# To 'N' bedzie trzeba zamknac w ladna petle (w kazdym nowym bloku ma dodawac '+ 1'):
N = N + 1
BlockNumber = N + 1

# Definicja nie/kompatybilnosci


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