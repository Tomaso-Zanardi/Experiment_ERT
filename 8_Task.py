##--------------------------------------------
## Importing modules
##--------------------------------------------

from psychopy import core, visual, event, data, gui  # psychopy modules
from psychopy import data, gui
import random
import os

##-------------------------------------------------
## ESCAPE KEY
##-------------------------------------------------

## This interrupts the whole experiment if the escape button is pressed
# ATTENTION: data will not be saved if the experiment is interrupted
event.globalKeys.clear()
event.globalKeys.add(key='escape', func=os._exit, func_args=[1], func_kwargs=None)
# Note: normally one should use func = core.quit
# but for some reason it is not working well in some psychopy versions
# (the problem has been reported from others on the psychopy forum)
# Check if in future releases the bug will be solved!

##-------------------------------------------------
## GUI for participants info
##-------------------------------------------------

# Specify fields for dlg as a dict
info = {'Subject':'', 
    'Age':'',
    'Gender': ['Female', 'Male', 'Other'],
    'Handedness': ['Right', 'Left']} 

# Use this dict to create the dlg
infoDlg = gui.DlgFromDict(dictionary=info, 
    title='TestExperiment',
    order=['Subject', 'Age', 'Gender', 'Handedness'])
# Script will now wait for the dlg to close...

if infoDlg.OK:  # This will be True if user hit OK...
    print(info)
else: # ...or False, if they hit Cancel
    print('User Cancelled')
    
##-------------------------------------------------
## Design Matrix
##-------------------------------------------------

# create your list of stimuli
stimList = data.createFactorialTrialList(
    {'instrBehav':['approachHappy', 'approachAngry'],
    'groupBehav':['approach', 'avoid'],
    'stimValence': ['happy', 'angry']})


## increase number of trials
# we want a total of 240 trials (8*30)
# and 8 trials of practice for each of the two orders (8 * 2)
stimList = stimList * 32

# randomize trial order
random.shuffle(stimList)
#print(stimList)

# sorts trials based on instrBehav to make it blocked
# need to make it conditional on subjnumber so that it is counterbalanced
if int(info['Subject']) % 2 == 0:
    newList = sorted(stimList, key=lambda d: d['instrBehav'], reverse = False)
else:
    newList = sorted(stimList, key=lambda d: d['instrBehav'], reverse = True)

#print(newList)


##-------------------------------------------------
## Experiment and TrialHandler
##-------------------------------------------------

# creating output file
# If you do not specify a folder, it will be saved in the same folder where the 
# experiment script is located

# if there is no subfolder called 'data' in the current folder
# (the folder in which your script is), this will create the data folder
# we will use it to save our results
if not os.path.isdir('/data'):        #creates the folder for output data
    os.mkdir('/data')
    
fileName = 'data/ERT_Subj'+ info['Subject']

# Setting an ExperimentHandler for data saving
thisExp = data.ExperimentHandler(name='ERT_exp',
    extraInfo=info,
    savePickle=True, # this saves an additional output file that is an "emergency backup"
    saveWideText=True,
    dataFileName=fileName)
    
#Setting the trial list using TrialHandler
trials = data.TrialHandler(nReps=1, # number of times to repeat the list of trials
    method='sequential', # we already organized our list of trials in the order we want
    trialList=newList,
    name='trials')

# Adding the trial loop to the experiment
thisExp.addLoop(trials)

##--------------------------------------------
## Creating a window
##-------------------------------------------- 

win = visual.Window(size = [1920, 1080], color='Gray', colorSpace='rgb', units='pix',
                    fullscr = True)
win.mouseVisible = False

##--------------------------------------------
## Creating stimuli
##--------------------------------------------

