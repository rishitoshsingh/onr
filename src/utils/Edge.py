class Edge:
    def __init__(self, id, state="stopped", on_off=False, element=None):
        self.id = id
        self.state = state
        self.element = element  # Selenium element
        self.on_off = on_off
        self.temperature = None
        self.flow = None
        self.fci = None
        self.from_node = None
        self.to_node = None

    # Setters
    def set_from_to(self, name):
        to_from = name.split("<->")
        self.to_node = int(to_from[0].strip()[1:])
        self.from_node = int(to_from[1].strip()[1:])

    def set_temperature(self, temperature):
        self.temperature = int(temperature)

    def set_flow(self, flow):
        self.flow = int(flow)

    def set_fci(self, fci):
        self.fci = int(fci)

    def get_status(self):
        if not self.on_off:
            return "attacked"
        elif self.state == "stopped":
            return "stopped"
        else:
            return "not_attacked"
    
    def get_edge_from_to(self):
        return f"{self.from_node} <-> {self.to_node}"

    def __repr__(self):
        return f"Edge({self.from_node}->{self.to_node}, id={self.id}, state={self.state}, on_off={self.on_off}, temperature={self.temperature}, flow={self.flow}, fci={self.fci})"