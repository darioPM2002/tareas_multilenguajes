from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.datacollection import DataCollector

from .agent import Basura, EstacionCarga, ObstacleAgent, Roomba

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
      
        i = 0

        # Create the border cells
        for _, cell in enumerate(self.grid):
      
            if i == 29: 
                
                Roomba.create_agents(
                    self,
                    1,
                    cell=cell,
                )
                self.running = True
                EstacionCarga.create_agents(
                    self,
                    1,
                    cell=cell,
                )
             
                
            i += 1
        Basura.create_agents(
            self,
            self.num_agents,
            cell=self.random.choices(self.grid.empties.cells, k=self.num_agents)
        )
        ObstacleAgent.create_agents(
            self,
            self.num_agents,
            cell=self.random.choices(self.grid.empties.cells, k=self.num_agents)
        )
       
        # Configurar el DataCollector
        self.datacollector = DataCollector(
            model_reporters={
                "Batería": get_battery,
                "Basuras": get_trash_count,
                "Celdas Mapeadas": get_mapped_cells
            }
        )
        
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)


# Funciones para recolectar datos
def get_battery(model):
    """Obtiene la batería del Roomba"""
    roombas = [agent for agent in model.agents if isinstance(agent, Roomba)]
    if roombas:
        return roombas[0].battery
    return 0


def get_trash_count(model):
    """Cuenta la cantidad de basura restante"""
    return len([agent for agent in model.agents if isinstance(agent, Basura)])


def get_mapped_cells(model):
    """Cuenta el número de celdas mapeadas por el Roomba"""
    roombas = [agent for agent in model.agents if isinstance(agent, Roomba)]
    if roombas:
        return len(roombas[0].historialMapeado)
    return 0