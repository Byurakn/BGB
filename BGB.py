#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Broken Grammar and Beyond
# Byurakn Ishkhanyan KU 2021

# import modules
from psychopy import visual, core, event, gui, data
from psychopy import logging
from importlib import reload
import numpy as np
import re
import glob, random
import time
import sys
import os
import pandas as pd
#reload(sys)
#sys.setdefaultencoding('utf-8')



# gui requesting participant info
participant_id = gui.Dlg(title='BGB') 
participant_id.addText('Subject Info')
participant_id.addField('ID: ')
participant_id.addField('Session: ', choices = [1, 2, 3])
participant_id.addField('Blocks: ', choices = [3, 2])
participant_id.show()

#saves data from dialogue box into the variable 'ID'
if participant_id.OK:
    ID = participant_id.data 

# number of repetitions
SESSION = 1

# instructions
intro = '''
Eksperimentet starter om få sekunder...
Husk: Tryk når du ser de grønne ???  hvis sætningerne skaber en helhed. 
Pegefinger = ja Langefinger = nej
'''


pause1 = '''
Blok 1/3 er færdig. Tag en kort pause.

'''
pause2 = '''
Blok 2/3 er færdig. Tag en kort pause.
'''

pause3 = '''
Blok 1/2 er færdig. Tag en kort pause.
'''

outro = '''
Forsøget er nu slut. 

Tak for din deltagelse.
'''

# define window
win = visual.Window(fullscr=True, color = 'black')

# get date for unique logfile id
date = data.getDateStr()

# Check if a log file directory exists and create one, if it doesn't
current_path = os.getcwd()
log_path = "\logfiles_BGB"
if not os.path.exists(current_path+log_path):
    os.makedirs(current_path+log_path)

# initiate logfiles
log = pd.DataFrame()
subject = ID[0]
session = ID[1]
blocks = ID[2]
filename = 'logfiles_BGB/{}{}{}_summary.csv'.format(subject, session, date)
filename2 = 'logfiles_BGB/{}{}{}.log'.format(subject, session, date)

# logging
logging.console.setLevel(logging.WARNING)

# overwrite (filemode='w') a detailed log of the last run in this dir
lastLog = logging.LogFile(filename2, level=logging.INFO, filemode='w')

# define clock for reaction time
global_time = core.Clock()
stopwatch = core.Clock()

# fetch stimuli from file
if session == 1:
    ordered = pd.read_csv("stimuli.csv", sep =  ";", encoding = 'ISO-8859-1')
    # randomizes the order of the lists
    list1 = ordered[ordered['List'] == 1]
    list1.reset_index(drop=True, inplace = True)
    list2 = ordered[ordered['List'] == 2]
    list2.reset_index(drop=True, inplace = True)
    list3 = ordered[ordered['List'] == 3]
    list3.reset_index(drop=True, inplace = True)
    list4 = ordered[ordered['List'] == 4]
    list4.reset_index(drop=True, inplace = True)
    list5 = ordered[ordered['List'] == 5]
    list5.reset_index(drop=True, inplace = True)
    list6 = ordered[ordered['List'] == 6]
    list6.reset_index(drop=True, inplace = True)
    list7 = ordered[ordered['List'] == 7]
    list7.reset_index(drop=True, inplace = True)
    list8 = ordered[ordered['List'] == 8]
    list8.reset_index(drop=True, inplace = True)
    lists = [list1, list2, list3, list4, list5, list6, list7, list8]
    random.shuffle(lists)
    rand_list = pd.concat(lists)
    rand_list.reset_index(drop=True, inplace = True)


# creating and shuffling the sessions
if blocks == 3:
    if session == 1:
        sessions = ['1', '2', '3']
        random.shuffle(sessions)
        # creating stimuli for 3 separate sessions
        stim1 = rand_list[0:43]
        stim2 = rand_list[43:85]
        stim3 = rand_list[85:128]
        file1 = "stim{}{}.csv".format(subject, sessions[0])
        file2 = "stim{}{}.csv".format(subject, sessions[1])
        file3 = "stim{}{}.csv".format(subject, sessions[2])
        stim1.reset_index(drop=True, inplace = True)
        stim2.reset_index(drop=True, inplace = True)
        stim3.reset_index(drop=True, inplace = True)
        stim1.to_csv(file1, sep =  ";", encoding = 'ISO-8859-1')
        stim2.to_csv(file2, sep =  ";", encoding = 'ISO-8859-1')
        stim3.to_csv(file3, sep =  ";", encoding = 'ISO-8859-1')
