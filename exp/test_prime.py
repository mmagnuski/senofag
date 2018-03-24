import os
import os.path as op
from random import shuffle
import numpy as np

from psychopy import visual, core, event
from settings import (create_settings, create_block, get_colors_from_square,
                     raise_error)
from stim import (subject_id_gui, create_stimuli, run_block, ArrowStim,
                  prime_from_arrow)

colors = ['red', 'green', 'yellow', 'blue']
settings = create_settings(short_test=False, send_triggers=False)
stim = create_stimuli(fullscr=True, settings=settings, monitor='lab')

# TODO change arrow arrow_sharpness, color & magnitude! approx. 3.8 degrees,
# 60 cm away from the screen

window = stim['win']
arrow = ArrowStim(stim['win'], razor_width=1.5, arrow_width=2.5,
                  arrow_sharpness=1.5, razor_sharpness=0.2)
prime = prime_from_arrow(arrow)

prime.draw()
window.flip()
event.waitKeys()

arrow.draw()
window.flip()
event.waitKeys()

arrow.setPos((0., 3.))
prime.setPos((0., 3.))
window.flip()
core.wait(1.)
prime.draw()
window.flip()
arrow.draw()
window.flip()
event.waitKeys()
