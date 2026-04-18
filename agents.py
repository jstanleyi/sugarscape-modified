import math
from mesa.discrete_space import CellAgent

def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    def __init__(self, model, cell, sugar=0, metabolism=0, vision = 0):
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
    
    def move(self):
        possibles = [
            cell
            for cell in self.cell.get_neighborhood(self.vision, include_center=True)
            if cell.is_empty 
        ]
        sugar_values = [
            cell.sugar
            for cell in possibles
        ]
        max_sugar = max(sugar_values)
        candidates_index = [
            i for i in range(len(sugar_values)) if math.isclose(sugar_values[i], max_sugar)
        ]
        candidates = [
            possibles[i]
            for i in candidates_index
        ]
        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [
            cell
            for cell in candidates
            if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
        ]
        self.cell = self.random.choice(final_candidates)
    
    def gather_and_eat(self):
        self.sugar += self.cell.sugar
        self.cell.sugar = 0
        self.sugar -= self.metabolism

    # Modification
    # Share 1 sugar with the most deprived vulnerable neighbor in the 8-neighborhood
    def share_with_neighbor(self):
        # only share if agent has at least one sugar left
        if self.sugar <= 1:
            return

        # Get neighboring cells (8-neighbor because model now uses Moore grid)
        neighbor_cells = self.cell.get_neighborhood(1, include_center=False)

        # Collect neighboring agents
        neighboring_agents = []
        for cell in neighbor_cells:
            if not cell.is_empty:
                neighboring_agents.extend(cell.agents)

        if len(neighboring_agents) == 0:
            return

        # Find vulnerable neighbors: those who cannot survive the next round
        vulnerable_neighbors = [
            agent
            for agent in neighboring_agents
            if agent.sugar <= agent.metabolism
        ]

        if len(vulnerable_neighbors) == 0:
            return

        # Find the minimum sugar level among vulnerable neighbors
        min_sugar = min(agent.sugar for agent in vulnerable_neighbors)

        # Select all equally most deprived vulnerable neighbors
        most_deprived = [
            agent
            for agent in vulnerable_neighbors
            if agent.sugar == min_sugar
        ]

        # Break ties randomly
        recipient = self.random.choice(most_deprived)

        # Transfer 1 unit of sugar
        self.sugar -= 1
        recipient.sugar += 1


    def see_if_die(self):
        if self.sugar <= 0:
            self.remove()
    
        
