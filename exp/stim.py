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
    image_size = np.array(img.size)
    image_size = np.round(image_size * scale).astype('int')
    return visual.ImageStim(win=win, image=image, units='pix',
                            size=image_size, **kwargs)


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


def show_trial(df, stim, trial, effect_colors=None, resp_clock=None):
    if resp_clock is None:
        resp_clock = core.Clock()

    # set pos
    stim[df.loc[trial, 'prime']].pos = (0., df.loc[trial, 'pos'])
    stim[df.loc[trial, 'target']].pos = (0., df.loc[trial, 'pos'])

    # show fixation
    fix_frames = df.loc[trial, 'fixTime']

    for f in stim['fix']:
        f.autoDraw = True

    for _ in range(fix_frames):
        stim['win'].flip()

    # show prime
    stim[df.loc[trial, 'prime']].draw()
    stim['win'].flip()

    # clear keybord buffer, show target
    event.getKeys()
    for frame in range(25):
        stim[df.loc[trial, 'target']].draw()
        stim['win'].flip()
        if frame == 0:
            resp_clock.reset()

    keys = event.getKeys(keyList=['f', 'j'], timeStamped=resp_clock)
    if keys is None or len(keys) == 0:
        # 1500 ms for response if not already given
        keys = event.waitKeys(keyList=['f', 'j'], timeStamped=resp_clock,
                              maxWait=1.5)

    for f in stim['fix']:
        f.autoDraw = False

    # evaluate repsonse
    eval_resp(df, trial, keys, effect_colors=effect_colors)

    # show effect
    for _ in range(30):
        stim['circle'][df.loc[trial, 'effect']].draw()
        stim['win'].flip()

    # rate sense of agency
    stim['rating scale'].reset()
    while stim['rating scale'].noResponse:
        stim['rating scale'].draw()
        stim['win'].flip()

    # save responses to df
    df.loc[trial, 'soa_rating'] = stim['rating scale'].getRating()
    df.loc[trial, 'rating_RT'] = stim['rating scale'].getRT()

    # post-trial random interval?


def eval_resp(df, trial, keys, effect_colors=None):
    if len(keys) == 0:
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


class Instructions:
	def __init__(self, win, instrfiles):
		self.win = win
		self.nextpage   = 0
		self.navigation = {'left': 'prev', 'right': 'next',
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
					image=imfl, size=[1169, 826], units='pix',
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
