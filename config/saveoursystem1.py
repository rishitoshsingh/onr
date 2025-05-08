# Path to the ChromeDriver
CHROME_DRIVER_PATH = '/opt/homebrew/bin/chromedriver'  # Update with the actual path to your chromedriver
TRIALS_HISTORY_PATH = 'trials/saveoursystem1_trials.csv'  # Path to save the scoreboard
HEADDLESS_MODE = True
# HEADDLESS_MODE = False

# Game URL
GAME_URL = 'https://dysruption.net/scenario/49d1908f-c4c9-41cb-bee5-3ec450d1ade7/2'  # Update with the actual game URL

# GAME CONFIG
NUM_TRIALS = 10
MAX_TURNS = 10
TURNS_ALLOWED = 10
# DETAILED_STATE = False  # Set to True for detailed state information
EDGE_DETAILED_STATE = True
NODE_DETAILED_STATE = False

# Bot Options
# BOT_INTELLIGENCE = "dumb" # "not_dumb", "intelligent"
# BOT_INTELLIGENCE = "only_maintain"
# BOT_INTELLIGENCE = "only_replace"
# BOT_INTELLIGENCE = "only_repair"
BOT_INTELLIGENCE = "weighted_random"

# random_threshold_actions = [0.3, 0.5, 0.7]
# import random
# RANDOM_THRESHOLD_ACTION = random.choice(random_threshold_actions)
# 30% chace the bot will take a random action
RANDOM_THRESHOLD_ACTION = 0.3