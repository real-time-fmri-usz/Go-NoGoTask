#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging
from time import strftime
import pandas as pd
from random import choice
from numpy.random import choice as choice2
import numpy as np
import random
import csv
import pandas
import matplotlib
import matplotlib.pyplot as plt
from psychopy.tools.filetools import fromFile
import pylab
import os
from operator import truediv

#Open Dialog for file
files = gui.fileOpenDlg('./results/')
file = files[0]


full_filename = os.path.splitext(os.path.basename(file))
filename = full_filename[0]

save_dir = os.path.dirname(file)

## Plot the staircase data to get the threshold
matplotlib.style.use('ggplot')
plt.style.use('seaborn-dark-palette')
colors = {0:'red', 1:'green'}
data = pandas.read_csv(file)
data['corr_factor'] = data['correct'].astype('category')
data['rounded_durations'] = round(data['stim_dur'],3)

#Plot1


plt.plot(data['trial'], data['stim_dur'])
plt.scatter(data = data, x='trial', y = 'stim_dur', c = data['corr_factor'].apply(lambda x: colors[x]), label = 'corr_factor', s = 1)
plt.title('Trial pathway')
plt.xlabel('Trial')
plt.ylabel('Stimulus Duration')
plt.savefig(save_dir+'/'+filename+'_trialPath.pdf')
plt.close()

#Plot2
durations = np.unique(data['rounded_durations'])
#cat_durations = ",".join(str(s) for s in durations)
#cat_durations = [ '%.2f' % elem for elem in durations]



nTrials = []
nCorrect = []
for i in range(len(durations)):
    id = data['rounded_durations'] == durations[i]
    nTrials.append(sum(id*1))
    nCorrect.append(sum((data['correct'][id])))
    

pCorrect = np.divide(nCorrect,nTrials)


#dataframe for correctness, nTrials, etc

sumData = pd.DataFrame({'durations': durations.astype('str'),'pCorrect':pCorrect*100,'nTrials':nTrials})
plt.scatter(data = sumData, x = 'durations', y = 'pCorrect', s = 'nTrials')

plt.title('Correct Responses by stimulus durations')
plt.xlabel('Stimulus Duration')
plt.ylabel('Percentage Correct')

plt.savefig(save_dir+'/'+filename+'_stimdur.pdf')

core.quit()
