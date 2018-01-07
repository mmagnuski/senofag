# encoding: utf-8

import os
from os import path as op
from PIL import Image

import numpy as np
from psychopy import core, visual, event, monitors, parallel


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
    image_size = np.array(img.size)
    image_size = np.round(image_size * scale).astype('int')
    return visual.ImageStim(win=win, image=image, units='pix',
                            size=image_size, **kwargs)


class Trigger(object):
    def __init__(self, port_address, mapping=None):
        self.port_address = port_address
        self.mapping = mapping
        self.frames = list()
        self.trigger_values = list()

    def set_sequence(self, frames, trigger_values):
        self.frames = frames
        self.trigger_values = trigger_values

    def react_to_frame(self, frame_num):
        if frame_num in self.frames:
            idx = self.frames.index(frame_num)
            value = self.trigger_values[idx]
            # TODO send trigger


def create_stimuli(fullscr=False):
    # create window (MUST BE CHANGED (E.G. TO A DEFAULT ONE))
    window = visual.Window((1200, 1000), fullscr=fullscr, monitor='testMonitor',
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

    # create rating scale
    navig = dict(leftKeys='f', rightKeys = 'j', acceptKeys='space',
                 low=1, high=7, markerStart=4, markerColor='seagreen',
                 showValue=False, showAccept=False, pos=(0., 0.),
                 scale='', labels=['niskie', 'wysokie'])

    stim['rating scale'] = visual.RatingScale(window, **navig)

    return stim


# [ ] triggers could be sent by onFlip function, then reset on other frames
def show_stim(window, stimuli=None, n_frames=10, resp_clock=None, trigger=None):
    if stimuli is None:
        stimuli = list()
    elif not isinstance(stimuli, list):
        stimuli = [stimuli]

    for frame in range(n_frames):
        for stim in stimuli:
            stim.draw()
        window.flip()

        # check if trigger object has something to say
        if trigger is not None:
            trigger.react_to_frame(frame)

        # reset response clock if it is the first frame
        if frame == 0 and resp_clock is not None:
            resp_clock.reset()


def show_trial(df, stim, trial, effect_colors=None, resp_clock=None):
    if resp_clock is None:
        resp_clock = core.Clock()

    # get stimuli
    fix = stim['fix']
    window = stim['win']
    prime = stim[df.loc[trial, 'prime']]
    target = stim[df.loc[trial, 'target']]

    # set position
    prime.pos = (0., df.loc[trial, 'pos'])
    target.pos = (0., df.loc[trial, 'pos'])

    # show fixation
    fix_frames = df.loc[trial, 'fixTime']
    show_stim(window=window, stimuli=fix, n_frames=fix_frames)

    # show prime (TODO: add Trigger to prime)
    show_stim(window=window, stimuli=fix + [prime], n_frames=2)
    show_stim(window=window, stimuli=fix, n_frames=4)

    # clear keybord buffer, show target (TODO: add Trigger)
    event.getKeys()
    show_stim(window=window, stimuli=fix + [target], n_frames=25,
              resp_clock=resp_clock)

    # get response
    keys = event.getKeys(keyList=['f', 'j'], timeStamped=resp_clock)
    # 1500 ms for response if not already given
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['f', 'j'], timeStamped=resp_clock,
                              maxWait=1.2)

    # evaluate repsonse
    eval_resp(df, trial, keys, effect_colors=effect_colors)
    circle = stim['circle'][df.loc[trial, 'effect']]

    # delay 1 (jittered 40 - 60 frames)
    # high is 61 because randint upper limit is exclusive
    delay_frames = np.random.randint(low=40, high=61)
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'delay1'] = delay_frames

    # show effect (TODO: add Trigger)
    show_stim(window=window, stimuli=circle, n_frames=25)

    # delay 2 (jittered 75 - 125 frames); again high is exclusive
    delay_frames = np.random.randint(low=75, high=126)
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'delay2'] = delay_frames

    # rate sense of agency (TODO: set maxWait?)
    stim['rating scale'].reset()
    while stim['rating scale'].noResponse:
        stim['rating scale'].draw()
        window.flip()

    # save responses to df
    df.loc[trial, 'soa_rating'] = stim['rating scale'].getRating()
    df.loc[trial, 'rating_RT'] = stim['rating scale'].getRT()

    # post-trial random interval, 25 - 75 frames
    delay_frames = np.random.randint(low=25, high=76)
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'ITI'] = delay_frames


def eval_resp(df, trial, keys, effect_colors=None):
    if keys is None or len(keys) == 0:
        keys = 'NoResp'
        df.loc[trial, 'effect'] = 'cross'
        df.loc[trial, 'resp'] = keys
        df.loc[trial, 'RT'] = np.nan
    else:
        df.loc[trial, 'resp'] = keys[0][0]
        df.loc[trial, 'RT'] = keys[0][1]
        df.loc[trial, 'ifcorr'] = keys[0][0] in df.loc[trial, 'corrResp']
        if not df.loc[trial, 'ifcorr']:
            df.loc[trial, 'effect'] = 'cross'
        else:
            used_hand = 'l' if keys == 'f' else 'r'
            condition = 'c' if used_hand == df.loc[trial, 'prime'][6] else 'i'
            df.loc[trial, 'effect'] = effect_colors[used_hand + condition]


def show_break(window):
    # TODO add info about how many trials passed, which block it is ...
    event.getKeys()
    text = visual.TextStim(window, text=u'Aby przejść dalej\nnaciśnij spację')
    text.draw()
    window.flip()

    # wait for space
    keys = event.getKeys(keyList=['space'])
    # 1500 ms for response if not already given
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['space'])

    # TODO random wait after break


def run_block(block_df, stim, block_num=0, break_every=15, effect_colors=None):
    n_trials = block_df.shape[0]
    suffix = '_block_{}.csv'.format(block_num)
    fname = os.path.join(settings['data dir'],
                         settings['subject name'] + suffix)
    for trial in range(n_trials):
        show_trial(block_df, stim, trial, effect_colors=effect_colors)

        # write data after every trial
        # (TODO: include save time in between-trial interval)
        block_df.to_csv(fname)

        if (trial + 1) % break_every == 0:
            show_break(stim['win'])
