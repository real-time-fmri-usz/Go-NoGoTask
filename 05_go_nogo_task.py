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
dlg.addField('Run:')
dlg.addField('Scanner', choices = ['yes','no'])
dlg.addField('Stimulus Threshold (in Frames):')
dlg.addField('Go Side', choices = ['left','right'])
dlg.addField('Practice', choices = ['yes','no'])
dlg.addField('Language', choices = ['en', 'de'])
dlg.addField('Session:')

exp_input = dlg.show()

#port = parallel.ParallelPort(0x1FF8)
### Parameters ###

###### EDIT PARAMETERS BELOW #######

stim_dur = {'strong':1,'weak':float(exp_input[3]),'catch':0}     # time in seconds that the subliminal stim appears on the screen [strong,weak,catch]
blank_dur = {'strong':2,'weak':2,'catch':0}        # time a blank screen between stim and mask is on screen [strong,weak,catch]
mask_dur = {'strong':12,'weak': 12 - float(exp_input[3]) + 1,'catch':15}     # time the mask appears on the screen [strong,weak,catch]
responses = [78,80,82,84,86,88,92,94,96,98,100,102]
response_dur_list = responses * 12
random.shuffle(response_dur_list)            # time the response period stays on the screen
fixation_dur = 12			# fixation before stimulus_strength
blank_dur_pre = 3
pause_dur = [258, 312, 340];
random.shuffle(pause_dur)
#strength_prob = [.5,.5]   # probability of the trial being strong or weak
stim_size = .06             #size of the stimulus on screen
mask_size_ratio = 1.6         #how much proptionally bigger is mask
#stim_line_width =  200      # width of diamond frame lines
blocker_size = .15         #size of black boxes the mask the edge of the stimulus (pick a value between 0 and 1. 0 blocks nothing, 1 blocks a whole half)
response_keys = {'left':'b','right':'z'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','z']
pix_size = .001

practice_iti_dur = 2
practice_stim_dur = .3
practice_blank_dur = .033
practice_mask_dur = .3

#which run
run = exp_input[1]


###### STOP EDITING BELOW THIS LINE #######



subid = exp_input[0]
if exp_input[2] == 'yes':
	scanner = True
else:
	scanner = False
stimulus_strength = exp_input[3]
go_side = exp_input[4]

if go_side == 'left':
	go_side_de = 'linke'
	nogo_side = 'right'
	nogo_side_de = 'rechte'
else:
	nogo_side = 'left'
	nogo_side_de = 'linke'
	go_side_de = 'rechte'

if exp_input[5] == 'yes':
	show_practice = True
else:
	show_practice = False

language = exp_input[6]
session = exp_input[7]



### Visuals ###


#window
win = visual.Window(size=[800, 600], color=[-1,-1,-1], screen = 0, fullscr = False)
win.setMouseVisible(False)
aspect = float(win.size[1])/float(win.size[0])
print(aspect)
stim_width = stim_size
stim_height = stim_size/aspect
fontsize = 0.055
wrapwidth = 80
#Shapes
mask = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width*mask_size_ratio, 0), (0, stim_height*mask_size_ratio), (stim_width*mask_size_ratio, 0), (0,-1*stim_height*mask_size_ratio)))
white_diamond = visual.ShapeStim(win, lineColor='white', fillColor='white', vertices=((-1*stim_width, 0), (0, stim_height), (stim_width, 0), (0,-1*stim_height)))
black_diamond = visual.ShapeStim(win, lineColor='black', fillColor='black', vertices=((-1*stim_width-pix_size, 0), (0, stim_height+pix_size), (stim_width+pix_size, 0), (0,-1*stim_height-pix_size)))
blockers = {'left':  visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, stim_height), (-1, -1*stim_height), (-1*stim_width+stim_width*blocker_size, stim_height), (-1*stim_width+stim_width*blocker_size, -1*stim_height))),
			'right': visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((1, stim_height), (1, -1*stim_height), (stim_width-stim_width*blocker_size, stim_height), (stim_width-stim_width*blocker_size, -1*stim_height))),
			'top':   visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, 1), (1, 1), (-1,stim_height-stim_size*blocker_size), (1,stim_height-stim_height*blocker_size))),
			'bottom':visual.ShapeStim(win, lineWidth=.1, lineColor='black', fillColor='black', vertices=((-1, -1), (1, -1), (-1,-1*stim_height+stim_height*blocker_size), (1,-1*stim_height+stim_height*blocker_size)))
			}


#noise
noiseTexture = rd.random([512,512])*2.0-1. # a X-by-X array of random numbers in [-1,1]
noise = visual.GratingStim(win, tex=noiseTexture, mask=None, size=(stim_width*2,stim_height*2))


#Fixation
fixation = visual.ShapeStim(
				win=win, name='polygon', vertices='cross',
			    size=(stim_width/1.5, stim_height/1.5),
			    ori=0, pos=(0, 0),
			    fillColor=[1,1,1], fillColorSpace='rgb',
				lineColor = [-1,-1,-1],
			    opacity=1, depth=0.0, interpolate=True)

