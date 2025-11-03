# variables for orientation_contrast_task
from datetime import datetime
import pygame
import random
import numpy as np
import random

'''timeout_time = 11600    # time before menu times out and block begins automatically
noise_time = .05       # time noise is on screen
present_time_o = .4    # time stimulus is on screen - we start this at 400ms for practice, then automatically adjust during thresholding
present_time_c = .4    # final experimental presentation times will be 75ms, 100ms, or 125ms
wait_for_input_time = 9999999999 # time waiting for input
sleep_time = 0.002        # sleep
ISI = 1 + random.uniform(0.0, 1.0)  #time between trials'''

'''# Time values for rapid testing
timeout_time = .0001    # time before menu times out and block begins automatically
noise_time = 0.0001        # time noise is on screen
present_time_o = .000001    # time stimulus is on screena
present_time_c = .000001      # time stimulus is on screen
wait_for_input_time = 0.0001 # time waiting for input
sleep_time = 0.0001      # sleep
ISI = 0.0001  #time between trials'''

# pres_time for PSeebold
timeout_time = 11600    # time before menu times out and block begins automatically
noise_time = .05       # time noise is on screen
present_time_o = .075    # time stimulus is on screen - we start this at 400ms for practice, then automatically adjust during thresholding
present_time_c = .1    # final experimental presentation times will be 75ms, 100ms, or 125ms
wait_for_input_time = 9999999999 # time waiting for input
sleep_time = 0.002        # sleep
ISI = 1 + random.uniform(0.0, 1.0)  #time between trials'''

# Time values for rapid testing (including practice blocks, which will reset present_time_o & _c)
'''timeout_time = 0.0001    # time before menu times out and block begins automatically
noise_time = 0.0001        # time noise is on screen
present_time_o = .4       # time stimulus is on screena
present_time_c = .4      # time stimulus is on screen
wait_for_input_time = 0.0001 # time waiting for input
sleep_time = 0.0001      # sleep
ISI = 0.0001  #time between trials'''


#placeholder participant ID
participant_ID = -100

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
noise_stim = pygame.image.load('noise_circle.png')
blockNum = 1
trialNum = 0
fix_cross = pygame.image.load("fixation_cross.png")
fix = pygame.image.load("fixation_dot.png")
presented_img_list = []
button = 'placeholder - no press'



log = {}
timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")