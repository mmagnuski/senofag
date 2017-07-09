import os
from os import path as op
from PIL import Image

import numpy as np
from psychopy import core, visual, event, monitors


def circle(win, col='green', pos=(0,0), r=2.5):
    circ = visual.Circle(win, pos=pos, radius=r, edges=128, units='deg',
                         interpolate=True)
    circ.setFillColor(col)
    circ.setLineColor(col)
    return circ


def whiteshape(v, win=None):
    return visual.ShapeStim(win, lineWidth=0.5, fillColor=[1, 1, 1],
                            lineColor=[1, 1, 1], vertices=v, closeShape=True)

# create fixation cross:
def fix(ln=1, lw=0.1, win=None):
    hlw = lw / 2
    v = np.array([[hlw, -ln], [hlw, ln], [-hlw, ln], [-hlw, -ln]])
    fix = list()
    fix.append(whiteshape(v, win=win))
    fix.append(whiteshape(np.fliplr(v), win=win))
    return fix


def resized_image(win=None, image=None, scale=1, **kwargs):
    img = Image.open(image)
    image_size = np.array([img.width, img.height])
    image_size = np.round(image_size * scale).astype('int')
    return visual.ImageStim(win=win, image=image, units='pix',
                            size=image_size, **kwargs)


def create_stimuli(fullscr=False):
    # create window (MUST BE CHANGED (E.G. TO A DEFAULT ONE))
    window = visual.Window((1200, 1000), fullscr=False, monitor='testMonitor',
                           units='deg', color='black')

    # a list of stimuli images:
    stim = {image: resized_image(win=window, image=op.join('pic', image),
                                 scale=0.5) for image in os.listdir('pic')}
    stim['win'] = window
    stim['fix'] = fix(win=window)

    # a list of colors images:
    colors = ['grey', 'blue', 'red', 'green', 'yellow']
    stim['circle'] = {c: circle(window, col=c) for c in colors}
    stim['circle']['cross'] = stim['cross.png']
    return stim


def show_trial(df, stim, trial, effect_colors=None):
    # show fixation
    fix_frames = df.loc[trial, 'fixTime']
    for f in stim['fix']:
        f.autoDraw = True

    for _ in range(fix_frames):
        stim['win'].flip()

    # show prime
    stim[df.loc[trial, 'prime']].draw()
    stim['win'].flip()

    # show target
    event.getKeys()
    for _ in range(25):
        stim[df.loc[trial, 'target']].draw()
        stim['win'].flip()

    # 1500 ms for response
    for _ in range(150):
        key = event.getKeys()
        if key:
            break
        stim['win'].flip()

    for f in stim['fix']:
        f.autoDraw = False

    # evaluate repsonse
    eval_resp(df, trial, key, effect_colors=effect_colors)

    for _ in range(30):
        stim['circle'][df.loc[trial, 'effect']].draw()
        stim['win'].flip()


def eval_resp(df, trial, key, effect_colors=None):
    if len(key) == 0:
        key = 'NoResp'
        df.loc[trial, 'effect'] = 'cross'
        df.loc[trial, 'resp'] = key
    else:
        df.loc[trial, 'resp'] = key[0]
        df.loc[trial, 'ifcorr'] = key[0] in df.loc[trial, 'corrResp']
        if not df.loc[trial, 'ifcorr']:
            df.loc[trial, 'effect'] = 'cross'
        else:
            used_hand = 'l' if key == 'd' else 'r'
            condition = 'c' if used_hand == df.loc[trial, 'prime'][6] else 'i'
            df.loc[trial, 'effect'] = effect_colors[used_hand + condition]
