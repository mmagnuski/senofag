from psychopy import core, visual, event, monitors
import numpy as np
from os import path as op

####################################################

stim_dir = lambda pth : op.join('pic', pth)

win = visual.Window((1200,1000), fullscr=False, monitor='testMonitor', units='deg', color='black') # MUST BE CHANGED (E.G. TO A DEFAULT ONE)

def circle(win, col='green', pos=(0,0), r=2.5):
    circ = visual.Circle(win, pos=pos, radius=r, edges=128,
      units='deg', interpolate=True)
    circ.setFillColor(col)
    circ.setLineColor(col)
    return circ

# a list of stimuli images:
stim = dict()
stim['win'] = win
stim['target_left.png'] = visual.ImageStim(
    win=win, image=stim_dir('target_left.png'))
stim['target_right.png'] = visual.ImageStim(
    win=win, image=stim_dir('target_right.png'))
stim['target_both.png'] = visual.ImageStim(
    win=win, image=stim_dir('target_both.png'))

# a list of primes images:
stim['prime_left.png'] = visual.ImageStim(
    win=win, image=stim_dir('prime_left.png'))
stim['prime_right.png'] = visual.ImageStim(
    win=win, image=stim_dir('prime_right.png'))

# a list of colors images:
colors = ['grey', 'blue', 'red', 'green', 'yellow']
stim['circle'] = {c: circle(win, col=c) for c in colors}
stim['circle']['cross'] = visual.ImageStim(win, image=stim_dir('cross.png'))

def whiteshape(v, win = win):      
    return visual.ShapeStim(win,        
       lineWidth  = 0.5,
       fillColor  = [1, 1, 1],     
       lineColor  = [1, 1, 1],     
       vertices   = v,
       closeShape = True
       )

# create fixation cross:       
def fix(ln=1, lw=0.1):
    hlw = lw/2
    v = np.array([
               [hlw, -ln],
               [hlw, ln],
               [-hlw, ln],
               [-hlw, -ln] ])

    fix = []
    fix.append(whiteshape(v))
    fix.append(whiteshape(      
       np.fliplr(v)        
       ))      
    return fix

stim['fix'] = fix()

def show_trial(df, stim, tri):
    # show fixation
    fix_frames = df.loc[tri, 'fixTime']
    for f in stim['fix']:
        f.autoDraw = True

    for _ in range(fix_frames):
        stim['win'].flip()

    # show prime
    stim[df.loc[tri, 'prime']].draw()
    stim['win'].flip()

    # show target
    event.getKeys()
    for _ in range(25):
        stim[df.loc[tri, 'target']].draw()
        stim['win'].flip()

    # 1500 ms for response
    for _ in range(150):
        k = event.getKeys()
        if k:
            break
        stim['win'].flip()

    for f in stim['fix']:
        f.autoDraw = False

    for _ in range(30):
        stim['circle'][df.loc[tri, 'effect']].draw()
        stim['win'].flip()
        



