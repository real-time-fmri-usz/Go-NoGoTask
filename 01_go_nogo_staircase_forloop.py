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

num_trials = 100        # number of trials in the experiment on target side
initialStim_dur = 12     # in frames
blank_dur = 2        # time a blank screen between stim and mask is on screen [strong,weak,catch]
initialMask_dur = 1 #12     # time the mask appears on the screen [strong,weak,catch]
stepsize = 2     # The stepsize for the staircase procedure
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
dlg.addField('Practice', choices = ['yes','no'])
dlg.addField('Language', choices = ['en', 'de'])
exp_input = dlg.show()

subid = exp_input[0]
session = exp_input[1]
if exp_input[2] == 'yes':
	scanner = True
else:
	scanner = False
version = exp_input[3]
if exp_input[4] == 'yes':
	show_practice = True
else:
	show_practice = False

language = exp_input[5]

#get shuffled list of trials
trial_states = {}
n = 0
for i in range(int(num_trials)):
	n+=1
	trial_states[n] = {'target':'left'}
	n+=1
	trial_states[n] = {'target':'right'}

trial_order = list(range(1,(1+num_trials)))
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


left_example = visual.ImageStim(
					win=win,
					image="left_diamond.png",
					units="pix",
					pos=[-150,-50])
right_example = visual.ImageStim(
					win=win,
					image="right_diamond.png",
					units="pix",
					pos=[150,-50])

frame_example = visual.ImageStim(
	win=win,
	image="mask.png",
	units="pix",
	pos=[0,-50])



#Create instructions depending on the language

