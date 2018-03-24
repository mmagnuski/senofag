# encoding: utf-8

import os
from os import path as op
import types
import time
from PIL import Image

import numpy as np
import pandas as pd

from psychopy import core, visual, event, gui, monitors, parallel
from settings import ensure_dtypes


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
    def __init__(self, port_address=None):
        self.frames = list()
        self.trigger_values = list()

        if port_address is not None and port_address:
            self.port = parallel.ParallelPort(address=port_address)
        else:
            self.port = False

    def set_sequence(self, frames, trigger_values):
        self.frames = frames
        self.trigger_values = trigger_values

    def react_to_frame(self, frame_num):
        if self.port and frame_num in self.frames:
            idx = self.frames.index(frame_num)
            value = self.trigger_values[idx]
            self.port.setData(value)

    def send(self, value):
        if self.port:
            self.port.setData(value)


def create_stimuli(fullscr=False, settings=None, monitor='lab'):
    if monitor == 'lab':
        monitor = monitors.Monitor('BenQ', width=53.136, distance=80)
        monitor.setSizePix((1920, 1080))
    window = visual.Window(fullscr=fullscr, monitor=monitor,
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
    navig = dict(leftKeys='d', rightKeys = 'l', acceptKeys='space',
                 low=1, high=7, markerStart=4, markerColor='seagreen',
                 showValue=False, showAccept=False, pos=(0., 0.),
                 scale='Poczucie kontroli:', labels=['niskie', 'wysokie'],
                 noMouse = True)

    stim['rating scale'] = visual.RatingScale(window, **navig)

    if settings is not None:
        stim['trigger'] = Trigger(settings['port address'])

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


# show_trial could get Trigger from the outside as kwarg,
# else create one if None...
def show_trial(df, stim, trial, effect_colors=None, resp_clock=None,
               trigger=None, show_effect=True):
    if resp_clock is None:
        resp_clock = core.Clock()

    if trigger is None:
        trigger = Trigger()

    # get stimuli
    fix = stim['fix']
    window = stim['win']
    prime = stim[df.loc[trial, 'prime']]
    target = stim[df.loc[trial, 'target']]

    # set position
    prime.pos = (0., df.loc[trial, 'pos'])
    target.pos = (0., df.loc[trial, 'pos'])

    # show fixation
    trigger.set_sequence([0, 2], [100, 0])
    fix_frames = df.loc[trial, 'fixTime']
    show_stim(window=window, stimuli=fix, n_frames=fix_frames, trigger=trigger)

    # show prime
    trigger.set_sequence([0], [1])
    show_stim(window=window, stimuli=fix + [prime], n_frames=2,
              trigger=trigger)
    trigger.set_sequence([0], [0])
    show_stim(window=window, stimuli=fix, n_frames=4, trigger=trigger)

    # clear keybord buffer, show target
    event.getKeys()
    trigger.set_sequence([0, 2], [2, 0])
    show_stim(window=window, stimuli=fix + [target], n_frames=25,
              resp_clock=resp_clock, trigger=trigger)

    # get response
    keys = event.getKeys(keyList=['d', 'l'], timeStamped=resp_clock)
    # 1500 ms for response if not already given
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['d', 'l'], timeStamped=resp_clock,
                              maxWait=1.2)

    correct_frames = 0
    if keys is not None:
        # response trigger
        correct_frames = 2
        trigger.send(8)
        trigger.set_sequence([1], [0])
        show_stim(window=window, stimuli=None, n_frames=2)

    # evaluate repsonse
    eval_resp(df, trial, keys, effect_colors=effect_colors)
    if show_effect or not df.loc[trial, 'ifcorr']:
        circle = stim['circle'][df.loc[trial, 'effect']]
    else:
        circle = stim['circle']['grey']

    # delay 1 (jittered 40 - 60 frames)
    # high is 61 because randint upper limit is exclusive
    delay_frames = np.random.randint(low=40, high=61) - correct_frames
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'delay1'] = delay_frames

    # show effect
    trigger.set_sequence([0, 2], [4, 0])
    show_stim(window=window, stimuli=circle, n_frames=25, trigger=trigger)

    # delay 2 (jittered 75 - 125 frames); again high is exclusive
    delay_frames = np.random.randint(low=75, high=126)
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'delay2'] = delay_frames

    # rate sense of agency (TODO: set maxWait?)
    frame = 0
    trigger.set_sequence([0, 2], [16, 0])
    stim['rating scale'].reset()
    while stim['rating scale'].noResponse:
        stim['rating scale'].draw()
        window.flip()
        trigger.react_to_frame(frame)
        frame += 1

    # send response marker when rating scale finished
    trigger.send(8)
    trigger.set_sequence([1], [0])
    show_stim(window=window, stimuli=None, n_frames=2)

    # save responses to df
    df.loc[trial, 'soa_rating'] = stim['rating scale'].getRating()
    df.loc[trial, 'rating_RT'] = stim['rating scale'].getRT()

    # post-trial random interval, 25 - 75 frames
    delay_frames = np.random.randint(low=25, high=76) - 2
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'ITI'] = delay_frames


