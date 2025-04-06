from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import test_config
print(f"Playing as tester bot")


from src.game import BreakItBad

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
if test_config.HEADDLESS_MODE:
    chrome_options.add_argument("--headless")

# Set up the Chrome driver
service = Service(test_config.CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

game = BreakItBad(driver, test_config.BOT_INTELLIGENCE, test_config.GAME_URL)
game.login()

for i in range(test_config.NUM_TRIALS):
    current_scoreboard = []
    game.start_game()
    game.get_state()
    while(True):
        game.attack()
        score = game.get_score()
        game.get_state()
        current_scoreboard.append(score)
        if (game.is_game_over()):
            break
    game.reset_game()

