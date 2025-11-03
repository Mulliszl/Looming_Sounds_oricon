from datetime import datetime
import pygame
import random
import time
import csv
import numpy as np
import random

######### UPDATE ME EVERY PARTICIPANT PLEASE :) #######################
participant_ID = -1
#######################################################################
'''-----------------------'''
present_time = .075 # time stimulus is on screen - ADJUST THIS FOR TEST - 0.075, .1, .125
noise_time = .05       # time noise is on screen
'''-----------------------'''
timeout_time = 11600    # time before menu times out and block begins automatically
wait_for_input_time = 2000 # time waiting for input
sleep_time = 0.2        # time for post-trial blacksquare on screen
ISI = 2 + random.uniform(0.0, 2.0)  #time between trials'''

total_correct = 0
#os.chdir("C:/Users/yingchenhe/Desktop/TMS Study F2022/Contrast Sensitivity for TMS Study - Gabor patches & audio")
# Pygame constants and necessary code
# Pygame constants and necessary code
pygame.init()  # start pygame
mixer = pygame.mixer  # start audio mixer
mixer.init()
resolution = (1920, 1080)  # screen resolution
screen = pygame.display.set_mode(resolution)  # create display
pygame.mouse.set_visible(False)  # hide the mouse
black = (0, 0, 0)  # color codes for later use
white = (255, 255, 255)
grey = (127, 127, 127)
font = pygame.font.SysFont("Arial", 50)  # set font and size
response_time = 2
background_color = grey
greysquare = pygame.image.load('greysquare.png')
noise_patch = pygame.image.load('Mask 3.png')

#test = 32

blockNum = 1
trialNum = 0
fix = pygame.image.load("fixation_cross.png")
presented_img_list = []
button = 'placeholder - no press'


# Draw content to center of screen (currently just text only)
def draw_screen(content, screen_color, content_color):
    center = (screen.get_width() // 2, screen.get_height() // 2)

    screen.fill(screen_color)
    if isinstance(content, str):
        text = font.render(content, True, content_color)
        text_rect = text.get_rect(center=center)
        screen.blit(text, text_rect)
    else:
        rect = content.get_rect(center=center)
        screen.blit(content, rect)

    pygame.display.update()

# Wait for KEY keypress, then return
def wait(key, key2, t):
    global button
    global scoring
    global trialNum
    global correctAnswer
    scoring = -1 # default for 'no button press'
    pygame.event.clear()
    start = time.time()
    while time.time() - start < t:  # loop until timout t is hit
        # gets a single event from the event queue
        events = pygame.event.get()
        for event in events:
            # captures the 'KEYDOWN'
            if event.type == pygame.KEYDOWN:
                # gets the key name
                if key and pygame.key.name(event.key) == key:
                    button = "Left"
                    scoring = 1
                    return True
                if key2 and pygame.key.name(event.key) == key2:
                    button = "Right"
                    scoring = 2
                    return True
                elif not key and key != '5':  # 5 is the emergency stop key
                    button = '-1'
                    return True
            elif event.type == pygame.NOEVENT:  # if we hit the timeout
                return False
            else:  # we don't care about any other event types
                pass


def wipe():
    draw_screen(greysquare, background_color, black)

    
def intro():
    # Display introductory text
    draw_screen('This practice block will help you learn the task. Press any key to begin...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    draw_screen(fix, background_color, black) # add fixation cross for first trial
    time.sleep(2 + random.uniform(0.0, 2.0))  # sleep for inter-trial interval


def outro():
    # Display outro text
    draw_screen('That was the last set of trials. Thanks for participating in our experiment! ', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()


def block(strength, wait_times):
    # Generate randomized trial order (one sound length/condition per block, 2 trials per block)
    # with 5 contrast levels, this means 6 of each contrast level per block
    global trialNum
    global total_correct
    directionList = [0,1]*7
    random.shuffle(directionList)
    contrast = [16,16]*7
    trials = []
    for c in range(0,2):  # prep contrast and direction values for Gabor patch
            trial = {
                'filename': '250Looming_' + str(strength) + '_Fade.wav',
                'contrast': contrast[c],
                'direction': directionList[c],
            }
            trials.append(trial)
            random.shuffle(trials)
    # Begin block of trials
    for trial in trials:
        Gabor = pygame.image.load('Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']+1) + '.png')
        img_presented = 'Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']+1) + '.png'
        if trial['filename'] == '250Looming_-1_Fade.wav':
            pass
        else:
            sound = mixer.Sound('250Looming_' +str(strength) + '_Fade.wav')  # load the sound
            channel = sound.play()  # start playing on a channel
            while channel.get_busy():  # do nothing until the channel is done playing
                pass
        # prepare the visual stimulus for this trial
        presented_img = 'placeholder' # placeholder

        draw_screen(Gabor, background_color, black)  # display visual stim1ulus
        time.sleep(present_time)
        wipe()
        draw_screen(noise_patch, background_color, black)
        time.sleep(noise_time)
        wipe()

        start = time.time()  # log start of response window
        if wait('q','p', wait_for_input_time):  # wait for input, max 2 seconds
            end = time.time()  # log end of response window
            response_time = int(round((end - start) * 1000, 0))  # calculate trial RT in ms, convert it to integer
            time.sleep(sleep_time)
        else:  # if False, then >2 seconds elapsed
            response_time = -1  # set RT to -1, participant did not respond 
            time.sleep(sleep_time)
        # print(response_time) # for testing, prints response time in terminal
        wipe()
        draw_screen(fix, background_color, black)

        trialNum = trialNum + 1
        print(trialNum)

        global presented_imgID
        if trial['direction'] == 0: # right
            correctNumber = 1
        if trial['direction'] == 1: # left
            correctNumber = 2
            
        if correctNumber == scoring: # a higher contrastID is lower contrast (harder to see/better performance)
            correct = 1
        else:
            correct = 0
        if correct == 1:
            total_correct = total_correct + 1
        log[(participant_ID, blockNum, strength, trialNum, img_presented, trial['direction'], trial['contrast'], button, correct,)] = response_time  # 
        with open(timestamp, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(log.items())
        time.sleep(ISI)  # sleep for inter-trial interval 
        print('correct? ', correct)
        print('selected: ', button  )
# The Actual Experiment begins here:

log = {}  # data will be saved to a log dictionary object
# Study is composed of 7 sessions, each with 5 blocks
# four sound conditions - 30 trials per block w/ 5 contrast levels - 6 trials per block
        # need 30

allBlocks = ["1", "32", "-1", "1", "-1", "32"]*2 # -1 is no sound

timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")

# create data file & write column headers
log[('participant_ID', 'blockNum','looming_strength', 'trialNum', 'img_presented', 'stimulus_direction', 'contrast', 'selected_input', 'correct?')] = 'response_time'  # 
with open(timestamp, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(log.items())
# 5 sessions, each with 7 audio blocks
intro()
for sessions in range(0, 1):
    # Each with 7 blocks
    allBlocks = ["1", "32", "-1", "1", "-1", "32"]
    blockShuffle = np.random.permutation(len(allBlocks))
    for blocks in range(0, 6):
        block(allBlocks[blockShuffle[blocks]], .4)  # run a non-training block for data collection
        blockNum = blockNum + 1
print('Accuracy = ' + str(total_correct/12))
# then close pygame
pygame.quit()