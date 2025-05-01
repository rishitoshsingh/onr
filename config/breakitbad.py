# Path to the ChromeDriver (download the chromedriver, and give the path to it)
CHROME_DRIVER_PATH = '/opt/homebrew/bin/chromedriver'  # Update with the actual path to your chromedriver

# Path where the bot will save the scores and actions for each game
TRIALS_HISTORY_PATH = 'trials/breakbad_trials.csv'  # Path to save the scoreboard
# Whether you want to view the game being played the bot (True) or not (False)
# If set to True, the bot will play games in background, and no chrome window will be opened
# If set to False, the bot will play games in headless mode, and a chrome window will be opened
HEADDLESS_MODE = True
# HEADDLESS_MODE = False

# Game URL (don't change)
GAME_URL = 'https://dysruption.net/scenario/8857adb7-42ff-4c4f-8ca3-1693aa830367/0'  # Update with the actual game URL

# GAME CONFIG
# number of games bot will play
NUM_TRIALS = 500
# Maximum number of attacks allowed in a game (don't change)
MAX_ATTACKS = 17
# Maximmum number of attacks you want bot to make in a single game (set to 5, because that's what leaderboard shows)
ATTACKS_ALLOWED = 5
# Whether to extract Edge and Node detailed state (Break It Bad only requires Edge detailed state to be extracted)
# (don't change)
EDGE_DETAILED_STATE = True
NODE_DETAILED_STATE = False

# Bot Options (either dumb, or not_dumb)
BOT_INTELLIGENCE = "not_dumb" # "not_dumb"