from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .utils import const
import random
from .utils import Node, Edge


class DysruptionGame:

    # GAME LOGIN SCREEN
    USERNAME_INPUT_SELECTOR = '/html/body/app-root/game/profile/div/profile-dialog/p-dialog/div/div/div[2]/div[1]/div/input'
    USERNAME_ACCEPT_BUTTON_SELECTOR = '/html/body/app-root/game/profile/div/profile-dialog/p-dialog/div/div/div[2]/div[2]/p-button[1]'
    
    # MAIN SCREEN SELECTORS
    INTRO_BANNER_CLOSE_BUTTON = "/html/body/app-root/game/game-intro-dialog/p-dialog/div/div/div[1]/div/button"
    SELECT_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[1]/div/p-button"
    MAP_BUTTON_SELECTOR = "/html/body/app-root/game/div[4]/div[1]/p-button[3]"

    NODE_SELECTOR = "leaflet-marker-icon"
    EDGE_SELECTOR = "g path"
    EDGE_SELECTOR = "//g/path"

    MAX_FIND_EDGES_TRIES = 3


    def __init__(self, driver: WebDriver, intelligence: str, game_url: str, edge_detailed_state: bool, node_detailed_state: bool, random_action_threshold=0.5):
        self.driver = driver
        self.game_url = game_url
        self.reset_game(first_run=True)
        self.initiliaze_edges_nodes()
        self.find_state_tries = 0
        self.intelligence = intelligence
        self.edge_detailed_state = edge_detailed_state
        self.node_detailed_state = node_detailed_state
        self.random_action_threshold = random_action_threshold
    
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

    def initiliaze_edges_nodes(self):
        self.nodes = []
        self.edges = []

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
                   driver.find_element(By.XPATH, self.MAP_BUTTON_SELECTOR).is_displayed()
        )
        self.driver.find_element(By.XPATH, self.INTRO_BANNER_CLOSE_BUTTON).click()
        self.driver.find_element(By.XPATH, self.MAP_BUTTON_SELECTOR).click()

    def activate_map_read_mode(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.SELECT_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, self.SELECT_BUTTON_SELECTOR).click()
        WebDriverWait(self.driver, 1)
    
    # def deactivate_map_read_mode(self):
    #     WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.ATTACK_BUTTON_SELECTOR)))
    #     self.driver.find_element(By.XPATH, self.ATTACK_BUTTON_SELECTOR).click()
    #     WebDriverWait(self.driver, 1)
    
    def find_edges(self):
        # Implement logic to find edges using Selenium
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element(By.TAG_NAME, "g").is_displayed()
        )
        map = self.driver.find_element(By.TAG_NAME, 'g')
        edges = map.find_elements(By.CLASS_NAME, "fuel")
        for i, edge in enumerate(edges):
            strokes = edge.get_attribute('stroke').split()
            edge_state = 'forward' if 'forward' in strokes else 'reverse' if 'reverse' in strokes else 'stopped' if 'stopped' in strokes else 'unknown'
            edge_on_off = True if 'on' in strokes else False
            new_edge = Edge(i+1, edge_state, edge_on_off, element=edge)
            self.edges.append(new_edge)
    
    def find_edges_state(self):
        self.activate_map_read_mode()
        for edge in self.edges:
            self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, edge.element)
            # WebDriverWait(self.driver, 1).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "inspector-item"))
            # )
            WebDriverWait(self.driver, 3).until(
                lambda d: any(
                    item.find_element(By.CLASS_NAME, "label").text.strip()
                    for item in d.find_elements(By.CLASS_NAME, "inspector-item")
                )
            )
            inspector_items = self.driver.find_elements(By.CLASS_NAME, "inspector-item")
            name_found = False
            for item in inspector_items:
                if item.find_element(By.CLASS_NAME, "label").text.lower() == "name":
                    name_found = True
                    edge.set_from_to(item.find_element(By.CLASS_NAME, "value").text)
                elif item.find_element(By.CLASS_NAME, "label").text.lower() == "temperature":
                    edge.set_temperature(item.find_element(By.CLASS_NAME, "value").text)
                if item.find_element(By.CLASS_NAME, "label").text.lower() == "flow":
                    edge.set_flow(item.find_element(By.CLASS_NAME, "value").text)
                elif item.find_element(By.CLASS_NAME, "label").text.lower() == "fci":
                    edge.set_fci(item.find_element(By.CLASS_NAME, "value").text)
            if not name_found:
                for item in inspector_items:
                    print(item.text)
                    print(type(item))
                print(edge.element.text)
                input()
        # self.deactivate_map_read_mode()

    def find_nodes(self):
        nodes = self.driver.find_elements(By.CLASS_NAME, self.NODE_SELECTOR)
        for node in nodes:
            classes = node.get_attribute('class').split()
            node_type = 'demand' if 'demand' in classes else 'supply' if 'supply' in classes else 'unknown'
            node_on_off = True if 'on' in classes else False
            new_node = Node(node_type, node_on_off, element=node)
            self.nodes.append(new_node)

    def find_nodes_state(self):
        self.activate_map_read_mode()
        for node in self.nodes:
            self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, node.element)
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inspector-item"))
            )
            inspector_items = self.driver.find_elements(By.CLASS_NAME, "inspector-item")
            for item in inspector_items:
                if item.find_element(By.CLASS_NAME, "label").text.lower() == "name":
                    node.set_name(item.find_element(By.CLASS_NAME, "value").text)
                elif item.find_element(By.CLASS_NAME, "label").text.lower() == "temperature":
                    node.set_temperature(item.find_element(By.CLASS_NAME, "value").text)
                if item.find_element(By.CLASS_NAME, "label").text.lower() == "penalty":
                    node.set_penalty(item.find_element(By.CLASS_NAME, "value").text)
                elif item.find_element(By.CLASS_NAME, "label").text.lower() == "supply":
                    node.set_supply(item.find_element(By.CLASS_NAME, "value").text)
                if item.find_element(By.CLASS_NAME, "label").text.lower() == "shortfall":
                    node.set_shortfall(item.find_element(By.CLASS_NAME, "value").text)
                elif item.find_element(By.CLASS_NAME, "label").text.lower() == "demand":
                    node.set_demand(item.find_element(By.CLASS_NAME, "value").text)
        # self.deactivate_map_read_mode()

    def random_action(self):
        return random.random() <= self.random_action_threshold 
    
    def action(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'p-dialog'))
        )
        time.sleep(1)

    def quit(self):
        self.driver.quit()

