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

##### SETUP #####

#Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addField('Subject ID:')

exp_input = dlg.show()

#port = parallel.ParallelPort(0x1FF8)
### Parameters ###

###### EDIT PARAMETERS BELOW #######

stim_dur = {'strong':1}     # time in seconds that the subliminal stim appears on the screen [strong,weak,catch]
blank_dur = {'strong':2}        # time a blank screen between stim and mask is on screen [strong,weak,catch]
mask_dur = {'strong':12}     # time the mask appears on the screen [strong,weak,catch]

response_dur = 90 #Do we need it here?
fixation_dur = 12			# fixation before stimulus_strength
blank_dur_pre = 3
#strength_prob = [.5,.5]   # probability of the trial being strong or weak
stim_size = .06             #size of the stimulus on screen
mask_size_ratio = 1.6         #how much proptionally bigger is mask
#stim_line_width =  200      # width of diamond frame lines
blocker_size = .15         #size of black boxes the mask the edge of the stimulus (pick a value between 0 and 1. 0 blocks nothing, 1 blocks a whole half)
response_keys = {'left':'b','right':'z'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','z']
pix_size = .001

subid = exp_input[0]
00
#window
win = visual.Window(size=[800, 600], color=[-1,-1,-1], screen = 0, fullscr = False, allowStencil = True)
win.setMouseVisible(False)
aspect = float(win.size[1])/float(win.size[0])
width_ratio = float(win.size[0])/800
height_ratio = float(win.size[1])/600
print(width_ratio)
print(height_ratio)
stim_width = stim_size
stim_height = stim_size/aspect
fontsize = 0.055
wrapwidth = 80
#Shapes
#mask = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width*mask_size_ratio, 0), (0, stim_height*mask_size_ratio), (stim_width*mask_size_ratio, 0), (0,-1*stim_height*mask_size_ratio)))
mask = visual.Rect(win, lineColor='white', fillColor='white', width = 2*stim_width*1.6, height = 2*stim_height*1.6)
black_square = visual.Rect(win, lineColor='black', fillColor='black', width = 2*stim_width, height = 2*stim_height)


white_diamond = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width, 0), (0, stim_height), (stim_width, 0), (0,-1*stim_height)))
black_diamond = visual.ShapeStim(win, lineColor='black', fillColor='black', vertices=((-1*stim_width-pix_size, 0), (0, stim_height+pix_size), (stim_width+pix_size, 0), (0,-1*stim_height-pix_size)))
blockers = {'left':  visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, stim_height), (-1, -1*stim_height), (-1*stim_width+stim_width*blocker_size, stim_height), (-1*stim_width+stim_width*blocker_size, -1*stim_height))),
			'right': visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((1, stim_height), (1, -1*stim_height), (stim_width-stim_width*blocker_size, stim_height), (stim_width-stim_width*blocker_size, -1*stim_height))),
			'top':   visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, 1), (1, 1), (-1,stim_height-stim_size*blocker_size), (1,stim_height-stim_height*blocker_size))),
			'bottom':visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, -1), (1, -1), (-1,-1*stim_height+stim_height*blocker_size), (1,-1*stim_height+stim_height*blocker_size)))
			}

#apert = visual.Aperture(win, size=1, pos=(0, 0), ori=0, nVert=120, shape=((-1*stim_width, 0), (0, stim_height), (stim_width, 0), (0,-1*stim_height)), inverted=False, units=None, name=None, autoLog=None)
aperture = visual.Aperture(win,	size = 1, shape= ((-1*stim_width, 1*stim_height), (-1*stim_width, -1*stim_height), (stim_width, -1*stim_height), (stim_width,1*stim_height)))
aperture.enabled = False
#maskNoise = visual.ImageStim(win, image = 'maskNoise.png', size = [stim_width*mask_size_ratio*width_ratio, stim_height*mask_size_ratio*height_ratio])
noise = visual.ImageStim(win, image = 'testnoise.png')
#Fixation
fixation = visual.ShapeStim(
				win=win, name='polygon', vertices='cross',
			    size=(stim_width/1.5, stim_height/1.5),
			    ori=0, pos=(0, 0),
			    fillColor=[1,1,1], fillColorSpace='rgb',
				lineColor = [-1,-1,-1],
			    opacity=1, depth=0.0, interpolate=True)


# left or right?

left_right = visual.TextStim(win, text='LEFT OR RIGHT?', font = 'Arial', color = 'white', alignHoriz = 'center', pos=(0.0,0.0))


### Timing ###

experiment_clock = core.Clock()

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_subliminal_test.csv'%(subid)
output_file = open(output_file_path,'w+')
output_file.write('subid,trial,side,response,correct,response_time\n')
output_file.flush()


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)

#clock reset
win.flip()
elapse_time = 0
last_trial_dur = 0


event.waitKeys(keyList=['t'])

experiment_clock.reset()

# Create a list of blocks and shuffle them
block_list = [1,2,3,4]

trials = ['left', 'right'] * 24
random.shuffle(trials)


for trial in range(len(trials)):
	side = trials[trial]
	for s in range(int(fixation_dur)):
		fixation.draw()
		win.flip()

	for p in range(int(blank_dur_pre)):
		win.flip()

	for stim in range(int(stim_dur['strong'])):
		white_diamond.draw()
		blockers[side].draw()
		win.flip()

	for m in range(int(blank_dur['strong'])):
		win.flip()

	responded = False
	response = []
	event.clearEvents(eventType=None)
	start_response = experiment_clock.getTime()
	for rr in range(int(mask_dur['strong'])):
		mask.draw()
		#black_square.draw()
		aperture.enabled = True
		noise.draw()
		#black_diamond.draw()
		win.flip()
		aperture.enabled = False
	for tt in range(int(blank_dur['strong'])):
		win.flip()

	while responded == False:
		left_right.draw()

		win.flip()
		response = event.getKeys(keyList=reskeys_list, timeStamped=True)
		if len(response) > 0:
			responded = True
			cumulative_response_time = round(experiment_clock.getTime(),3)
			response_time = round(experiment_clock.getTime() - start_response,3)
			sub_response = response_keys_inv[response[0][0]]
			if sub_response == side:
				correct = 1
			else:
				correct = 0

			output_file.write(','.join([str(subid),str(trial+1),str(side),str(sub_response),str(correct),str(response_time)+'\n']))
			output_file.flush()
