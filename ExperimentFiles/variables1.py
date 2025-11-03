# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 14:12:49 2025

@author: zach
"""
# variables1.py
# Contains all settings, paths, and global variables.

import pygame
import random
import numpy as np
from os.path import join 
import time 

# --- Participant ID (will be set by main_experiment.py) ---
participant_ID = -100

# --- Timings ---
### TIMINGS UPDATED TO MATCH SEEBOLD'S FILE ###

timeout_time = 11600    # (This is not currently used in our new code)
noise_time = .05        # (This was already 0.05)
present_time_o = .075   # CHANGED: Was 0.125. This is your visual stimulus time.
wait_for_input_time = 9999999999 # CHANGED: Was 5000. Now effectively infinite.
sleep_time = 0.002      # (This is not currently used in our new code)
ISI = 1.0 + random.uniform(0.0, 1.0)  # (This is the same as before)

# --- Experiment Design Variables ---
AUDITORY_CONDITIONS = [
    "center_looming", 
    "center_stationary", 
    "side_looming", 
    "side_stationary", 
    "silent"
]
VISUAL_CONDITIONS = ["foveal", "peripheral"]
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

DIFFICULTY_MAP = {
    "easy": 5,
    "medium": 3,
    "hard": 1
}

# --- Asset Path ---
ASSET_PATH = "Assets"

# --- Pygame Globals (will be initialized later) ---
screen = None
font = None
fix_cross = None
noise_stim = None
resolution = (1920, 1080) # The window size
black = (0, 0, 0)
white = (255, 255, 255)
grey = (127, 127, 127)
mixer = None

looming_mono_sound = None
stationary_center_sound = None
stationary_left_sound = None
stationary_right_sound = None

# Screen Positions (calculated after screen is created)
CENTER_X_POS = None
STIMULUS_Y_POS = None
PERIPHERAL_X_OFFSET = 500
PERIPHERAL_L_POS = None
PERIPHERAL_R_POS = None


### FUNCTION TO INITIALIZE PYGAME ###
def initialize_pygame():
    """
    Initializes Pygame, creates the screen, and loads assets.
    """
    global screen, font, fix_cross, noise_stim, looming_mono_sound
    global stationary_center_sound, stationary_left_sound, stationary_right_sound
    global mixer, black, white, grey, resolution
    global CENTER_X_POS, STIMULUS_Y_POS, PERIPHERAL_L_POS, PERIPHERAL_R_POS
    
    print("--- Audio Debug: Calling pygame.mixer.pre_init(buffer=1024)... ---")
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    
    # --- Pygame Setup ---
    pygame.init()  
    mixer = pygame.mixer
    mixer.init() 
    print(f"--- Audio Debug: pygame.mixer.init() complete. Settings: {pygame.mixer.get_init()} ---")

    screen = pygame.display.set_mode(resolution) 
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont("Arial", 50)
    
    # --- Calculate Screen Positions ---
    CENTER_X_POS = screen.get_width() // 2
    STIMULUS_Y_POS = screen.get_height() // 2
    PERIPHERAL_L_POS = CENTER_X_POS - PERIPHERAL_X_OFFSET
    PERIPHERAL_R_POS = CENTER_X_POS + PERIPHERAL_X_OFFSET

    # --- Load Assets ---
    try:
        fix_cross = pygame.image.load(join(ASSET_PATH, "fixation_dot.png"))
        noise_stim = pygame.image.load(join(ASSET_PATH, "noise_circle.png")) 
    except:
        print(f"FATAL ERROR: Could not load 'fixation_dot.png' or 'noise_circle.png' from {ASSET_PATH}")
        pygame.quit()
        quit()

    # --- Load Audio Assets ---
    try:
        print(f"--- Audio Debug: Loading LOOMING sound... ---")
        looming_mono_sound = mixer.Sound(join(ASSET_PATH, "Auditory", "250Looming_32_Fade.wav"))
        looming_mono_sound.set_volume(1.0) 
        
        print(f"--- Audio Debug: Loading STATIONARY sounds... ---")
        stationary_center_sound = mixer.Sound(join(ASSET_PATH, "Auditory", "Stationary_1_75db.wav")) 
        stationary_center_sound.set_volume(1.0)
        
        stationary_left_sound = mixer.Sound(join(ASSET_PATH, "Auditory", "Stationary_1_75db_0.wav")) 
        stationary_left_sound.set_volume(1.0)
        
        stationary_right_sound = mixer.Sound(join(ASSET_PATH, "Auditory", "Stationary_1_75db_1.wav")) 
        stationary_right_sound.set_volume(1.0)

        print(f"--- Audio Debug: ...All sounds loaded. ---")

    except Exception as e:
        print("--- FATAL ERROR: Could not load sound file. ---")
        print(f"--- ERROR MESSAGE: {e} ---")
        pygame.quit()
        quit()