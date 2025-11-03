# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 12:46:49 2025

@author: zach
"""

# main_experiment.py
# This is your main file to run the experiment.

from datetime import datetime
import csv
import os
from os.path import join
import variables1 as v             # Import our variables file

# --- Experiment Settings ---
NUM_SESSIONS = 3
NUM_BLOCKS_PER_SESSION = 6
# Set how many times each condition is repeated per block
REPEATS_PER_CONDITION_PER_BLOCK = 5 

# (5 Audio x 2 Visual x 3 Difficulty) = 30 conditions
# Total trials per block = 30 * 5 = 150 trials
NUM_TRIALS_PER_BLOCK = 30 * REPEATS_PER_CONDITION_PER_BLOCK

# --- Participant Setup (MOVED TO TOP) ---
participant_ID = input("Enter Participant ID: ") or "-1"
include_practice = 1 # 1 for yes, 0 for no

# --- NEW: Initialize Pygame *AFTER* getting input ---
v.initialize_pygame()

# --- NOW set the global ID and import the rest ---
v.participant_ID = participant_ID # Set the global participant ID
import experiment_functions as ef  # <-- IMPORT MOVED HERE

# --- Log File Setup ---
DATA_FOLDER = "data_test" 

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created subfolder: {DATA_FOLDER}")

timestamp = datetime.now().strftime("%Y_%m_%d_%H%M")
base_filename = f"participant_{participant_ID}_{timestamp}.csv"
log_filename = join(DATA_FOLDER, base_filename) 

# Your log headers are still perfect and will capture the new audio conditions
log_headers = [
    'participant_ID', 
    'session', 
    'block', 
    'trial_num',
    'auditory_condition', # will now be e.g., "center_looming"
    'visual_condition',   
    'visual_location',    
    'difficulty',         
    'stimulus_tilt',      
    'correct_response',   
    'participant_response',
    'is_correct',
    'response_time'
]

# Write headers to the log
with open(log_filename, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(log_headers)

# --- Start Experiment ---
ef.show_text_screen("Welcome to the experiment. Press 'f' to begin practice.")

# --- Practice Blocks ---
if include_practice == 1:
    ef.run_practice_block(log_filename)
    # The text for this screen is now inside the function

# --- Main Experiment Loop ---
for session_num in range(1, NUM_SESSIONS + 1):
    for block_num in range(1, NUM_BLOCKS_PER_SESSION + 1):
        
        ef.show_text_screen(f"Session {session_num}/{NUM_SESSIONS}, Block {block_num}/{NUM_BLOCKS_PER_SESSION}. Press 'f' to start.")
        
        # This will now generate a list of 150 trials (30 conditions * 5 repeats)
        trial_list = ef.generate_trial_list(REPEATS_PER_CONDITION_PER_BLOCK)
        
        ef.run_orientation_block(
            log_filename,
            session_num,
            block_num,
            trial_list
        )
        
        if (session_num == NUM_SESSIONS) and (block_num == NUM_BLOCKS_PER_SESSION):
            continue 
        ef.show_text_screen("Block complete. Take a short break. Press 'f' to continue.")

ef.show_text_screen("Experiment complete. Thank you!")
ef.end_experiment()