if language == 'en':

	#instructions_en
	instructions_text1 = visual.TextStim(win, text='In each trial of this experiment a diamond shape will appear in the middle of the screen',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text2 = visual.TextStim(win, text='It will have a point missing from its left side or its right side.',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text3 = visual.TextStim(win, text='left side missing                 right side missing',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.5))

	instructions_text4 = visual.TextStim(win, text='The diamond will be followed immediately by a frame shape.',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.2))

	instructions_text5 = visual.TextStim(win, text='Press the "%s" key if the frame is preceded by a diamond missing a point on its %s side.'%('left','left'),
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.0))

	instructions_text6 = visual.TextStim(win, text='Press the "%s" key if the frame is preceded by a diamond missing a point on its %s side.'%('right','right'),
										height = fontsize,
										color = 'white',
										font = 'Arial',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))

	instructions_text7 = visual.TextStim(win, text='Trials where you have to press a button will be more frequent!',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))

	instructions_text8 = visual.TextStim(win, text='please keep this in mind when making your response.',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.2))



	instructions2_text = [visual.TextStim(win, text='Great job!',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.1)),
						visual.TextStim(win, text='In the real experiment you will only have %s seconds to respond.'%(round(response_dur*0.0167,1)),
						height = fontsize,
						font = 'Arial',
						color = 'white',
						alignHoriz = 'center',
						alignVert = 'center',
						pos=(0.0,0.0))]

	#mis
	example_text = visual.TextStim(win, text='Here are some practice examples . . .',
									font = 'Arial',
									height = fontsize,
									color = 'white',
									alignHoriz = 'center',
									alignVert = 'center',
									pos=(0.0,0.0))

	get_ready_text = [visual.TextStim(win, text='Now let\'s move on the the real experiment.',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.0)),
					  visual.TextStim(win, text='Get ready . . .',
					  					height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))]

	press_left_text = visual.TextStim(win, text='Press the left key',
										height = 0.075,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

	press_right_text = visual.TextStim(win, text='Press the right key',
	 									color = 'white',
										font = 'Arial',
										height = 0.075,
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

	press_nothing_text = visual.TextStim(win, text='Press nothing',
										color = 'white',
										font = 'Arial',
										height = 0.075,
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

else:
	#instructions_de
	instructions_text1 = visual.TextStim(win, text='In jedem Durchgang wird eine Diamantenform in der Mitte des Bildschirms erscheinen.',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text2 = visual.TextStim(win, text='Der Diamant wird entweder links oder rechts abgeschnitten sein.',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text3 = visual.TextStim(win, text='Linke Seite abgeschnitten                 Rechte Seite abgeschnitten',
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.5))

	instructions_text4 = visual.TextStim(win, text='Auf diesen Diamant wird jeweils ein schwarzer Diamant mit Rahmen folgen.',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.2))

	instructions_text5 = visual.TextStim(win, text='Drücke die "%s" Taste, wenn dem Diamanten vorher die %s Seite gefehlt hat!'%('linke','linke'),
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.0))

	instructions_text6 = visual.TextStim(win, text='Drücke die "%s" Taste, wenn dem Diamanten vorher die %s Seite gefehlt hat!'%('rechte','rechte'),
										height = fontsize,
										color = 'white',
										font = 'Arial',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))

	instructions_text7 = visual.TextStim(win, text='Durchgänge, in denen du eine Taste drücken musst, sind häufiger!',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))

	instructions_text8 = visual.TextStim(win, text='Bitte denke daran, wenn du antwortest.',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.2))



	instructions2_text = [visual.TextStim(win, text='Gut gemacht!',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.1)),
						visual.TextStim(win, text='Im Hauptexperiment wirst du nur %s Sekunden für deine Antwort haben.'%(round(response_dur*0.0167,1)),
						height = fontsize,
						font = 'Arial',
						color = 'white',
						alignHoriz = 'center',
						alignVert = 'center',
						pos=(0.0,0.0))]

	#mis
	example_text = visual.TextStim(win, text='Hier sind ein paar Übungsdurchgänge...',
									font = 'Arial',
									height = fontsize,
									color = 'white',
									alignHoriz = 'center',
									alignVert = 'center',
									pos=(0.0,0.0))

	get_ready_text = [visual.TextStim(win, text='Nun folgt das richtige Experiment',
										height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.0)),
					  visual.TextStim(win, text='Es geht gleich los...',
					  					height = fontsize,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,-0.1))]

	press_left_text = visual.TextStim(win, text='Drücke die linke Taste',
										height = 0.075,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

	press_right_text = visual.TextStim(win, text='Drücke die rechte Taste',
	 									color = 'white',
										font = 'Arial',
										height = 0.075,
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

	press_nothing_text = visual.TextStim(win, text='Drücke nichts',
										color = 'white',
										font = 'Arial',
										height = 0.075,
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))





instructions_text1.wrapWidth = wrapwidth
instructions_text2.wrapWidth = wrapwidth
instructions_text3.wrapWidth = wrapwidth
instructions_text4.wrapWidth = wrapwidth
instructions_text5.wrapWidth = wrapwidth
instructions_text6.wrapWidth = wrapwidth
instructions_text7.wrapWidth = wrapwidth
instructions_text8.wrapWidth = wrapwidth

for instruction in instructions2_text:
	instruction.wrapWidth = wrapwidth


### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()

# Create the results folder

if not os.path.exists('results'):
    os.makedirs('results')

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_%s_%s_staircase.csv'%(subid,session,time_stamp)
output_file = open(output_file_path,'w+')

###TO DO
output_file.write('subid,session,trial,trial_type,stim_side,response,correct,response_time,cumulative_response_time,iti_onset,iti_dur,stim_onset,stim_dur_frames,stim_dur,blank_onset,blank_dur,mask_onset,mask_dur,response_onset,response_dur,target_side,version,currentDirection,presentation_duration\n')
output_file.flush()


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


##### RUN EXPERIMENT #####

###  instructions  ###
#explain task
if show_practice:
	#intro to experiment
	instructions_header.draw()
	instructions_text1.draw()
	win.flip()
	event.waitKeys(keyList='space')
#
#	#show missing corner shapes
	instructions_header.draw()
	instructions_text2.draw()
	instructions_text3.draw()
	left_example.draw()
	right_example.draw()
	win.flip()
	event.waitKeys(keyList='space')
#
#	#show frame shape
	instructions_header.draw()
	instructions_text4.draw()
	frame_example.draw()
	win.flip()
	event.waitKeys(keyList='space')
#
#	#tell what buttons to press
	instructions_header.draw()
	instructions_text5.draw()
	instructions_text6.draw()
	win.flip()
	event.waitKeys(keyList='space')
#
	instructions_header.draw()
	example_text.draw()
	win.flip()
	event.waitKeys(keyList='space')
#
	for practice_side in ['left','right']:
		instructions_header.draw()
		win.flip()
		core.wait(practice_iti_dur)
		#press practice stim
		practice_clock.reset()
		while practice_clock.getTime() < practice_stim_dur:
			instructions_header.draw()
			white_diamond.draw()
			blockers[practice_side].draw()
			win.flip()
		#blank screen
		while practice_clock.getTime() < practice_stim_dur+practice_blank_dur:
			instructions_header.draw()
			win.flip()
		#press mask
		while practice_clock.getTime() < practice_stim_dur+practice_blank_dur+practice_mask_dur:
			instructions_header.draw()
			mask.draw()
			black_diamond.draw()
			if version == 'go-nogo' and target_side == practice_side:
				press_nothing_text.draw()
			else:
				if practice_side == 'left':
					press_left_text.draw()
				else:
					press_right_text.draw()
			win.flip()
		#response
		instructions_header.draw()
		if practice_side == 'left':
			press_left_text.draw()
		else:
			press_right_text.draw()
		win.flip()
		event.waitKeys(keyList=response_keys[practice_side])


	#Post practice text, get ready for experiment
	instructions_header.draw()
	for instruction in instructions2_text:
		instruction.draw()
	win.flip()
	event.waitKeys(keyList='space')
	experiment_header.draw()
	for get_ready in get_ready_text:
		get_ready.draw()
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

correctInARow = 0
mask_dur = initialMask_dur
stim_dur = initialStim_dur
currentDirection = ''
directions = ['a'] * (len(trial_order) + 1)
trial = 0
for shuffled_trial in trial_order:
	trial += 1
	iti_dur = choice(iti_durs)
	target_side = trial_states[shuffled_trial]['target']
	if (target_side == 'left'):
		side = 'left'
	else:
		side = 'right'

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
		#response collection
		if not responded:
			response = event.getKeys(keyList=reskeys_list, timeStamped=True)
			if len(response) > 0:
				responded = True
				cumulative_response_time = round(experiment_clock.getTime(),3)
				response_time = round(experiment_clock.getTime() - start_response,3)
				sub_response = response_keys_inv[response[0][0]]
				if version == 'oddball':
					if sub_response == side:
						correct = 1
						currentDirection = 'down'
					else:
						correct = 0 #0
						currentDirection = 'up'
				output_file.write(','.join([str(subid),str(session),str(trial),str(target_side),str(side),str(sub_response),str(correct),str(response_time),str(cumulative_response_time),str(iti_onset/60),str(iti_dur/60),str(stim_onset/60),str(stim_dur),str(stim_dur/60),str(blank_onset/60),str(blank_dur/60),str(mask_onset/60),str(mask_dur/60),str(response_onset/60),str(response_dur/60),target_side,version,str(currentDirection),str(presentation_duration)+'\n']))
				output_file.flush()

	if not responded:
		if version == 'go-nogo' and target_type == 'target':
			correct = 1
		else:
			correct = 0 #0
		output_file.write(','.join([str(subid),str(session),str(trial),str(target_side),str(side),'NA',str(correct),'NA','NA',str(iti_onset/60),str(iti_dur/60),str(stim_onset/60),str(stim_dur),str(stim_dur/60),str(blank_onset/60),str(blank_dur/60),str(mask_onset/60),str(mask_dur/60),str(response_onset/60),str(response_dur/60),str(target_side),str(version),str(currentDirection),str(presentation_duration)+'\n']))
		output_file.flush()
	#timing update
	last_trial_dur = iti_dur + stim_dur + blank_dur + mask_dur + response_dur

	directions[trial] = currentDirection

	if trial > 1:
		if not directions[trial] == directions[trial-1]:
			stepsize = stepsize / 2
			if stepsize < 1:
				stepsize = 1

	if correct == 1:
		correctInARow += 1
		if correctInARow == 2:
			stim_dur -= stepsize
			mask_dur += stepsize
			correctInARow = 0

	else:
		correctInARow = 0
		stim_dur += stepsize
		mask_dur -= stepsize


	if stim_dur < 1:
		stim_dur = 1

	if mask_dur > 12:
		mask_dur = 12

	if mask_dur < 1:
		mask_dur = 1

	if stim_dur > 12:
		stim_dur = 12


output_file.close()
win.close()
