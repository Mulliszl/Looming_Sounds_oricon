# home for functions definitions in the contrst & orientation experiment suite
from datetime import datetime
import pygame
import random
import time
import csv
import numpy as np
import random
from variables import *

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
                    scoring = 0
                    return True
                if key2 and pygame.key.name(event.key) == key2:
                    button = "Right"
                    scoring = 1
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


def add_noise(image, probability):
    width, height = image.get_size()
    noisy_image = pygame.Surface((width, height))
    for y in range(height):
        for x in range(width):
                r, g, b, a = image.get_at((x, y))
                if random.random() < probability:
                    # Set pixel to white
                    r = g = b = 255
                else:
                    # Set pixel to black
                    r = g = b = 0
                image.set_at((x, y), (r, g, b, a))
    global noise_stim
    return noise_stim


    
def intro(session, round):
    # Display introductory text
    draw_screen('Session ' +str(session + 1) + ': Starting Block ' + str(round) + ' of 6. Press any key to continue...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    time.sleep(.2)

def type(type,sound):
    # Display introductory text
    draw_screen('This block will be ' + str(type) + ' with ' +str(sound) + '. Press any key to begin...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    draw_screen(fix, background_color, black) # add fixation dot for first trial
    time.sleep(2 + random.uniform(0.0, 2.0))  # sleep for inter-trial interval
    

def end_session(session):
    # Display introductory text
    draw_screen('You finished Session ' +str(session + 1) + '! Please take a few minutes to rest before continuing', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    time.sleep(.2)


def practice_intro_c():
    # Display introductory text
    draw_screen('This practice block will help you learn the contrast task. Press any key to begin...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    draw_screen(fix, background_color, black) # add fixation dot for first trial
    time.sleep(2 + random.uniform(0.0, 2.0))  # sleep for inter-trial interval

def practice_intro_o():
    # Display introductory text
    draw_screen('This practice block will help you learn the orientation task. Press any key to begin...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    draw_screen(fix, background_color, black) # add fixation dot for first trial
    time.sleep(2 + random.uniform(0.0, 2.0))  # sleep for inter-trial interval


def threshold_intro():
    # Display introductory text
    draw_screen('This training block will help us customize the task. Press any key to begin...', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()
    draw_screen(fix, background_color, black) # add fixation dot for first trial
    time.sleep(2 + random.uniform(0.0, 2.0))  # sleep for inter-trial interval

def outro():
    # Display outro text
    draw_screen('That was the last set of trials. Thanks for participating in our experiment! ', background_color, black)
    wait('','', timeout_time)  # wait for keypress with basically infinite timeout time
    wipe()


def contrast(strength, numTrials):
    # Generate randomized trial order (one sound length/condition per block, 30 trials per block)
    # with 5 contrast levels, this means 6 of each contrast level per block
    global trialNum
    task_type = 'contrast'
    directionList = [1,2]*int(numTrials/2)
    contrast = [1,2,4,8,16]*int(numTrials)#/5)
    trials = []
    for c in range(0,50):  # prep contrast and direction values for Gabor patch
            trial = {
                'filename': '250Looming_' + str(strength) + '_Fade.wav',
                'contrast': contrast[c],
                'direction': directionList[c],
            }
            trials.append(trial)
            random.shuffle(trials)
    # Begin block of trials
    for trial in trials:
        # 8/28/23 PREVIOUS,
        # Gabor = pygame.image.load('Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']+1) + '.png')
        # img_presented = 'Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']+1) + '.png'
        Gabor = pygame.image.load('Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']) + '.png')
        img_presented = 'Contrast_' + str(trial['contrast']) + '_Direction_' + str(trial['direction']) + '.png'
        if trial['filename'] == '250Looming_-1_Fade.wav':
            pass
        else:
            sound = mixer.Sound('250Looming_' +str(strength) + '_Fade.wav')  # load the sound
            channel = sound.play()  # start playing on a channel
            while channel.get_busy():  # do nothing until the channel is done playing
                pass

        draw_screen(Gabor, background_color, black)  # display visual stim1ulus
        time.sleep(present_time_c)
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

        global trialNum
        trialNum = trialNum + 1
        print(trialNum)

        correctNumber = -10000000 #placeholder
        
        global presented_imgID
        if trial['direction'] == 1: # left
            correctNumber = 0
        if trial['direction'] == 2: # right
            correctNumber = 1
            
        if correctNumber == scoring: # a higher contrastID is lower contrast (harder to see/better performance)
            correct = 1
        else:
            correct = 0

        log[(participant_ID, task_type, present_time_c, blockNum, strength, trialNum, img_presented, trial['direction'], trial['contrast'], button, correct,)] = response_time  # 
        with open(timestamp, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(log.items())
        time.sleep(ISI)  # sleep for inter-trial interval 
        print('correct? ', correct)
        print('selected: ', button  )
        
def orientation(strength, numTrials):
    task_type = 'orientation'
    directionList = [1,2]*int(numTrials/2)
    orientation = [1, 2, 3, 4, 5]*int(numTrials)#/5
    trials = []
    for c in range(0,50):  # prep contrast and direction values for Gabor patch
            trial = {
                'filename': '250Looming_' + str(strength) + '_Fade.wav',
                'orientation': orientation[c],
                'direction': directionList[c],
            }
            trials.append(trial)
            random.shuffle(trials)
    # Begin block of trials
    for trial in trials:
        Gabor = pygame.image.load('Orientation_' + str(trial['orientation']) + '_Direction_' + str(trial['direction']) + '.png')
        img_presented = 'Orientation_' + str(trial['orientation']) + '_Direction_' + str(trial['direction']) + '.png'
        if trial['filename'] == '250Looming_-1_Fade.wav':
            pass
        else:
            sound = mixer.Sound('250Looming_' +str(strength) + '_Fade.wav')  # load the sound
            channel = sound.play()  # start playing on a channel
            while channel.get_busy():  # do nothing until the channel is done playing
                pass
        # prepare the visual stimulus for this trial
        presented_img = 'placeholder' # placeholder
        add_noise(noise_stim, .5)
        draw_screen(Gabor, background_color, black)  # display visual stim1ulus
        time.sleep(present_time_o)
        wipe()
        draw_screen(noise_stim, background_color, black)
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

        global trialNum
        trialNum = trialNum + 1
        print(trialNum)

        correctNumber = -10000000 #placeholder
        global presented_imgID
        if trial['direction'] == 1: # left
            correctNumber = 0
        if trial['direction'] == 2: # right
            correctNumber = 1
            
        if correctNumber == scoring: # a higher contrastID is lower contrast (harder to see/better performance)
            correct = 1
        else:
            correct = 0

        log[(participant_ID, task_type, present_time_o, blockNum, strength, trialNum, img_presented, trial['direction'], trial['orientation'], button, correct,)] = response_time  # 
        with open(timestamp, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(log.items())
        time.sleep(ISI)  # sleep for inter-trial interval 
        print('correct? ', correct)
        print('selected: ', button  )
        
def ori_practice_block():
    # Generate randomized trial order (one sound length/condition per block, 2 trials per block)
    # with 5 contrast levels, this means 6 of each contrast level per block
    global present_time_o
    strength = 'placeholder'
    task_type = 'orientation'
    if present_time_o ==  .4:
        practice_intro_o()
    else:
        threshold_intro()
    ori_practice_correct = 0
    practice_trial = 0
    directionList = [0,1]*6
    random.shuffle(directionList)
    orientation = [5,5]*6
    sounds = ["1", "32", "-1","1", "32", "-1","1", "32", "-1","1", "32", "-1"]
    trials = []
    for c in range(0,12):  # prep contrast and direction values for Gabor patch
            trial = {
                'filename': '250Looming_' + str(sounds[c]) + '_Fade.wav',
                'orientation': orientation[c],
                'direction': directionList[c],
            }
            trials.append(trial)
            random.shuffle(trials)
    # Begin block of trials
    for trial in trials:
        Gabor = pygame.image.load('Orientation_' + str(trial['orientation']) + '_Direction_' + str(trial['direction']+1) + '.png')
        img_presented = 'Orientation_' + str(trial['orientation']) + '_Direction_' + str(trial['direction']+1) + '.png'
        if trial['filename'] == '250Looming_-1_Fade.wav':
            pass
        else:
            sound = mixer.Sound(trial['filename'])  # load the sound
            channel = sound.play()  # start playing on a channel
            while channel.get_busy():  # do nothing until the channel is done playing
                pass

        add_noise(noise_stim, .5)
        draw_screen(Gabor, background_color, black)  # display visual stim1ulus
        time.sleep(present_time_o)
        wipe()
        draw_screen(noise_stim, background_color, black)
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

        practice_trial = practice_trial + 1
        print(practice_trial)


        if trial['direction'] == scoring: # a higher orienttID is lower orient (harder to see/better performance)
            correct = 1
        else:
            correct = 0
        if correct == 1:
            ori_practice_correct = ori_practice_correct + 1
        log[(participant_ID, task_type, present_time_o, blockNum, strength, practice_trial, img_presented, trial['direction'], trial['orientation'], button, correct,)] = response_time  # 
        with open(timestamp, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(log.items())
        time.sleep(ISI)  # sleep for inter-trial interval 
        print('correct? ', correct)
        print('selected: ', button)        

    print('Accuracy = ' + str(ori_practice_correct/12))
    
    next_time = -100 # placeholder
    if present_time_o == .4:    # after first threshold round, automatically set next round to .1
        next_time = .1
    
    # after first prctice round (block 2), if participant achieved 75%, set to 75ms
    if present_time_o == .1:
        if (ori_practice_correct/12) > .75: 
            next_time = .075
        else:
            next_time = .125 # otherwise set time to 125ms
    
    # after second practice round (block 3) if participant achieved 75%, set to 75 for full experiment
    if present_time_o == .075:
        if (ori_practice_correct/12) > .75: 
            next_time = 0.075
        else:
            next_time = 0.1 # otherwise, if accuracy < 75% go with 100ms
    
    # after second practice round (block 3) if participant achieved 75%, set to 100 for full experiment        
    if present_time_o == .125:
        if (ori_practice_correct/12) > .75: 
            next_time = .1
        else: 
            next_time = .125 # otherwise, if accuracy < 75% go with 125ms
    
    present_time_o = next_time
    
    
    
def con_practice_block():
    # Generate randomized trial order (one sound length/condition per block, 2 trials per block)
    # with 5 contrast levels, this means 6 of each contrast level per block
    global present_time_c
    strength = 'placeholder' # this is here to keep the data sheets clean
    task_type = 'contrast'
    if present_time_c == .4:
        practice_intro_c()
    else:
        threshold_intro()
    con_practice_correct = 0
    practice_trial = 0
    directionList = [0,1]*6
    random.shuffle(directionList)
    contrast = [16,16]*6
    trials = []
    sounds = ["1", "32", "-1","1", "32", "-1","1", "32", "-1","1", "32", "-1"]
    for c in range(0,12):  # prep contrast and direction values for Gabor patch
            trial = {
                'filename': '250Looming_' + str(sounds[c]) + '_Fade.wav',
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
            sound = mixer.Sound(trial['filename'])  # load the sound
            channel = sound.play()  # start playing on a channel
            while channel.get_busy():  # do nothing until the channel is done playing
                pass

        draw_screen(Gabor, background_color, black)  # display visual stim1ulus
        time.sleep(present_time_c)
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

        practice_trial = practice_trial + 1
        print(practice_trial)


        if trial['direction'] == scoring: 
            correct = 1
        else:
            correct = 0
        if correct == 1:
            con_practice_correct = con_practice_correct + 1
        log[(participant_ID, task_type, present_time_c, blockNum, strength, practice_trial, img_presented, trial['direction'], trial['contrast'], button, correct,)] = response_time  # 
        with open(timestamp, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(log.items())
        time.sleep(ISI)  # sleep for inter-trial interval 
        print('correct? ', correct)
        print('selected: ', button)        

    print('Accuracy = ' + str(con_practice_correct/12))
    
    next_time = -100 # placeholder
    if present_time_c == .4:    # after first threshold round, automatically set next round to .1
        next_time = .1
    
    # after first prctice round (block 2), if participant achieved 75%, set to 75ms
    if present_time_c == .1:
        if (con_practice_correct/12) > .75: 
            next_time = .075
        else:
            next_time = .125 # otherwise set time to 125ms
    
    # after second practice round (block 3) if participant achieved 75%, set to 75 for full experiment
    if present_time_c == .075:
        if (con_practice_correct/12) > .75: 
            next_time = 0.075
        else:
            next_time = 0.1 # otherwise, if accuracy < 75% go with 100ms
    
    # after second practice round (block 3) if participant achieved 75%, set to 100 for full experiment        
    if present_time_c == .125:
        if (con_practice_correct/12) > .75: 
            next_time = .1
        else: 
            next_time = .125 # otherwise, if accuracy < 75% go with 125ms'''
            
            
    print(next_time)
    print(present_time_c)
    
    present_time_c = next_time
    
    print(present_time_c)
