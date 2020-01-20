#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging, parallel
from time import strftime
from random import choice
from numpy.random import choice as choice2
import numpy.random as rd
import numpy as np
import random
import pandas as pd

# parallel_port
#port = parallel.ParallelPort(0x1FF8)

#Experimenter input
dlg = gui.Dlg(title = 'Resting State')
dlg.addField('Duration in sec:')
exp_input = dlg.show()

duration_sec = int(exp_input[0])
duration_frames = duration_sec * 60
#window
win = visual.Window(size=[800, 600], color=[-1,-1,-1], screen = 0, fullscr = True)
win.setMouseVisible(False)
aspect = float(win.size[1])/float(win.size[0])
print(aspect)
stim_size = .06
stim_width = stim_size
stim_height = stim_size/aspect
fontsize = 0.055
wrapwidth = 80
#Shapes

#Fixation
fixation = visual.ShapeStim(
				win=win, name='polygon', vertices='cross',
			    size=(stim_width/1.5, stim_height/1.5),
			    ori=0, pos=(0, 0),
			    fillColor=[1,1,1], fillColorSpace='rgb',
				lineColor = [-1,-1,-1],
			    opacity=1, depth=0.0, interpolate=True)


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


for frames in range(duration_frames):
    #if frames == 1:
    # 	win.callOnFlip(port.setData, int("00000001", 2))
    fixation.draw()
    win.flip()
