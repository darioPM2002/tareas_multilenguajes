from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid

from .agent import RandomAgent, ObstacleAgent, Roomba

class RandomModel(Model):
    """
    Creates a new model with random agents.
    Args:
        num_agents: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, num_agents=10, width=8, height=8, seed=42):

        super().__init__(seed=seed)
        self.num_agents = num_agents
        self.seed = seed
        self.width = width
        self.height = height

        self.grid = OrthogonalMooreGrid([width, height], torus=False)

        # Identify the coordinates of the border of the grid
      
        i=0
        # Create the border cells
        for _, cell in enumerate(self.grid):
      
            if i==0: 
                Roomba.create_agents(
                    self,
                    self.num_agents,
                    cell=cell,
                )
                self.running = True
            i+=1
        RandomAgent.create_agents(
        self,
        self.num_agents,
        cell=self.random.choices(self.grid.empties.cells, k=self.num_agents)
            )
       
        
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.agents.shuffle_do("step")
