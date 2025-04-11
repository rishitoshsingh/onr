from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config
print(f"PLaying as {config.BOT_INTELLIGENCE} bot")


from src.game import BreakItBad
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

game = BreakItBad(driver, config.BOT_INTELLIGENCE, config.GAME_URL, config.EDGE_DETAILED_STATE, config.NODE_DETAILED_STATE)
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
    for i in range(config.ATTACKS_ALLOWED):
        game.get_state()
        edge = game.attack()
        score = game.get_score()
        current_moves.append(edge.get_edge_from_to())
        current_scoreboard.append(score)
        if (game.is_game_over()):
            break
    current_scoreboard = current_scoreboard + [None] * (config.MAX_ATTACKS - len(current_scoreboard))
    current_moves = current_moves + [None] * (config.MAX_ATTACKS - len(current_moves))
    trial_record = current_moves + current_scoreboard
    save_trials_to_csv(trial_record, config.TRIALS_HISTORY_PATH)
    game.reset_game()

# Ensure the file is properly closed before analyzing
metrics.analyze_scoreboard(config.TRIALS_HISTORY_PATH, config.ATTACKS_ALLOWED)