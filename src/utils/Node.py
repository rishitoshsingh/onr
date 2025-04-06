class Node:
    def __init__(self, type="demand", on_off=False, element=None):
        self.name = None
        self.id = None
        self.type = type  # "demand" or "supply"
        self.element = element  # Selenium element
        self.demand = None
        self.supply = None
        self.shortfall = None
        self.on_off = on_off
        self.temperature = None
        self.penalty = None

    # Setters
    def set_name(self, name):
        self.name = name
        self.id = int(name[1:])
    
    def set_demand(self, demand):
        self.demand = demand
    
    def set_supply(self, supply):
        self.supply = supply

    def set_shortfall(self, shortfall):
        self.shortfall = shortfall
    
    def set_temperature(self, temperature):
        self.temperature = int(temperature)
    
    def set_penalty(self, penalty):
        self.penalty = penalty

    def __repr__(self):
        return f"Node(name={self.name}, type={self.type}, on_off={self.on_off}, demand={self.demand}, supply={self.supply}, shortfall={self.shortfall}, temperature={self.temperature}, penalty={self.penalty})"