def prime_detection_task(df, stim, trial,  resp_clock=None, trigger=None):
    if resp_clock is None:
        resp_clock = core.Clock()

    if trigger is None:
        trigger = Trigger()

    # get stimuli
    fix = stim['fix']
    window = stim['win']
    if not pd.isnull(df.loc[trial, 'prime']):
        prime = stim[df.loc[trial, 'prime']]
        prime.pos = (0., df.loc[trial, 'pos'])
    else:
        prime = None
    target = stim[df.loc[trial, 'target']]

    # set position
    target.pos = (0., df.loc[trial, 'pos'])

    # show fixation
    trigger.set_sequence([0, 2], [100, 0])
    fix_frames = df.loc[trial, 'fixTime']
    show_stim(window=window, stimuli=fix, n_frames=fix_frames, trigger=trigger)

    # show prime
    trigger.set_sequence([0], [1])
    add_stim = [prime] if prime is not None else []
    show_stim(window=window, stimuli=fix + add_stim, n_frames=2,
              trigger=trigger)
    trigger.set_sequence([0], [0])
    show_stim(window=window, stimuli=fix, n_frames=4, trigger=trigger)

    # show target
    trigger.set_sequence([0, 2], [2, 0])
    show_stim(window=window, stimuli=fix + [target], n_frames=25,
              trigger=trigger)

    # delay 1 (60 frames)
    show_stim(window=window, stimuli=fix, n_frames=60)

    # clear keybord buffer & change fixation to signalise response window
    event.getKeys()
    for arm in fix:
        arm.setFillColor((1, -1, -1))
        arm.setLineColor((1, -1, -1))
    trigger.set_sequence([0, 2], [101, 0])
    show_stim(window=window, stimuli=fix, n_frames=3, trigger=trigger,
              resp_clock=resp_clock)

    # get response
    keys = event.getKeys(keyList=['d', 'l', 'space'], timeStamped=resp_clock)
    # 1500 ms for response if not already given
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['d', 'l', 'space'],
                              timeStamped=resp_clock, maxWait=1.2)

    for arm in fix:
        arm.setFillColor((1, 1, 1))
        arm.setLineColor((1, 1, 1))

    correct_frames = 0
    if keys is not None:
        # response trigger
        correct_frames = 2
        trigger.send(8)
        trigger.set_sequence([1], [0])
        show_stim(window=window, stimuli=fix, n_frames=2)

    # evaluate repsonse for prime detection
    eval_resp_prime(df, trial, keys)
    if df.loc[trial, 'resp'] == 'NoResp':
        show_stim(window=window, stimuli=stim['circle']['cross'], n_frames=25)

    # post-trial random interval, 25 - 75 frames
    delay_frames = np.random.randint(low=25, high=76) - correct_frames
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'ITI'] = delay_frames