else:
    if session == 1:
        sessions = ['1', '2']
        random.shuffle(sessions)
        # creating stimuli for 2 separate sessions
        stim1 = rand_list[0:64]
        stim2 = rand_list[64:128]
        file1 = "stim{}{}.csv".format(subject, sessions[0])
        file2 = "stim{}{}.csv".format(subject, sessions[1])
        stim1.reset_index(drop=True, inplace = True)
        stim2.reset_index(drop=True, inplace = True)
        stim1.to_csv(file1, sep =  ";", encoding = 'ISO-8859-1')
        stim2.to_csv(file2, sep =  ";", encoding = 'ISO-8859-1')
stim_file = "stim{}{}.csv".format(subject, session)
stim = pd.read_csv(stim_file, sep =  ";", encoding = 'ISO-8859-1')

# pseudorandomizing the stimuli
stim['cond'] = stim['Condition'].str[0]
stim.groupby('cond').cumcount()
stim["s_cumcounts"] = stim.groupby("cond").cumcount()
stim.sort_values(["s_cumcounts", "cond"])
stim = stim.sort_values(["s_cumcounts", "cond"])
stim.reset_index(drop=True, inplace = True)
takesamp = lambda d: d.sample(frac = 1)
stim = stim.groupby('s_cumcounts').apply(takesamp)
stim.reset_index(drop=True, inplace = True)

# saves a stimuli file. will be removed after everything is checked
stim.to_csv("cond_test.csv", sep =  ";", encoding = 'ISO-8859-1')

# getting rid of the mouse because annoying
myMouse = event.Mouse(win=win)
myMouse.setVisible(0)

# sentence
def show_txt(txt):
    txt_stim = visual.TextStim(win, text = txt, color = 'white', height = 0.08)
    txt_stim.draw()
    win.flip()


# fixation cross
fix_cross = visual.TextStim(win, text = '+', color = 'white', height = 0.1)

# question
def show_q(txt):
    txt_stim = visual.TextStim(win, text = txt, color = 'green', height = 0.1)
    txt_stim.draw()
    win.flip()

question = "???"


def shutdown():
    win.close()
    core.quit()
    
# keys
KEYS_trigger=['t'] # The MR scanner sends a "t" to notify that it is starting
quit_key = 'escape' # quits the experiment

# global key to quit the experiment
event.globalKeys.add(key=quit_key, func=shutdown)


#### run experiment ####

# instructions
show_txt(intro)
#core.wait(5)
#Wait for scanner trigger "t" to continue
event.waitKeys(keyList=KEYS_trigger) 
global_time.reset()

ITI = []
ISI = []

for i in range(len(stim)+1):
    n = 3 + (random.randint(0, 4000)/1000)
    m = 3 + (random.randint(0, 4000)/1000)
    ITI.append(n)
    ISI.append(m)
