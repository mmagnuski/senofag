from psychopy import visual, event, core

win = visual.Window()
circ = visual.Circle(win)
circ.setFillColor("pink")
circ.draw()
win.flip()

event.waitKeys()
core.quit()