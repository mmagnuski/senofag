# stim tests
from psychopy import visual, event, core
from stim import stim

# present objects
# ---------------
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

stim['win'].flip()
event.waitKeys()


#######################
# present target/prime flipping

clock = core.Clock()
keepLooping = True
for img in ['tleft', 'pleft']:
    stim[img].draw()
    stim['win'].flip()
    k = []
    while not k:
        k = event.getKeys(keyList=['space', 'escape'])