def eval_resp_prime(df, trial, keys):
    correct_response = df.loc[trial, 'corrResp']
    if keys is None or len(keys) == 0:
        keys = 'NoResp'
        df.loc[trial, 'ifcorr'] = False
        df.loc[trial, 'effect'] = 'cross'
        df.loc[trial, 'resp'] = keys
        df.loc[trial, 'RT'] = np.nan
    else:
        key, key_time = keys[0]
        df.loc[trial, 'resp'] = key
        df.loc[trial, 'RT'] = key_time
        df.loc[trial, 'ifcorr'] = key == correct_response


def eval_resp(df, trial, keys, effect_colors=None):
    if keys is None or len(keys) == 0:
        keys = 'NoResp'
        df.loc[trial, 'ifcorr'] = False
        df.loc[trial, 'effect'] = 'cross'
        df.loc[trial, 'resp'] = keys
        df.loc[trial, 'RT'] = np.nan
    else:
        key, key_time = keys[0]
        df.loc[trial, 'resp'] = key
        df.loc[trial, 'RT'] = key_time
        df.loc[trial, 'ifcorr'] = key in df.loc[trial, 'corrResp']
        if not df.loc[trial, 'ifcorr']:
            df.loc[trial, 'effect'] = 'cross'
            if df.loc[trial, 'choiceType'] == 'Free':
                df.loc[trial, 'cond'] = 'XXX'
        else:
            used_hand = 'l' if key == 'd' else 'r'
            condition = 'c' if used_hand == df.loc[trial, 'prime'][6] else 'i'
            df.loc[trial, 'effect'] = effect_colors[used_hand + condition]
            if df.loc[trial, 'choiceType'] == 'Free':
                df.loc[trial, 'cond'] = 'comp' if condition == 'c' else 'incomp'
    # if incorrect response add this trial type to the end of the df
    if not df.loc[trial, 'ifcorr']:
        last_index = df.index[-1]
        df.loc[last_index + 1, :] = df.loc[trial, :]
        # ARGH, fuck, pandas, why?!
        df = ensure_dtypes(df)


def show_break(window):
    # TODO add info about how many trials passed, which block it is ...?
    event.getKeys()
    break_text = u'To jest ekran przerwy\n\nAby przejść dalej\nnaciśnij spację'
    text = visual.TextStim(window, text=break_text)
    text.draw()
    window.flip()

    # wait for space or for quit
    keys = event.waitKeys(keyList=['q', 'space'])
    check_quit(keys)

    # TODO random wait after break?


def run_block(block_df, stim, break_every=15, n_trials=None,
              effect_colors=None, trigger=None, show_effect=None,
              prime_det=False, settings=None, suffix='_data.csv'):
    # set dataframe file name
    fname = 'SoA_{}_{}'.format(
        settings['subject group'], settings['subject name']) + suffix
    fname = os.path.join(settings['data dir'], fname)

    # set trials to use
    max_trials = block_df.shape[0]
    n_trials = max_trials if n_trials is None else n_trials
    all_trials = block_df.index[:min(n_trials, max_trials)]

    for trial in all_trials:
        if not prime_det:
            show_trial(block_df, stim, trial, effect_colors=effect_colors,
                       trigger=trigger, show_effect=show_effect)
        else:
            prime_detection_task(block_df, stim, trial, trigger=trigger)

        # write data after every trial TODO CHECK IF CORRECT
        t0 = time.clock()
        block_df.to_csv(fname)
        t1 = time.clock()
        block_df.loc[trial, 'saveTime'] = t1 - t0

        if (trial) % break_every == 0:
            show_break(stim['win'])


def check_quit(keys=None):
    if keys is None:
        event.getKeys(keyList=['q'])
    if 'q' in keys:
        core.quit()


