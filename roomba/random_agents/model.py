from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.datacollection import DataCollector

from .agent import Basura, EstacionCarga, ObstacleAgent, Roomba
class RandomModel(Model):
    """
    Modelo con porcentajes ajustables de Basura y Obstáculos.
    """
    def __init__(self, num_agents=10, width=8, height=8, seed=42,
             porcentaje_basura=0.3, porcentaje_obstaculos=0.3):

        super().__init__(seed=seed)

        self.num_agents = num_agents
        self.seed = seed
        self.width = width
        self.height = height
        self.basura_pct = porcentaje_basura
        self.obstaculos_pct = porcentaje_obstaculos

        self.grid = OrthogonalMooreGrid([width, height], torus=False)

        # --- Crear Roomba y Estación ---
        i = 0
        for _, cell in enumerate(self.grid):
            if i == 29: 
                Roomba.create_agents(self, 1, cell=cell)
                EstacionCarga.create_agents(self, 1, cell=cell)
            i += 1

        # --- Celdas disponibles ---
        empty_cells = self.grid.empties.cells

        # --- Calcular cantidades según porcentaje ---
        total_celdas = len(empty_cells)
        n_basura = int(total_celdas * self.basura_pct)
        n_obstaculos = int(total_celdas * self.obstaculos_pct)

        # --- Crear Basuras ---
        Basura.create_agents(
            self,
            n_basura,
            cell=self.random.choices(empty_cells, k=n_basura)
        )

        # --- Crear Obstáculos ---
        ObstacleAgent.create_agents(
            self,
            n_obstaculos,
            cell=self.random.choices(self.grid.empties.cells, k=n_obstaculos)
        )

        # --- Data collector ---
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