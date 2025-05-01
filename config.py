# Path to the ChromeDriver
CHROME_DRIVER_PATH = '/opt/homebrew/bin/chromedriver'  # Update with the actual path to your chromedriver
TRIALS_HISTORY_PATH = 'trials/breakbad_trials.csv'  # Path to save the scoreboard
HEADDLESS_MODE = True
# HEADDLESS_MODE = False

# Game URL
GAME_URL = 'https://dysruption.net/scenario/8857adb7-42ff-4c4f-8ca3-1693aa830367/0'  # Update with the actual game URL

# GAME CONFIG
NUM_TRIALS = 500
MAX_ATTACKS = 17
ATTACKS_ALLOWED = 5
# DETAILED_STATE = False  # Set to True for detailed state information
EDGE_DETAILED_STATE = True
NODE_DETAILED_STATE = False

# Bot Options
# BOT_INTELLIGENCE = "dumb" # "not_dumb", "intelligent"
BOT_INTELLIGENCE = "not_dumb" # "not_dumb", "intelligent"