from datetime import datetime
import random
import csv
from function_def import *


######### UPDATE ME EVERY PARTICIPANT PLEASE :) #######################
participant_ID = -1
#######################################################################

include_practice = 0 # <-- Used for rapid iteration prototyping -  1 for yes, 0 for no
log = {}  # data will be saved to a log dictionary object

# Study is composed of 3 sessions, each with 6 blocks
# three sound conditions - 50 trials per block w/ 5 visual levels - 10 iterations of each visual level per block, 5 left, 5 right

allBlocks = ["1", "32", "-1"]*2 # -1 is no sound - this time we only have 3 blocks of 50 trials per condition
timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")

# create data file & write column headers
log[('participant_ID', 'task_type', 'present_time','blockNum','looming_strength', 'trialNum', 'img_presented', 'stimulus_direction', 'contrast/orientation', 'selected_input', 'correct?')] = 'response_time'      
with open(timestamp, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(log.items())
    
# first, we run the pre-blocks - 1 practice and 2 threshold blocks per trial condition
if include_practice == 1:
    for sessions in range(0, 3):
        ori_practice_block()
            
    for sessions in range(0, 3):
        con_practice_block()
else:
    pass    

# Then beging the main experiment - 3 sessions, each with 6 audio blocks
for sessions in range(0, 3):
    # Each with 6 blocks - build a dictionary in which task type and sound condition are linked to ensure balanced design, then shuffle
        blockNum = 1
        keys = ['Orient_Looming', 'Orient_Stationary', 'Orient_NoSound']*2#, 'Contrast_Looming','Contrast_Stationary', 'Contrast_NoSound']
        values = [('orient', 32), ('orient', 1), ('orient', -1), ('contrast', 32), ('contrast', 1), ('contrast', -1)]
        allBlocks = {key: values for key,values in zip(keys,values)}
        blockShuffle = random.shuffle(keys)
        for blocks in keys:
            intro(sessions, blockNum)
            block_stats = allBlocks[blocks]
            if values[1] == -1:
                sound = 'no sounds'
            else:
                if values[1] == 1:
                    sound = 'stationary sounds'
                else:
                    sound = 'looming sounds'

            if block_stats[0] == 'orient':
                type('orientation',sound)
                orientation(block_stats[1], 50)
            elif block_stats[0] == 'contrast':
                type('contrast', sound)
                orientation(block_stats[1], 50)
            blockNum = blockNum + 1
        end_session(sessions)
        
# Once we're done, say bye bye
outro()