class Instructions:
	def __init__(self, win, instrfiles):
		self.win = win
		self.nextpage   = 0
		self.navigation = {'d': 'prev', 'l': 'next'}

		# get instructions from file:
		self.imagefiles = instrfiles
		self.images = []
		self.generate_images()
		self.stop_at_page = len(self.images)

	def generate_images(self):
		self.images = []
		for imfl in self.imagefiles:
			if not isinstance(imfl, types.FunctionType):
				self.images.append(visual.ImageStim(self.win,
					image=imfl, size=[1366, 768], units='pix',
					interpolate=True))
			else:
				self.images.append(imfl)

	def present(self, start=None, stop=None):
		if not isinstance(start, int):
			start = self.nextpage
		if not isinstance(stop, int):
			stop = len(self.images)

		# show pages:
		self.nextpage = start
		while self.nextpage < stop:
			# create page elements
			action = self.show_page()

			# go next/prev according to the response
			if action == 'next':
				self.nextpage += 1
			else:
				self.nextpage = max(0, self.nextpage - 1)

	def show_page(self, page_num=None):
		if not isinstance(page_num, int):
			page_num = self.nextpage

		img = self.images[page_num]
		if not isinstance(img, types.FunctionType):
			img.draw()
			self.win.flip()

			# wait for response
			k = event.waitKeys(keyList=self.navigation.keys())[0]
			return self.navigation[k]
		else:
			img()
			return 'next'


def subject_id_gui():
    myDlg = gui.Dlg(title="Poczucie kontroli - badanie")
    myDlg.addText('Subject info')
    myDlg.addField('ID:')
    myDlg.addField('Group:')
    myDlg.show()
    if myDlg.OK:
        return myDlg.data
    else:
        core.quit()


class ArrowStim(object):
    def __init__(self, window, razor_width=1., razor_height=0.8,
                 razor_sharpness=0.15, arrow_width=2., arrow_height=1.6,
                 arrow_sharpness=0.5, arrow_color='white', razor_color='black',
                 pos=(0, 0)):

        pos_array = np.array(pos)[np.newaxis, :]
        jigjag = np.array([1, -1, 1, -1, 1])
        razor_x_pos_right = razor_width + jigjag * razor_sharpness
        razor_x_pos_left = razor_x_pos_right * -1
        y_pos = np.linspace(razor_height, -razor_height, num=5)

        full_x = np.concatenate([razor_x_pos_right, razor_x_pos_left[::-1]])
        full_y = np.concatenate([y_pos, y_pos[::-1]])
        razor_vertices = np.stack([full_x, full_y], axis=1)

        razor_shape = visual.ShapeStim(window, vertices=razor_vertices)
        razor_shape.setFillColor(razor_color)
        razor_shape.setLineColor(razor_color)

        arrow_xpos = arrow_width * np.array([1., 1., 1., -1., -1.])
        arrow_xpos[1] += arrow_sharpness
        arrow_ypos = np.concatenate(
            [np.linspace(arrow_height, -arrow_height, num=3),
             np.linspace(-arrow_height, arrow_height, num=2)])
        arrow_vertices = np.stack([arrow_xpos, arrow_ypos], axis=1)
        arrow_vertices += pos_array
        arrow_shape = visual.ShapeStim(window, vertices=arrow_vertices)
        arrow_shape.setFillColor(arrow_color)
        arrow_shape.setLineColor(arrow_color)

        self.window = window
        self.arrow_color = arrow_color
        self.razor_color = razor_color
        self.arrow_vertices = arrow_vertices
        self.razor_vertices = razor_vertices
        self.arrow = arrow_shape
        self.razor = razor_shape

    def draw(self):
        self.arrow.draw()
        self.razor.draw()

    def setPos(self, pos):
        # even this doesn't work... (shape still gets messed up)
        pos_array = np.asarray(pos)[np.newaxis, :]
        arrow_shape = visual.ShapeStim(
            self.window, vertices=np.array(self.arrow_vertices) + pos_array)
        arrow_shape.setFillColor(self.arrow_color)
        arrow_shape.setLineColor(self.arrow_color)
        self.arrow = arrow_shape

        razor_shape = visual.ShapeStim(
            self.window, vertices=np.array(self.razor_vertices) + pos_array)
        razor_shape.setFillColor(self.razor_color)
        razor_shape.setLineColor(self.razor_color)
        self.razor = razor_shape
