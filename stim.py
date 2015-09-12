from psychopy import core, visual, event, monitors
import os

PTH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PTH)

####################################################

win = visual.Window((1200,1000), fullscr=False, monitor='testMonitor', units='deg', color='black') # MUST BE CHANGED (E.G. TO A DEFAULT ONE)

# a list of stimuli images:
stim = dict()
stim['tleft'] = visual.ImageStim(win=win, image='target_left.png')
stim['tright'] = visual.ImageStim(win=win, image='target_right.png')
stim['tboth'] = visual.ImageStim(win=win, image='target_both.png')

# a list of primes images:
stim['pleft'] = visual.ImageStim(win=win, image='prime_left.png')
stim['pright'] = visual.ImageStim(win=win, image='prime_right.png')

# a list of colors images:
names = ['example', 'blue', 'red', 'green', 'purple', 'orange', 'yellow']
stim['circle'] = {k: visual.ImageStim(win, image='color_{}.png'.format(k)) for k in names}
stim['circle']['grey'] = visual.ImageStim(win, image='grey.png')



#######################
#######################
'''
# TESTS:

#######################
# present objects
print "cyellow original size = ", stim['circle']['yellow'].size
stim['circle']['yellow'].pos = [-10, 0]
stim['circle']['yellow'].draw()
stim['circle']['yellow'].pos = [0, -10]
stim['circle']['yellow'].size = [3, 3] # image scaled to 3 * 3 degrees of the visual angle (?)
stim['circle']['yellow'].draw()
print "prime left original size = ", stim['pleft'].size
print "target left original size = ", stim['tleft'].size

stim['pleft'].size *= 0.333
stim['tleft'].size *= 0.333
print "prime left new size = ", stim['pleft'].size
print "target left new size = ", stim['tleft'].size

win.flip()
event.waitKeys()


#######################
# present target/prime flipping

clock = core.Clock()
keepLooping = True
while keepLooping:
    for img in ['tleft', 'pleft']:
        if keepLooping:
            for frameN in range(1):
                stim[img].draw()
                win.flip()
                keys = event.getKeys(keyList=['space', 'escape'])
                if keys:
                    rt = clock.getTime()
                    keepLooping = False
                    print "rt = ", rt
                    break
'''