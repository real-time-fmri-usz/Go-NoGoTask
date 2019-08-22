#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging
from time import strftime
from random import choice
from numpy.random import choice as choice2
import numpy.random as rd
import numpy as np
import random
import csv
import pandas
import matplotlib
import matplotlib.pyplot as plt
import os


##### SETUP #####

### Parameters ###

###### EDIT PARAMETERS BELOW #######

num_trials_cue = 50        # number of trials in the experiment on target side
num_trials_catch = 10
num_trials_total = num_trials_cue + num_trials_catch
initialStim_dur = 1     # in frames
blank_dur = 2        # time a blank screen between stim and mask is on screen [strong,weak,catch]
initialMask_dur = 12 #12     # time the mask appears on the screen [strong,weak,catch]     # The stepsize for the staircase procedure
response_dur = 90 #90              # time the response period stays on the screen
iti_durs = [30,60]  # time with no no image present between trials
fontsize = 0.06
wrapwidth = 80

stim_size = .06             #size of the stimulus on screen
mask_size_ratio = 1.6         #how much proptionally bigger is mask
#stim_line_width =  200      # width of diamond frame lines
blocker_size = .12         #size of black boxes the mask the edge of the stimulus (pick a value between 0 and 1. 0 blocks nothing, 1 blocks a whole half)
response_keys = {'left':'b','right':'z'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','z']
pix_size = .001

practice_iti_dur = 2
practice_stim_dur = .3
practice_blank_dur = .033
practice_mask_dur = .3


###### STOP EDITING BELOW THIS LINE #######


#Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addField('Subject ID:')
dlg.addField('Session:')
dlg.addField('Scanner', choices = ['yes','no'])
dlg.addField('Version:', choices = ['oddball'])
dlg.addField('Language', choices = ['en', 'de'])
exp_input = dlg.show()

subid = exp_input[0]
session = exp_input[1]
if exp_input[2] == 'yes':
	scanner = True
else:
	scanner = False
version = exp_input[3]
language = exp_input[4]

#get shuffled list of trials
trial_states = {}
n = 0
for i in range(int(num_trials_cue)):
	n+=1
	trial_states[n] = {'target':'left'}
	n+=1
	trial_states[n] = {'target':'right'}

for i in range(int(num_trials_catch)):
	n+=1
	trial_states[n] = {'target': 'catch'}


trial_order = list(range(1,(1+num_trials_cue+num_trials_catch)))
random.shuffle(trial_order)


### Visuals ###

#window
win = visual.Window(size=[800, 600], color=[-1,-1,-1], screen = 0, fullscr = False)
win.setMouseVisible(False)
aspect = float(win.size[1])/float(win.size[0])
print(aspect)
stim_width = stim_size
stim_height = stim_size/aspect
#Shapes
mask = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width*mask_size_ratio, 0), (0, stim_height*mask_size_ratio), (stim_width*mask_size_ratio, 0), (0,-1*stim_height*mask_size_ratio)))
white_diamond = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width, 0), (0, stim_height), (stim_width, 0), (0,-1*stim_height)))
black_diamond = visual.ShapeStim(win, lineColor='black', fillColor='black', vertices=((-1*stim_width-pix_size, 0), (0, stim_height+pix_size), (stim_width+pix_size, 0), (0,-1*stim_height-pix_size)))
blockers = {'left':  visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, stim_height), (-1, -1*stim_height), (-1*stim_width+stim_width*blocker_size, stim_height), (-1*stim_width+stim_width*blocker_size, -1*stim_height))),
			'right': visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((1, stim_height), (1, -1*stim_height), (stim_width-stim_width*blocker_size, stim_height), (stim_width-stim_width*blocker_size, -1*stim_height))),
			'top':   visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, 1), (1, 1), (-1,stim_height-stim_size*blocker_size), (1,stim_height-stim_height*blocker_size))),
			'bottom':visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, -1), (1, -1), (-1,-1*stim_height+stim_height*blocker_size), (1,-1*stim_height+stim_height*blocker_size)))
			}


#Fixation
fixation = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(stim_width, stim_height),
    ori=0, pos=(0, 0),
    fillColor=[1,1,1], fillColorSpace='rgb',
    lineColor = [-1,-1,-1],
	opacity=1, depth=0.0, interpolate=True)
###text
#headers
instructions_header = visual.TextStim(win, text='INSTRUCTIONS', font = 'Arial', color = 'white', alignHoriz = 'center', pos=(0.0,.8))
experiment_header = visual.TextStim(win, text='MAIN EXPERIMENT', font = 'Arial', color = 'white', alignHoriz = 'center', pos=(0.0,.8))



get_ready_text =  visual.TextStim(win, text='Get ready . . .',
					  					height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))



### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()




### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


##### RUN EXPERIMENT #####

###  instructions  ###
#explain task


get_ready_text.draw()
win.flip()
event.waitKeys(keyList='space')


### Main Experiment ###servicde
#clock reset
win.flip()
elapse_time = 0
last_trial_dur = 0

#trigger scanner
if scanner:
	#port.write(chr(np.uint8(128+32+64+1)))
    event.waitKeys(keyList=['t'])

experiment_clock.reset()

mask_dur = initialMask_dur
stim_dur = initialStim_dur

trial = 0
for shuffled_trial in trial_order:
	trial += 1
	iti_dur = choice(iti_durs)
	target_side = trial_states[shuffled_trial]['target']
	if (target_side == 'left'):
		side = 'left'
	elif (target_side == 'right'):
		side = 'right'
	else:
		side = 'catch'

	elapse_time += last_trial_dur
	iti_onset = elapse_time
	stim_onset = elapse_time + iti_dur
	blank_onset = elapse_time + iti_dur + stim_dur
	mask_onset = elapse_time + iti_dur + stim_dur + blank_dur
	response_onset = elapse_time + iti_dur + stim_dur  + blank_dur + mask_dur

	# iti presentation
	#Add the Parallelport stuff here -> see parallel_port.py
	for s in range(int(iti_dur)):
		fixation.draw()
		win.flip()
	#stim presentation
	start_stimulus = experiment_clock.getTime()
	for i in range(int(stim_dur)):
		if not side == 'catch':
			white_diamond.draw()
			blockers[side].draw()
		win.flip()
	presentation_duration = experiment_clock.getTime() - start_stimulus
	#blank presentation
	for m in range(int(blank_dur)):
		win.flip()
	# mask presentation
	responded = False
	response = []
	event.clearEvents(eventType=None)
	start_response = experiment_clock.getTime()
	for rr in range(int(response_dur)):
		if rr < mask_dur:
			mask.draw()
			black_diamond.draw()
		else:
			#fixation.draw()
			black_diamond.draw()
		win.flip()

	#timing update
	last_trial_dur = iti_dur + stim_dur + blank_dur + mask_dur + response_dur






win.close()
