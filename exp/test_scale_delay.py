# coding: utf-8

from psychopy import visual, event


win = visual.Window(monitor='testMonitor')
txt = visual.TextStim(win, text=u'Dupa kościotrupa!')
scale = visual.RatingScale(win, leftKeys='d', rightKeys = 'l',
                           acceptKeys='space', noMouse=True,
                           markerStart=3)

for i in range(3):
    txt.draw()
    win.flip()
    event.waitKeys()
    
    scale.reset()
    while scale.noResponse:
        scale.draw()
        win.flip()
