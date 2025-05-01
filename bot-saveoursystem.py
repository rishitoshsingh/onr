from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config.saveoursystem1 as config
print(f"PLaying as {config.BOT_INTELLIGENCE} bot")


from src.game import SaveOurSystem
import src.utils.metrics as metrics
from src.utils import save_trials_to_csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
if config.HEADDLESS_MODE:
    chrome_options.add_argument("--headless")

# Set up the Chrome driver
service = Service(config.CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
config.TRIALS_HISTORY_PATH = "_".join([config.TRIALS_HISTORY_PATH.split(".")[0], config.BOT_INTELLIGENCE])+".csv"

game = SaveOurSystem(driver, config.BOT_INTELLIGENCE, config.GAME_URL, config.EDGE_DETAILED_STATE, config.NODE_DETAILED_STATE, config.RANDOM_THRESHOLD_ACTION)
game.login()

import os
already_played_games_count = 0
if os.path.exists(config.TRIALS_HISTORY_PATH):
    with open(config.TRIALS_HISTORY_PATH, 'r') as f:
        lines = f.readlines()
        already_played_games_count = len(lines)-1
    print(f"Already played games: {already_played_games_count}")
games_scoreboard = None

current_moves, current_scoreboard = [], []
for i in range(config.NUM_TRIALS):
    print(f"Playing Trial: {already_played_games_count+i+1}")
    current_moves, current_scoreboard = [], []
    game.start_game()
    # game.get_state()
    for i in range(config.TURNS_ALLOWED):
        game.get_state()
        actions = game.action()
        score = game.get_score()
        current_moves.append(actions)
        current_scoreboard.append(score)
        # if (game.is_game_over()):
        #     break
    current_scoreboard = current_scoreboard + [None] * (config.MAX_TURNS - len(current_scoreboard))
    current_moves = current_moves + [None] * (config.MAX_TURNS - len(current_moves))
    trial_record = current_moves + current_scoreboard
    save_trials_to_csv(trial_record, config.TRIALS_HISTORY_PATH, sep=";")
    game.reset_game()

# Ensure the file is properly closed before analyzing
metrics.analyze_scoreboard_save_our_system(config.TRIALS_HISTORY_PATH)