message = visual.TextStim(win, color = 'white')
happy = visual.ImageStim(win, 'happy.jpg', pos=[0, 300], size = [300, 220])
angry = visual.ImageStim(win, 'angry.jpg', pos=[0, 300], size = [300, 220])
avatar = visual.ImageStim(win, 'avatar.png', pos=[0, -200], size = [80, 160])
group1 = visual.ImageStim(win, 'avatar.png', pos=[150, -230], size = [50, 100])
group2 = visual.ImageStim(win, 'avatar.png', pos=[300, -230], size = [50, 100])
group3 = visual.ImageStim(win, 'avatar.png', pos=[450, -230], size = [50, 100])
group4 = visual.ImageStim(win, 'avatar.png', pos=[-150, -230], size = [50, 100])
group5 = visual.ImageStim(win, 'avatar.png', pos=[-300, -230], size = [50, 100])
group6 = visual.ImageStim(win, 'avatar.png', pos=[-450, -230], size = [50, 100])

##-------------------------------------------------
## Experiment
##-------------------------------------------------

message.text = 'Welcome to the experiment!\nPress spacebar when you are ready to start'
message.draw()
win.flip()
event.waitKeys(keyList = ['space'])

# Creating a for loop, at each iteration of the loop one trial from the list of
# trials we generated with the trialHandler is selected, in a sequential order

