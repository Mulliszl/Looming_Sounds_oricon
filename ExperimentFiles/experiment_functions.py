# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 12:46:49 2025

@author: zach
"""

# experiment_functions.py
# This is the "engine" of your experiment.

import pygame
import random
import time
import csv
import numpy as np
from os.path import join 
from variables1 import * # Import all settings

# --- Core Pygame Functions ---
# (draw_screen, wait, show_text_screen, end_experiment are all UNCHANGED)

def draw_screen(content, screen_color, content_color, position="center"):
    screen.fill(screen_color)
    if position == "center":
        center_coords = (CENTER_X_POS, STIMULUS_Y_POS)
    elif position == "peripheral_left":
        center_coords = (PERIPHERAL_L_POS, STIMULUS_Y_POS)
    elif position == "peripheral_right":
        center_coords = (PERIPHERAL_R_POS, STIMULUS_Y_POS)
    else:
        center_coords = (CENTER_X_POS, STIMULUS_Y_POS)
    if isinstance(content, str):
        text = font.render(content, True, content_color)
        text_rect = text.get_rect(center=center_coords)
        screen.blit(text, text_rect)
    else:
        rect = content.get_rect(center=center_coords)
        screen.blit(content, rect)
    pygame.display.update()

def wait(key='f', key2='j', t=wait_for_input_time):
    global button, correct_response
    button = -1
    pygame.event.clear()
    start = time.time()
    while time.time() - start < t:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    button = 'f'
                    response_time = (time.time() - start) * 1000
                    return response_time, button
                elif event.key == pygame.K_j:
                    button = 'j'
                    response_time = (time.time() - start) * 1000
                    return response_time, button
                elif event.key == pygame.K_ESCAPE:
                    end_experiment()
    return -1, "TIMEOUT"

def show_text_screen(text):
    draw_screen(text, grey, white, position="center")
    while True:
        response_time, button = wait(key='f', key2=None, t=float('inf'))
        if button == 'f':
            break
    draw_screen("", black, black)
    time.sleep(0.5)

def end_experiment():
    pygame.quit()
    quit()

# --- Trial Generation ---
# (This function is UNCHANGED)
def generate_trial_list(num_repeats):
    """
    Creates a fully randomized, balanced trial list for a block.
    (5x2x3 = 30 conditions)
    """
    trials = []
    
    for aud in AUDITORY_CONDITIONS:
        for vis in VISUAL_CONDITIONS:
            for diff in DIFFICULTY_LEVELS:
                trial_details = {
                    'auditory': aud,
                    'visual': vis,
                    'difficulty': diff,
                    'stimulus_tilt': random.choice(['L', 'R']) 
                }
                trials.append(trial_details)
    
    full_trial_list = trials * num_repeats
    random.shuffle(full_trial_list)
    return full_trial_list

# --- Main Experiment Block ---

def run_orientation_block(log_filename, session_num, block_num, trial_list):
    """
    Runs a single block of the main experiment.
    ### UPDATED with SEQUENTIAL audio-visual logic ###
    """
    looming_sound_channel = pygame.mixer.find_channel()
    if looming_sound_channel is None:
        print("--- Audio Debug: Error! No free audio channel for LOOMING sound. ---")
        end_experiment()
    else:
        print(f"--- Audio Debug: Acquired looming_sound_channel {looming_sound_channel} ---")

    for trial_num_idx, trial_info in enumerate(trial_list):
        
        # Stop all sounds from the previous trial
        pygame.mixer.stop()

        trial_num = trial_num_idx + 1
        
        # --- 1. Get Trial Conditions ---
        aud_cond = trial_info['auditory'] 
        vis_cond = trial_info['visual']
        diff_cond = trial_info['difficulty']
        stim_tilt = trial_info['stimulus_tilt'] 
        
        # --- 2. Determine Stimuli ---
        
        sound_to_play = None 
        
        if aud_cond == "center_looming":
            sound_to_play = looming_mono_sound
            looming_sound_channel.set_volume(1.0, 1.0) # Center
            
        elif aud_cond == "side_looming":
            sound_to_play = looming_mono_sound
            if random.choice(['L', 'R']) == 'L':
                looming_sound_channel.set_volume(1.0, 0.0) # Left
            else:
                looming_sound_channel.set_volume(0.0, 1.0) # Right
        
        elif aud_cond == "center_stationary":
            sound_to_play = stationary_center_sound
            
        elif aud_cond == "side_stationary":
            if random.choice(['L', 'R']) == 'L':
                sound_to_play = stationary_left_sound
            else:
                sound_to_play = stationary_right_sound
        
        # (Visual Position logic is unchanged)
        if vis_cond == "foveal":
            visual_pos = "center"
        else: 
            visual_pos = random.choice(["peripheral_left", "peripheral_right"])
        
        # (Visual Stimulus Image logic is unchanged)
        tilt_filename = "Direction_1" if stim_tilt == 'L' else "Direction_2"
        difficulty_value = DIFFICULTY_MAP[diff_cond]
        img_filename = f"Orientation_{difficulty_value}_{tilt_filename}.png"
        full_img_path = join(ASSET_PATH, "Visual", img_filename)

        try:
            stimulus_image = pygame.image.load(full_img_path)
        except:
            print(f"Error: Could not load image file: {full_img_path}")
            end_experiment()
            
        correct_response = 'f' if stim_tilt == 'L' else 'j'

        # --- 3. Run Trial Sequence (SEQUENTIAL LOGIC) ---
        
        # a. Fixation
        draw_screen(fix_cross, grey, white, position="center")
        time.sleep(1.0) 
        
        ### START OF REPLICATION LOGIC ###
        
        # b. Play audio (if any) AND WAIT for it to finish
        if sound_to_play:
            print(f"--- Audio Debug: Trial {trial_num} ({aud_cond}): Playing sound... ---")
            
            channel_to_wait_on = None
            if aud_cond in ["center_looming", "side_looming"]:
                looming_sound_channel.play(sound_to_play)
                channel_to_wait_on = looming_sound_channel
            else:
                # Play stationary sound and get its channel
                channel_to_wait_on = sound_to_play.play()

            # --- THIS IS THE SEQUENTIAL LOGIC ---
            # Wait for the sound to finish playing before proceeding
            if channel_to_wait_on:
                while channel_to_wait_on.get_busy():
                    pass # Do nothing (as in original Seebold code)
            
            print(f"--- Audio Debug: Trial {trial_num} ({aud_cond}): ...Sound finished. ---")
            
        else:
            # This is a silent trial.
            # We do nothing and proceed immediately to the visual stimulus.
            # This replicates the original confound where silent trials are shorter.
            print(f"--- Audio Debug: Trial {trial_num} ({aud_cond}): This is a silent trial. ---")
        
        ### END OF REPLICATION LOGIC ###

        # c. Present visual stimulus (now happens *after* sound is done)
        draw_screen(stimulus_image, grey, white, position=visual_pos)
        time.sleep(present_time_o) # This is 0.075s
        
        # d. Noise mask
        draw_screen(noise_stim, grey, white, position=visual_pos)
        time.sleep(noise_time) # This is 0.05s
        
        # e. Blank screen (for response)
        draw_screen("", black, black)
        
        # f. Get response
        response_time, button = wait(key='f', key2='j', t=wait_for_input_time)
        
        # g. Inter-trial interval (black screen)
        time.sleep(ISI)
        
        # --- 4. Score and Log ---
        is_correct = 1 if (button == correct_response) else 0
        
        log_data = [
            participant_ID,
            session_num,
            block_num,
            trial_num,
            aud_cond, 
            vis_cond,
            visual_pos,
            diff_cond,
            stim_tilt,
            correct_response,
            button,
            is_correct,
            response_time
        ]
        
        with open(log_filename, 'a', newline='') as f:
            w = csv.writer(f)
            w.writerow(log_data)
            
        print(f"Trial {trial_num} complete. Correct: {is_correct} (Response: {button})")


# --- Practice Block ---
# (This function is unchanged)
def run_practice_block(log_filename):
    """
    Runs 10 trials with center_stationary sound
    """
    show_text_screen("Starting practice. Press 'f' for Left, 'j' for Right. Press 'f' to begin.")
    
    practice_trials = []
    for i in range(10):
        practice_trials.append({
            'auditory': 'center_stationary', # Practice with sound
            'visual': 'foveal',
            'difficulty': 'easy',
            'stimulus_tilt': random.choice(['L', 'R'])
        })
        
    random.shuffle(practice_trials)
    
    # Run the block (using the same main function!)
    # We log this with session=0, block=0
    run_orientation_block(log_filename, session_num=0, block_num=0, trial_list=practice_trials)

    show_text_screen("Practice complete. We will now begin the full experiment.")