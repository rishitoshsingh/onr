from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config
print(f"PLaying as {config.BOT_INTELLIGENCE} bot")


from src.game import BreakItBad

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
if config.HEADDLESS_MODE:
    chrome_options.add_argument("--headless")

# Set up the Chrome driver
service = Service(config.CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

game = BreakItBad(driver, config.BOT_INTELLIGENCE, config.GAME_URL)
game.login()

import os
already_played_games_count = 0
if os.path.exists(config.SCOREBOARD_PATH):
    with open(config.SCOREBOARD_PATH, 'r') as f:
        lines = f.readlines()
        already_played_games_count = len(lines)-1
    print(f"Already played games: {already_played_games_count}")
games_scoreboard = None

for i in range(config.NUM_TRIALS):
    print(f"Playing Trial: {already_played_games_count+i+1}")
    current_scoreboard = []
    game.start_game()
    game.find_edges()
    while(True):
        game.attack()
        score = game.get_score()
        game.find_edges()
        current_scoreboard.append(score)
        if (game.is_game_over()):
            with open(config.SCOREBOARD_PATH, 'a') as f:
                current_scoreboard = current_scoreboard + [current_scoreboard[-1]] * (config.MAX_ROUNDS - len(current_scoreboard))
                f.write(','.join(map(str, current_scoreboard)) + '\n')
            break
    game.reset_game()

import src.utils.metrics as metrics
metrics.analyze_scoreboard(config.SCOREBOARD_PATH, config.NUM_TRIALS)    