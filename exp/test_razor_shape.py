import os
import os.path as op
from random import shuffle
import numpy as np

from psychopy import visual, event
from settings import (create_settings, create_block, get_colors_from_square,
                     raise_error)
from stim import subject_id_gui, create_stimuli, run_block, ArrowStim

colors = ['red', 'green', 'yellow', 'blue']
settings = create_settings(short_test=False, send_triggers=False)
stim = create_stimuli(fullscr=True, settings=settings)

#arrow = ArrowStim(stim['win'])
#arrow.draw()
#stim['win'].flip()
#event.waitKeys()


# TODO change arrow arrow_sharpness, color & magnitude! approx. 3.8 degrees,
# 60 cm away from the screen

arrow = ArrowStim(stim['win'], razor_width=1.5, arrow_width=2.5,
                  arrow_sharpness=1.5, razor_sharpness=0.2)
arrow.draw()
stim['win'].flip()
event.waitKeys()

#arrow = ArrowStim(stim['win'], razor_width=2., arrow_width=3.,
#                  arrow_sharpness=2.)
#arrow.draw()
#stim['win'].flip()
#event.waitKeys()

#arrow = ArrowStim(stim['win'], razor_width=2., arrow_width=3.,
#                  arrow_sharpness=2., razor_sharpness=0.5)
#arrow.setPos((0., 3.))
#arrow.draw()
#stim['win'].flip()
#event.waitKeys()
