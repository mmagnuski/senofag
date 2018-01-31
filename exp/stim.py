# encoding: utf-8

import os
from os import path as op
import types
from PIL import Image

import numpy as np
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


def create_stimuli(fullscr=False, settings=None):
    window = visual.Window(fullscr=fullscr, monitor='testMonitor',
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
                 scale='', labels=['niskie', 'wysokie'], noMouse = True)

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
               trigger=None):
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

    # response trigger
    trigger.set_sequence([0], [8])
    trigger.react_to_frame(0)
    trigger.set_sequence([1], [0])
    show_stim(window=window, stimuli=None, n_frames=2)

    # evaluate repsonse
    eval_resp(df, trial, keys, effect_colors=effect_colors)
    circle = stim['circle'][df.loc[trial, 'effect']]

    # delay 1 (jittered 40 - 60 frames)
    # high is 61 because randint upper limit is exclusive
    delay_frames = np.random.randint(low=40, high=61) - 2
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
        check_quit()
        stim['rating scale'].draw()
        window.flip()
        trigger.react_to_frame(frame)
        frame += 1

    # send response marker when rating scale finished
    trigger.set_sequence([0], [8])
    trigger.react_to_frame(0)
    trigger.set_sequence([1], [0])
    show_stim(window=window, stimuli=None, n_frames=2)

    # save responses to df
    df.loc[trial, 'soa_rating'] = stim['rating scale'].getRating()
    df.loc[trial, 'rating_RT'] = stim['rating scale'].getRT()

    # post-trial random interval, 25 - 75 frames
    delay_frames = np.random.randint(low=25, high=76) - 2
    show_stim(window=window, stimuli=None, n_frames=delay_frames)
    df.loc[trial, 'ITI'] = delay_frames


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
    text = visual.TextStim(window, text=u'Aby przejść dalej\nnaciśnij spację')
    text.draw()
    window.flip()

    # wait for space
    keys = event.getKeys(keyList=['space'])
    # 1500 ms for response if not already given
    if keys is None or len(keys) == 0:
        keys = event.waitKeys(keyList=['space'])

    # TODO random wait after break


def run_block(block_df, stim, block_num=0, break_every=15, effect_colors=None,
              trigger=None, settings=None):
    trial = 1
    suffix = '_block_{}.csv'.format(block_num)
    fname = os.path.join(settings['data dir'],
                         settings['subject name'] + suffix)
    while trial <= block_df.index[-1]:
        show_trial(block_df, stim, trial, effect_colors=effect_colors,
                   trigger=trigger)

        # write data after every trial
        # (TODO: include save time in between-trial interval)
        block_df.to_csv(fname)

        if (trial + 1) % break_every == 0:
            show_break(stim['win'])
        trial += 1


def check_quit():
    if 'q' in event.getKeys(keyList=['q']):
        core.quit()


class Instructions:
	def __init__(self, win, instrfiles):
		self.win = win
		self.nextpage   = 0
		self.navigation = {'d': 'prev', 'l': 'next',
			'space': 'next'}

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
    myDlg = gui.Dlg(title="Senofag")
    myDlg.addText('Subject info')
    myDlg.addField('ID:')
    myDlg.show()
    if myDlg.OK:
        return myDlg.data[0]
    else:
        core.quit()