ITI_onset_list = []
acc = 0
# loop through trials
for n in range(len(stim)):
    if n == 0:
        fix_cross.draw()
        win.flip()
        ITI_onset_1 = global_time.getTime()
        ITI_onset_list.append(ITI_onset_1)
        core.wait(ITI[0])
    show_txt(stim['Part1'][n])
    Part1_onset = global_time.getTime()
    core.wait(2)
    fix_cross.draw()
    win.flip()
    fix_cross1_onset = global_time.getTime()
    core.wait(0.3)
    show_txt(stim['Part2'][n])
    Part2_onset = global_time.getTime()
    core.wait(2)
    fix_cross.draw()
    win.flip()
    fix_cross2_onset = global_time.getTime()
    core.wait(0.3)
    show_txt(stim['Part3'][n])
    Part3_onset = global_time.getTime()
    core.wait(2)
    fix_cross.draw()
    win.flip()
    ISI_onset = global_time.getTime()
    core.wait(ISI[n])
    event.clearEvents()
    stopwatch.reset()
    show_q(question)
    q_onset = global_time.getTime()
    core.wait(1)
    if n < len(stim):
        fix_cross.draw()
        win.flip()
        ITI_onset_n = global_time.getTime()
        ITI_onset_list.append(ITI_onset_n)
        core.wait(ITI[n+1])
    if n == 0:
        ITI_onset = ITI_onset_list[0]
    elif n > 0 and n < len(stim):
        ITI_onset = ITI_onset_list[n]
    key = event.getKeys(keyList=['left', 'right'], timeStamped=stopwatch)
    if key:
        if (key[0][0] == 'left' and stim['ExpectedResponse'][n] == "Y") or (key[0][0] == 'right' and stim['ExpectedResponse'][n] == "N"):
            accuracy = 1
            acc = acc + accuracy
        else:
            accuracy = 0
        log = log.append({'SubjectID': ID[0],
        'Session': ID[1],
        'List': stim['List'][n],
        'Part1': stim['Part1'][n],
        'Part2': stim['Part2'][n],
        'Part3': stim['Part3'][n],
        'Condition': stim['Condition'][n],
        'Item': stim['Item'][n],
        'Homophone': stim['Homophone'][n],
        'Verbform': stim['Verbform'][n],
        'ExpectedResponse': stim['ExpectedResponse'][n],
        'Timestamp': global_time.getTime(),
        'Accuracy': accuracy,
        'Response': key[0][0],
        'RT': key [0][1],
        'ITI': ITI[n],
        'ISI': ISI[n],
        'ITI_onset': ITI_onset,
        'Part1_onset': Part1_onset,
        'fix_cross1_onset': fix_cross1_onset,
        'Part2_onset': Part2_onset,
        'fix_cross2_onset': fix_cross2_onset,
        'Part3_onset': Part3_onset,
        'ISI_onset': ISI_onset,
        'q_onset': q_onset}, ignore_index = True)
    else:
        log = log.append({'SubjectID': ID[0],
        'Session': ID[1],
        'List': stim['List'][n],
        'Part1': stim['Part1'][n],
        'Part2': stim['Part2'][n],
        'Part3': stim['Part3'][n],
        'Condition': stim['Condition'][n],
        'Item': stim['Item'][n],
        'Homophone': stim['Homophone'][n],
        'Verbform': stim['Verbform'][n],
        'ExpectedResponse': stim['ExpectedResponse'][n],
        'Timestamp': global_time.getTime(),
        'Accuracy': 'NA',
        'Response': 'NA',
        'RT': 'NA',
        'ITI': ITI[n],
        'ISI': ISI[n],
        'ITI_onset': ITI_onset,
        'Part1_onset': Part1_onset,
        'fix_cross1_onset': fix_cross1_onset,
        'Part2_onset': Part2_onset,
        'fix_cross2_onset': fix_cross2_onset,
        'Part3_onset': Part3_onset,
        'ISI_onset': ISI_onset,
        'q_onset': q_onset}, ignore_index = True)
    col_order = ['SubjectID', 'Session', 'List', 'Part1', 'Part2', 'Part3', 'Condition', 
    'Item', 'Homophone', 'Verbform', 'ITI', 'ISI', 'ExpectedResponse', 'Timestamp', 'Response', 'RT', 'Accuracy',
        'ITI_onset', 'Part1_onset', 'fix_cross1_onset', 'Part2_onset', 'fix_cross2_onset', 'Part3_onset','ISI_onset',
        'q_onset']
    log[col_order].to_csv(filename, sep =  ";", encoding = 'ISO-8859-1')
    print (n, acc) 
if ID[2] == 3:
    if ID[1] == 1:
        show_txt(pause1)
    elif ID[2] == 2:
        show_txt(pause2)
    else:
        show_txt(outro)
elif ID[2] == 2:
    if ID[1] == 1:
        show_txt(pause3)
    else:
        show_txt(outro)
core.wait(10)
core.quit()