for trial in trials:
    print('Trial ', trials.thisTrialN, ': ', trial)   # print the conditions of the current trial in the output
    
    ## block instructions
    # displaying the instructions for the block
    # we use the attribute of the trialHandler .thisTrialN which keeps
    # track of the number of the current trial. 

    if (trials.thisTrialN == 0 or trials.thisTrialN == 128):
        Practice = 1
        PauseCount = 0
        if trial['instrBehav'] == 'approachHappy':
            message.color = 'white'
            message.text = 'If the face is happy, press the up arrow key.\nIf the face is angry, press the down arrow key.\n\n\nPress the spacebar when you are ready to start the practice.'

        elif trial['instrBehav'] == 'approachAngry':
            message.color = 'white'
            message.text = 'If the face is angry, press the up arrow key.\nIf the face is happy, press the down arrow key.\n\n\nPress the spacebar when you are ready to start the practice.'
        
        message.draw()
        win.flip()
        event.waitKeys(keyList = ['space'])

    elif (trials.thisTrialN == 8 or trials.thisTrialN == 136):
        Practice = 0
        PauseCount = 0
        message.color = 'white'
        message.text = 'You have completed the Practice.\nPress the spacebar when you are ready to start the Task'
        message.draw()
        win.flip()        
        event.waitKeys(keyList = ['space'])

    ## make all avatars appear in the starting positions

    # setting positions
    group1.pos = [150, -230]
    group2.pos = [300, -230]
    group3.pos = [450, -230]
    group4.pos = [-150, -230]
    group5.pos = [-300, -230]
    group6.pos = [-450, -230]
    avatar.pos = [0, -200]
    
    # drawing avatars
    avatar.draw()
    group1.draw()
    group2.draw()
    group3.draw()
    group4.draw()
    group5.draw()
    group6.draw()
    
    win.flip()
    core.wait(1)

    ## make the face stimulus appear
    # which image to display is selected based on the value of 'stimValence'
    # for the current trial
    
    if trial['stimValence'] == 'happy':
        happy.draw()
    elif trial['stimValence'] == 'angry':
        angry.draw()

    avatar.draw()
    group1.draw()
    group2.draw()
    group3.draw()
    group4.draw()
    group5.draw()
    group6.draw()
    
    win.flip()

    # we initialize a clock to record the response time
    # we do it here because we want RTs to be time locked to face stimulus onset
    clock = core.Clock() 
    
    core.wait(0.1) # wait 100 ms
    
    ## make the group move
    # the direction in which the group moves depends on the value of
    # trial['groupBehav'] for the current trial
    
    # define the displacement for the movement of the group
    # a movement is defined as a displacement on the y axis
    approach_mov = [0, +100]  
    avoid_mov = [0, -100]
    
    if trial['groupBehav'] == 'approach':
        
        # the position of the avatars is increased of 100 pixels on the y axis
        group1.pos += approach_mov
        group2.pos += approach_mov
        group3.pos += approach_mov
        group4.pos += approach_mov
        group5.pos += approach_mov
        group6.pos += approach_mov
    
    elif trial['groupBehav'] == 'avoid':

        # the position of the avatars is decreased of 100 pixels on the y axis
        group1.pos += avoid_mov
        group2.pos += avoid_mov
        group3.pos += avoid_mov
        group4.pos += avoid_mov
        group5.pos += avoid_mov
        group6.pos += avoid_mov
    
    if trial['stimValence'] == 'happy':
        happy.draw()
    elif trial['stimValence'] == 'angry':
        angry.draw()
    
    avatar.draw()
    group1.draw()
    group2.draw()
    group3.draw()
    group4.draw()
    group5.draw()
    group6.draw()
    
    win.flip()
    
    ## collect response from participant
    # we set a maximum response deadline of 2 seconds, and wait for a button
    # press of one of the two allowed_keys options
    event.clearEvents()
    max_dur = 2
    allowed_keys = ['up', 'down']
    
    event.clearEvents() # deleting button presses still in memory
    keys = event.waitKeys(max_dur, keyList = allowed_keys, timeStamped = clock)

    # keys is a list of button presses. We want to look at the first one.
    # if a button press was provided within the deadline, keys will contain a tuple
    # keys[0][0] contains the value of the pressed button
    # keys[0][1] contains the RT in seconds
    # print('Pressed button: ', keys[0][0])
    # print('RT: ', keys[0][1] * 1000, ' ms')
    
    ## make the participant avatar move
    
    # if no button press was given within the deadline, keys is equal to None
    if keys == None:
        avatar.pos = [0, -200] # no movement
    # changing position of the participant avatar depending on the button pressed
    elif keys[0][0] == 'up':
        avatar.pos += [0, 100]
    elif keys[0][0] == 'down':
        avatar.pos += [0, -100]
    
    if trial['stimValence'] == 'happy':
        happy.draw()
    elif trial['stimValence'] == 'angry':
        angry.draw()
    
    avatar.draw()
    group1.draw()
    group2.draw()
    group3.draw()
    group4.draw()
    group5.draw()
    group6.draw()
    
    win.flip()
    core.wait(0.5)
    
    ## Add data to output
    if keys != None:
        trials.addData('RT', keys[0][1])
        trials.addData('Response', keys[0][0])
    trials.addData('Practice', Practice)
    
    ## Feedback
    if Practice == 1:
        if keys == None:
            message.text = 'Respond faster!'
            message.color = 'white'
            message.draw()
        elif (trial['stimValence'] == 'happy' and trial['instrBehav'] == 'approachHappy' and keys[0][0] == 'up'):
            message.text = 'Correct!'
            message.color = 'green'
            message.draw()
        elif (trial['stimValence'] == 'angry' and trial['instrBehav'] == 'approachAngry' and keys[0][0] == 'up'):
            message.text = 'Correct!'
            message.color = 'green'
            message.draw()
        elif (trial['stimValence'] == 'happy' and trial['instrBehav'] == 'approachAngry' and keys[0][0] == 'down'):
            message.text = 'Correct!'
            message.color = 'green'
            message.draw()
        elif (trial['stimValence'] == 'angry' and trial['instrBehav'] == 'approachHappy' and keys[0][0] == 'down'):
            message.text = 'Correct!'
            message.color = 'green'
            message.draw()
        else:
            message.text = 'Wrong!'
            message.color = 'red'
            message.draw()
    
        win.flip()
        core.wait(1)

    PauseCount += 1
    
    ## ISI 
    # blank interval between trials
    win.flip()
    core.wait(1)

    ## Pause
    if PauseCount == 30:
        message.color = 'white'
        message.text = 'This is a short break.\nPress spacebar when you are ready to continue.'
        message.draw()
        win.flip()
        event.waitKeys(keyList = ['space'])

    thisExp.nextEntry() # proceed to the next trial

message.color = 'white'
message.text = 'Congrats! You have completed the experiment.\nThank you!'
message.draw()
win.flip()
event.waitKeys(keyList = ['space'])