class BreakItBad (DysruptionGame):

    ATTACK_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[2]/div/p-button"
    SCOREBOARD_SELECTOR = "/html/body/app-root/game/div[4]/div[2]/break-it-bad/multi-score-display/current-score/p-fieldset/fieldset/div/div"

    def __init__(self, driver: WebDriver, intelligence: str, game_url: str, edge_detailed_state: bool, node_detailed_state: bool, random_action_threshold=0.5):
        super().__init__(driver, intelligence, game_url, edge_detailed_state, node_detailed_state, random_action_threshold)
        
    def initiliaze_edges_nodes(self):
        super().initiliaze_edges_nodes()
        self.not_attacked_edges = []
        self.attacked_edges = []
        self.off_edges = []

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
        self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, edge.element)
        return edge

    def action(self):
        edge = self.attack()
        super().action()
        return edge
    
    def is_game_over(self):
        # Implement logic to check if the game is over using Selenium
        if len(self.not_attacked_edges) == 0:
            return True
        return False

    def filter_edges(self):
        for edge in self.edges:
            if edge.get_status() == "not_attacked":
                self.not_attacked_edges.append(edge)
            elif edge.get_status() == "stopped":
                self.off_edges.append(edge)
            elif edge.get_status() == "attacked":
                self.attacked_edges.append(edge)

    def deactivate_map_read_mode(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.ATTACK_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, self.ATTACK_BUTTON_SELECTOR).click()
        WebDriverWait(self.driver, 1)

    def get_state(self):
        try:
            self.initiliaze_edges_nodes()
            self.find_nodes()
            if self.node_detailed_state:
                self.find_nodes_state()
            self.find_edges()
            if self.edge_detailed_state:
                self.find_edges_state()
            self.deactivate_map_read_mode()
            self.filter_edges()
        except:
            print("Error while getting state")
            if self.find_state_tries < self.MAX_FIND_EDGES_TRIES:
                self.find_state_tries += 1
                print(f"Retrying to find state {self.find_state_tries}/{self.MAX_FIND_EDGES_TRIES}")
                time.sleep(2)
            else:
                raise
            self.get_state()
        self.find_state_tries = 0


