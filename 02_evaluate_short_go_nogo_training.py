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
data = pandas.read_csv(file)

clean_data = data[data['correct'] != 'Rest']
only_correct = clean_data[clean_data['correct'] == '1'].groupby(['trial_type','strength']).count()
all_data = clean_data.groupby(['trial_type','strength']).count()

percentages_correct = only_correct/all_data

print('Percentages correct trials per condition')
print(percentages_correct['correct'] * 100)

core.quit()