###text
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
					pos=[-150,-50])

frame_example = visual.ImageStim(
	win=win,
	image="mask.png",
	units="pix",
	pos=[0,-50])



#Create instructions depending on the language

if language == 'en':

	#instructions_en
	instructions_text1 = visual.TextStim(win, text='Press the "%s" button as fast as possible when you see this frame.'%go_side,
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text2 = visual.TextStim(win, text='If the frame is preceded by a diamond with a missing edge on its %s side, press the %s button!'%(go_side,go_side),
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text3 = visual.TextStim(win, text='However, do not press any button if the frame is preceded by a diamond with a missing edge on its %s side!'%nogo_side,
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text4 = visual.TextStim(win, text='Keep in mind: In the experiment, the speed of the diamond and frame presentation will be fast! ',
										height = fontsize,
										font = 'Arial',
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

	press_left_text = visual.TextStim(win, text='Press left',
										height = 0.075,
										font = 'Arial',
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,stim_size+.2))

	press_right_text = visual.TextStim(win, text='Press right',
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

elif language == 'de':


	instructions_text1 = visual.TextStim(win, text='Drücke die %s Taste so schnell wie möglich, wenn du diesen Rahmen siehst.'%go_side_de,
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text2 = visual.TextStim(win, text='Drücke die %s Taste, wenn dem Rahmen ein Diamant vorangeht, dem die %s Seite fehlt!'%(go_side_de,go_side_de),
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text3 = visual.TextStim(win, text='Aber, drücke keine Taste, wenn dem Rahmen ein Diamant vorangeht, dem die %s Seite fehlt!'%nogo_side_de,
										font = 'Arial',
										height = fontsize,
										color = 'white',
										alignHoriz = 'center',
										alignVert = 'center',
										pos=(0.0,0.3))

	instructions_text4 = visual.TextStim(win, text='Denke daran: Im Experiment ist die Geschwindigkeit der Diamanten und Rahmen sehr hoch!',
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

### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_%s_%s_%s_%s_%s.csv'%(subid,run,stimulus_strength,go_side,time_stamp,session)
output_file = open(output_file_path,'w+')
output_file.write('subid,session,run,trial,trial_type,side,response,correct,strength,response_time,cumulative_response_time,fixation_onset,fixation_dur,stim_onset,stim_dur,blank_onset,blank_dur,mask_onset,mask_dur,response_onset,response_dur,go_side,Staircase_stimulus,Presentation Duration\n')
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
	frame_example.draw()
	win.flip()
	event.waitKeys(keyList='space')

	#show missing corner shapes
	instructions_header.draw()
	instructions_text2.draw()
	if go_side == 'right':
		right_example.draw()
	else:
		left_example.draw()
	frame_example.draw()
	win.flip()
	event.waitKeys(keyList='space')

	#show frame shape
	instructions_header.draw()
	instructions_text3.draw()
	if go_side == 'right':
		left_example.draw()
	else:
		right_example.draw()
	frame_example.draw()
	win.flip()
	event.waitKeys(keyList='space')

	#tell what buttons to press
	instructions_header.draw()
	instructions_text4.draw()
	win.flip()
	event.waitKeys(keyList='space')

	for get_ready in get_ready_text:
		get_ready.draw()
	win.flip()
	event.waitKeys(keyList='space')

print(go_side)

### Main Experiment ###

#clock reset
win.flip()
elapse_time = 0
last_trial_dur = 0

#trigger scanner
if scanner:
	#port.write(chr(np.uint8(128+32+64+1)))
    event.waitKeys(keyList=['t'])

experiment_clock.reset()

# Create a list of blocks and shuffle them
block_list = [1,2,3,4]
random.shuffle(block_list)

# Iterate over three shorter blocks of the nogo task with 20 seconds pause inbetween
elapse_time = 0
for b in range(len(block_list)):

	trial_list_block = pd.read_csv(filepath_or_buffer = "trials/no_go_catch_run"+run+"-00"+str(block_list[b])+".par",
	delim_whitespace=True,
    header = None,
    names = ['totalDur', 'trialType', 'duration', 'weirdFactor', 'trialName'])
	trial_list_block = trial_list_block.replace(np.nan,'Null')
	go_type = ''
	strength = ''
	last_trial_dur = 0
	for trial in range(len(trial_list_block)):
		if trial_list_block['trialName'][trial] == 'Null':
			elapse_time += last_trial_dur
			trial_duration = int(trial_list_block['duration'][trial] * 60)
			for frames in range(trial_duration):
				win.flip()
			output_file.write(','.join([str(subid),str(session),str(run),str(trial+1),'Rest','Rest','Rest','Rest','Rest','Rest','Rest',str(elapse_time/60),str(trial_list_block['duration'][trial]),'Rest','Rest','Rest','Rest','Rest','Rest','Rest','Rest','Rest','Rest',str(trial_list_block['duration'][trial])+'\n']))
			output_file.flush()
			last_trial_dur = trial_duration

		else:
			if trial_list_block['trialName'][trial] == 'weakGo':
				strength = 'weak'
				go_type = 'go'
			elif trial_list_block['trialName'][trial] == 'strongGo':
				strength = 'strong'
				go_type = 'go'
			elif trial_list_block['trialName'][trial] == 'weakNoGo':
				strength = 'weak'
				go_type = 'nogo'
			elif trial_list_block['trialName'][trial] == 'strongNoGo':
				strength = 'strong'
				go_type = 'nogo'
			elif trial_list_block['trialName'][trial] == 'catch':
				strength = 'catch'
				go_type = 'catch'

			if (go_type == 'go' and go_side == 'left') or (go_type == 'nogo' and nogo_side == 'left'):
				side = 'left'
			else:
				side = 'right'

			if go_type == 'catch':
				side = 'NA'

			response_dur = response_dur_list[0]
			print(len(response_dur_list))
			response_dur_list.pop(0)

			elapse_time += last_trial_dur
			fixation_onset = elapse_time
			pre_blank_onset = fixation_onset + fixation_dur
			stim_onset = elapse_time + fixation_dur + blank_dur_pre
			blank_onset = elapse_time + fixation_dur + blank_dur_pre + stim_dur[strength]
			mask_onset = elapse_time + fixation_dur + blank_dur_pre + stim_dur[strength] + blank_dur[strength]
			response_onset = elapse_time + fixation_dur + blank_dur_pre + stim_dur[strength] + blank_dur[strength] + mask_dur[strength]

			for s in range(int(fixation_dur)):
				fixation.draw()
				win.flip()

			for p in range(int(blank_dur_pre)):
				win.flip()


			# if go_type == 'go' and strength == 'weak':
			# 	win.callOnFlip(port.setData, int("00000001", 2))
			# # elif go_type == 'go' and strength == 'strong':
			# # 	win.callOnFlip(port.setData, int("00000010", 2))
			# elif go_type == 'nogo' and strength == 'weak':
			# 	win.callOnFlip(port.setData,int("00000011", 2))
			# # elif go_type == 'nogo' and strength == 'strong':
			# # 	win.callOnFlip(port.setData,int("00000100", 2))
			# elif go_type == 'catch':
			# 	win.callOnFlip(port.setData,int("00000101", 2))
			start_stimulus = experiment_clock.getTime()
			for stim in range(int(stim_dur[strength])):
				white_diamond.draw()
				if side != 'NA':
					blockers[side].draw()
				win.flip()
				# if go_type == 'go' and strength == 'strong':
				# 	win.callOnFlip(port.setData, int("00000010", 2))
				# elif go_type == 'nogo' and strength == 'strong':
				# 	win.callOnFlip(port.setData,int("00000100", 2))
			presentation_duration = experiment_clock.getTime() - start_stimulus
			#port.setData(0)
			#blank presentation
			for m in range(int(blank_dur[strength])):
				win.flip()

			# mask presentation
			responded = False
			response = []
			event.clearEvents(eventType=None)
			start_response = experiment_clock.getTime()
			for rr in range(int(response_dur)):
				if rr < mask_dur[strength]:
					mask.draw()
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
						# port.setData(129)
						if go_type == 'go':
							correct = 1
						elif sub_response == side:
							correct = 1
						else:
							correct = 0
						if go_type == 'catch':
							correct = 1
						output_file.write(','.join([str(subid),str(session), str(run),str(trial+1),str(go_type),str(side),str(sub_response),str(correct),strength,str(response_time),str(cumulative_response_time),str(fixation_onset/60),str(fixation_dur/60),str(stim_onset/60),str(stim_dur[strength]/60),str(blank_onset/60),str(blank_dur[strength]/60),str(mask_onset/60),str(mask_dur[strength]/60),str(response_onset/60),str(response_dur/60),go_side,stimulus_strength,str(presentation_duration)+'\n']))
						output_file.flush()

			if not responded:
				if go_type == 'nogo':
					correct = 1
				elif go_type == 'catch':
					correct = 0
				else:
					correct = 0
				output_file.write(','.join([str(subid),str(session), str(run),str(trial+1),str(go_type),str(side),'NA',str(correct),strength,'NA','NA',str(fixation_onset/60),str(fixation_dur/60),str(stim_onset/60),str(stim_dur[strength]/60),str(blank_onset/60),str(blank_dur[strength]/60),str(mask_onset/60),str(mask_dur[strength]/60),str(response_onset/60),str(response_dur/60),str(go_side),str(stimulus_strength),str(presentation_duration)+'\n']))
				output_file.flush()

			last_trial_dur = fixation_dur + blank_dur_pre + stim_dur[strength] + blank_dur[strength] + mask_dur[strength] + response_dur
			#port.setData(0)
	pause_text = visual.TextStim(win, text='Pause', height = .065, color = 'white', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
	if not b == 3:
		for p in range(int(pause_dur[b])):
			pause_text.draw()
			win.flip()
		elapse_time += pause_dur[b]