class SaveOurSystem (DysruptionGame):

    REPAIR_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[2]/div/p-button[1]"
    REPLACE_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[2]/div/p-button[2]"
    MAINTAIN_BUTTON_SELECTOR = "/html/body/app-root/game/div[5]/action-toolbar/div/mode-list[2]/div/p-button[3]"

    SCOREBOARD_SELECTOR = "/html/body/app-root/game/div[4]/div[2]/save-our-system/current-score/p-fieldset/fieldset/div/div"
    BUDGET_SELECTOR = "/html/body/app-root/game/div[4]/div[2]/save-our-system/budget/p-fieldset[1]/fieldset/div/div"

    END_TURN_BUTTON_SELECTOR = "/html/body/app-root/game/current-actions/p-button[2]/button"

    REPAIR_COST = 250
    MAINTAIN_COST = 50
    REPLACE_COST = 500


    def __init__(self, driver: WebDriver, intelligence: str, game_url: str, edge_detailed_state: bool, node_detailed_state: bool, random_action_threshold=0.5):
        super().__init__(driver, intelligence, game_url, edge_detailed_state, node_detailed_state, random_action_threshold)
        
    def initiliaze_edges_nodes(self):
        super().initiliaze_edges_nodes()
        self.operational_edges = []
        self.destroyed_edges = []

    def get_score(self):
        # Implement logic to find scoreboard using Selenium
        scoreboard = self.driver.find_element(By.XPATH, self.SCOREBOARD_SELECTOR).text
        return scoreboard
    
    def get_budget(self):
        budget_text = self.driver.find_element(By.XPATH, self.BUDGET_SELECTOR).text
        return int(budget_text.replace("$", "").replace(",", "").strip())

    def perform_action(self, edge, action_button_selector):
        # Implement logic to attack an edge using Selenium
        self.driver.find_element(By.XPATH, action_button_selector).click()
        self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, edge.element)

    def action(self):
        actions = []
        budget, current_cost = self.get_budget(), 0
        if self.intelligence == "only_maintain":
            edges_to_act = self.operational_edges
        elif self.intelligence == "only_replace":
            edges_to_act = self.edges
        elif self.intelligence == "only_repair":
            edges_to_act = self.destroyed_edges
        elif self.intelligence == "weighted_random":
            edges_to_act = self.edges
        random.shuffle(edges_to_act)
        for edge in edges_to_act:
            if super().random_action():
                if self.intelligence == "only_maintain" and (current_cost+self.MAINTAIN_COST) <= budget:
                    self.perform_action(edge, self.MAINTAIN_BUTTON_SELECTOR)
                    current_cost += self.MAINTAIN_COST
                    actions.append(f"MAINTAIN: {edge.get_edge_from_to()}")
                elif self.intelligence == "only_replace" and (current_cost+self.REPLACE_COST) <= budget:
                    self.perform_action(edge, self.REPLACE_BUTTON_SELECTOR)
                    current_cost += self.REPLACE_COST
                    actions.append(f"REPLACE: {edge.get_edge_from_to()}")
                elif self.intelligence == "only_repair" and (current_cost+self.REPAIR_COST) <= budget:
                    self.perform_action(edge, self.REPAIR_BUTTON_SELECTOR)
                    current_cost += self.REPAIR_COST
                    actions.append(f"REPAIR: {edge.get_edge_from_to()}")
                elif self.intelligence == "weighted_random":
                    if edge.fci >= 99.6 and (current_cost+self.MAINTAIN_COST) <= budget:
                        self.perform_action(edge, self.MAINTAIN_BUTTON_SELECTOR)
                        current_cost += self.MAINTAIN_COST
                        actions.append(f"MAINTAIN: {edge.get_edge_from_to()}")
                    elif edge.fci >= 92 and (current_cost+self.REPAIR_COST) <= budget:
                        self.perform_action(edge, self.REPAIR_BUTTON_SELECTOR)
                        current_cost += self.REPAIR_COST
                        actions.append(f"REPAIR: {edge.get_edge_from_to()}")
                    elif (current_cost+self.REPLACE_COST) <= budget:
                        self.perform_action(edge, self.REPLACE_BUTTON_SELECTOR)
                        current_cost += self.REPLACE_COST
                        actions.append(f"REPLACE: {edge.get_edge_from_to()}")
        self.driver.execute_script(const.JS_MOUSEEVENT_CLICK, self.driver.find_element(By.XPATH, self.END_TURN_BUTTON_SELECTOR))
        super().action()
        return actions
    
    def is_game_over(self):
        # Implement logic to check if the game is over using Selenium
        if len(self.not_attacked_edges) == 0:
            return True
        return False

    def filter_edges(self):
        for edge in self.edges:
            if edge.fci == 0:
                self.destroyed_edges.append(edge)
            else:
                self.operational_edges.append(edge)

    def get_state(self):
        try:
            self.initiliaze_edges_nodes()
            self.find_nodes()
            if self.node_detailed_state:
                self.find_nodes_state()
            self.find_edges()
            if self.edge_detailed_state:
                self.find_edges_state()
            self.filter_edges()
        except:
            print("Error while getting state")
            if self.find_state_tries < self.MAX_FIND_EDGES_TRIES:
                self.find_state_tries += 1
                print(f"Retrying to find state {self.find_state_tries}/{self.MAX_FIND_EDGES_TRIES}")
                time.sleep(2)
            else:
                raise
            self.get_state()
        self.find_state_tries = 0
