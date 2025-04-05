from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .utils import const
import random

class BreakItBad:

    # GAME LOGIN SCREEN
    USERNAME_INPUT_SELECTOR = '/html/body/app-root/game/profile/div/profile-dialog/p-dialog/div/div/div[2]/div[1]/div/input'
    USERNAME_ACCEPT_BUTTON_SELECTOR = '/html/body/app-root/game/profile/div/profile-dialog/p-dialog/div/div/div[2]/div[2]/p-button[1]'
    
    # MAIN SCREEN SELECTORS
    INTRO_BANNER_CLOSE_BUTTON = "/html/body/app-root/game/game-intro-dialog/p-dialog/div/div/div[1]/div/button"
    ATTACK_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[2]/div/p-button"
    MAP_BUTTON_SELECTOR = "/html/body/app-root/game/div[4]/div[1]/p-button[3]"

    NODE_SELECTOR = None
    EDGE_SELECTOR = "g path"
    EDGE_SELECTOR = "//g/path"
    SCOREBOARD_SELECTOR = "/html/body/app-root/game/div[4]/div[2]/break-it-bad/multi-score-display/current-score/p-fieldset/fieldset/div/div"

    MAX_FIND_EDGES_TRIES = 3

    def __init__(self, driver: WebDriver, intelligence: str, game_url: str):
        self.driver = driver
        self.game_url = game_url
        self.reset_game(first_run=True)
        self.initiliaze_edges()
        self.find_edges_tries = 0
        self.intelligence = intelligence
        
    
    def reset_game(self, first_run=False):
        self.driver.get(self.game_url)
        if first_run:
            WebDriverWait(self.driver, 5).until(
                # Wait till username input screen appears
                EC.presence_of_element_located((By.XPATH, self.USERNAME_INPUT_SELECTOR))
            )
        else:
            WebDriverWait(self.driver, 5).until(
                # Wait till the driver see the close button os start game banner
                EC.presence_of_element_located((By.XPATH, self.INTRO_BANNER_CLOSE_BUTTON))
            )

    def initiliaze_edges(self):
        self.not_attacked_edges = []
        self.attacked_edges = []
        self.off_edges = []

    def login(self):
        self.driver.find_element(By.XPATH, self.USERNAME_INPUT_SELECTOR).send_keys('bot')
        self.driver.find_element(By.XPATH, self.USERNAME_ACCEPT_BUTTON_SELECTOR).click()
        WebDriverWait(self.driver, 5).until(
            # Wait till the driver see the close button os start game banner
            EC.presence_of_element_located((By.XPATH, self.INTRO_BANNER_CLOSE_BUTTON))
        )

    def start_game(self):
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element(By.XPATH, self.INTRO_BANNER_CLOSE_BUTTON).is_displayed() and
                   driver.find_element(By.XPATH, self.ATTACK_BUTTON_SELECTOR).is_displayed() and
                   driver.find_element(By.XPATH, self.MAP_BUTTON_SELECTOR).is_displayed()
        )
        self.driver.find_element(By.XPATH, self.INTRO_BANNER_CLOSE_BUTTON).click()
        # time.sleep(2)
        self.driver.find_element(By.XPATH, self.ATTACK_BUTTON_SELECTOR).click()
        self.driver.find_element(By.XPATH, self.MAP_BUTTON_SELECTOR).click()
        WebDriverWait(self.driver, 1)

    def find_nodes(self):
        # Implement logic to find nodes using Selenium
        nodes = self.driver.find_elements_by_class_name('node')
        return nodes

    def find_edges(self):
        # Implement logic to find edges using Selenium
        # edges = self.driver.execute_script(f"return document.querySelectorAll('{self.EDGE_SELECTOR}');")
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element(By.TAG_NAME, "g").is_displayed()
        )
        self.initiliaze_edges()
        map = self.driver.find_element(By.TAG_NAME, 'g')
        edges = map.find_elements(By.TAG_NAME, 'path')
        try: 
            for edge in edges:
                attr = edge.get_attribute('stroke')
                if "on forward" in attr or "on reverse" in attr:
                    self.not_attacked_edges.append(edge)
                elif "off" in attr:
                    self.attacked_edges.append(edge)
                elif "on stopped" in attr:
                    self.off_edges.append(edge)
        except Exception as e:
            print(f"Error while finding edges: {e}")
            self.find_edges_tries += 1
            if self.find_edges_tries < self.MAX_FIND_EDGES_TRIES:
                self.find_edges()
            else:
                raise e
        self.find_edges_tries = 0

    def get_score(self):
        # Implement logic to find scoreboard using Selenium
        scoreboard = self.driver.find_element(By.XPATH, self.SCOREBOARD_SELECTOR).text
        return scoreboard

    def attack(self):
        # Implement logic to attack an edge using Selenium
        if self.intelligence == "not_dumb":
            edge = random.choice(self.not_attacked_edges)
        elif self.intelligence == "dumb":
            edge = random.choice(self.not_attacked_edges + self.off_edges)
        # self.not_attacked_edges.remove(edge)
        self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, edge)
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'p-dialog'))
        # )
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'p-dialog'))
        )
        time.sleep(1)
    
    def is_game_over(self):
        # Implement logic to check if the game is over using Selenium
        if len(self.not_attacked_edges) == 0:
            return True
        return False

    def quit(self):
        self.driver.quit()