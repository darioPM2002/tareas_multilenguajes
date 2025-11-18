from mesa.discrete_space import CellAgent, FixedAgent

class DrawAgent(CellAgent):
    """
    Agente que solo sirve para dibujar una celda en el grid.
    No se mueve, no interactúa, solo ocupa la cell asignada.
    """
    def __init__(self, model, cell, color="green"):
        super().__init__(model)
        self.cell = cell
        self.color = color

    def step(self):
        pass
class Basura(CellAgent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
    """
    def __init__(self, model, cell):
        """
        Creates a new random agent.
        Args:
            model: Model reference for the agent
            cell: Reference to its position within the grid
        """
        super().__init__(model)
 
        self.cell = cell
        self.color= "blue"
    

    def move(self):
        """
        Determines the next empty cell in its neighborhood, and moves to it
        """
        

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        

class greenAgent(CellAgent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
    """
    def __init__(self, cell):
        """
        Creates a new random agent.
        Args:
            model: Model reference for the agent
            cell: Reference to its position within the grid
        """
        super().__init__()
 
        self.cell = cell


class Roomba(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.battery = 100
        self.desviacionx = 0
        self.desviaciony = 0
        self.distancia_base = 0
        self.direction = "arriba"
        self.directionCurso = ""
        self.estado = ""

    #BORRAR BASURA

    def borrarBasura(self):
        basuras = [a for a in self.cell.agents if isinstance(a, Basura)]

        for b in basuras:
            print("Basura encontrada")
            self.battery -= 1
            b.remove()

    def distancia_al_origen(coord):
        x, y = coord
        print(x**2 + y**2) ** 0.5
        return (x**2 + y**2) ** 0.5


    #   MAPEO Y MOVIMIENTO    # -------------------------------------------------
    def mapeoRoomba(self):

    # --- Obtener vecinos ---
     vecinos = { "izquierda": None, "derecha": None, "arriba": None, "abajo": None }
 
     for v in self.cell.neighborhood:
         if v is None:
             continue
 
         cx, cy = v.coordinate
         x, y = self.cell.coordinate
 
         # Pintar exploración
         if not any(isinstance(a, DrawAgent) for a in v.agents):
             da = DrawAgent(self.model, v, color="yellow")
             self.model.register_agent(da)
 
         if (cx, cy) == (x - 1, y): vecinos["izquierda"] = v
         if (cx, cy) == (x + 1, y): vecinos["derecha"] = v
         if (cx, cy) == (x, y + 1): vecinos["arriba"] = v
         if (cx, cy) == (x, y - 1): vecinos["abajo"] = v
 
 
     def hay_obs(vec):
         return vec is None or any(isinstance(a, ObstacleAgent) for a in vec.agents)
 
 
     # --- Inicializa zigzag ---
     if not hasattr(self, "zigzag_mode"):
         self.zigzag_mode = False
         self.zigzag_dx = 0   # pasos a la derecha en zigzag
 
 
     # --- Lógica normal: avanza hacia arriba ---
     if not self.zigzag_mode:
 
         if self.direction == "arriba" and hay_obs(vecinos["arriba"]):
             # inicia zigzag hacia abajo
             self.zigzag_mode = True
             self.zigzag_dx = 0
             self.next_vertical = "abajo"
 
         elif self.direction == "abajo" and hay_obs(vecinos["abajo"]):
             # inicia zigzag hacia arriba
             self.zigzag_mode = True
             self.zigzag_dx = 0
             self.next_vertical = "arriba"
 
 
         if self.direction == "arriba" and vecinos["arriba"]:
             return self.move_to(vecinos["arriba"])
         if self.direction == "abajo" and vecinos["abajo"]:
             return self.move_to(vecinos["abajo"])
 
 
     # --- Comportamiento ZIGZAG ---
     if self.zigzag_mode:
 
         # 1. Mover 2 pasos a la derecha
         if self.zigzag_dx < 2:
             if not hay_obs(vecinos["derecha"]):
                 self.zigzag_dx += 1
                 return self.move_to(vecinos["derecha"])
             else:
                 # no se puede zigzaguear → abortar zigzag
                 self.zigzag_mode = False
                 self.direction = self.next_vertical
                 return
 
         # 2. Ya movió 2 pasos → ahora baja/sube
         self.zigzag_mode = False
         self.direction = self.next_vertical
 
         if self.direction == "abajo" and vecinos["abajo"]:
             return self.move_to(vecinos["abajo"])
 
         if self.direction == "arriba" and vecinos["arriba"]:
             return self.move_to(vecinos["arriba"])
 
         # Si no puede, se queda sin moverse
         return

    def move(self):
        self.borrarBasura()
        self.mapeoRoomba()
        print(self.direction)


    # -------------------------------------------------
    #   STEP
    # -------------------------------------------------
    def step(self):
        self.move()
        pass



# -------------------------------------------------
#   ESTACIÓN DE CARGA (SIN CAMBIOS)
# -------------------------------------------------
class EstacionCarga(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.battery = 100
        self.distancia_base = 0
        self.direction = ""

    def borrarBasura(self):
        basuras = [a for a in self.cell.agents if isinstance(a, Basura)]
        for b in basuras:
            print("Basura encontrada")
            self.battery -= 1
            b.remove()

    def move(self):
        print()

    def step(self):
        self.move()
        pass

class ObstacleAgent(FixedAgent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell=cell

    def step(self):
        pass
