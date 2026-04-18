from pathlib import Path

import numpy as np

import mesa
from agents import SugarAgent
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.discrete_space.property_layer import PropertyLayer

class SugarScapeModel(mesa.Model):
    def calc_gini(self):
        agent_sugars = [a.sugar for a in self.agents]
        if len(agent_sugars) == 0:
            return 0
        sorted_sugars = sorted(agent_sugars)
        n = len(sorted_sugars)
        total = sum(sorted_sugars)
        if total == 0:
            return 0
        x = sum(el * (n - ind) for ind, el in enumerate(sorted_sugars)) / (n * total)
        return 1 + (1 / n) - 2 * x
    
    def __init__(
        self,
        width = 50,
        height = 50,
        initial_population=200,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
        seed = None
    ):
        super().__init__(rng=seed)
        self.width = width
        self.height = height
        self.running = True

        # Modification: from 4 neighbors to 8 neighbors
        self.grid = OrthogonalMooreGrid(
            (self.width, self.height), torus=False, random=self.random
        )

        # Modification: more plots
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Gini": self.calc_gini,
                "Population": lambda m: len(m.agents),
                "MeanSugar": lambda m: (
                    sum(a.sugar for a in m.agents) / len(m.agents)
                    if len(m.agents) > 0 else 0
                ),
            },
        )
        
        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.grid.add_property_layer(
            PropertyLayer.from_data("sugar", self.sugar_distribution)
        )

        SugarAgent.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
            sugar=self.rng.integers(
                endowment_min, endowment_max, (initial_population,), endpoint=True
            ),
            metabolism=self.rng.integers(
                metabolism_min, metabolism_max, (initial_population,), endpoint=True
            ),
            vision=self.rng.integers(
                vision_min, vision_max, (initial_population,), endpoint=True
            ),
        )
        
        self.datacollector.collect(self)
    
    # Define step:
    # 1. Sugar grows back
    # 2. All agents move
    # 3. All agents gather and eat
    # 4. All agents share with a vulnerable neighbor (Modification)
    # 5. All agents check if they die
    # 6. Collect Gini
    def step(self):
        self.grid.sugar.data = np.minimum(
            self.grid.sugar.data + 1, self.sugar_distribution
        )
        self.agents.shuffle_do("move")
        self.agents.shuffle_do("gather_and_eat")
        self.agents.shuffle_do("share_with_neighbor")
        self.agents.shuffle_do("see_if_die")
        self.datacollector.collect(self)
    
