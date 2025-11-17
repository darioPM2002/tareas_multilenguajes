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
      self.cell=cell
      self.battery = 100
      self.distancia_base = 0          # nivel de batería inicial
      self.direction = ""      # dirección actual
      
    

    def borrarBasura(self):
        basuras = [a for a in self.cell.agents if isinstance(a, Basura)]

        for b in basuras:
            print("Basura encontrada")
            self.battery-=1
            b.remove()   
            
    def move(self):
        self.borrarBasura()
        
        next_moves = self.cell.neighborhood
        x, y = self.cell.coordinate
        izquierda = derecha = arriba = abajo = None
        superiorIz = superiorDe = inferiorIz = inferiorDer = None

        for vecino in next_moves:
            if vecino is None:
                continue   
            
            cx, cy = vecino.coordinate
            x, y = self.cell.coordinate

            if (cx, cy) == (x-1, y):
                izquierda = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x+1, y):
                derecha = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x, y+1):
                arriba = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x, y-1):
                abajo = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
                
            elif (cx, cy) == (x-1, y+1):
                superiorIz = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x+1, y+1):
                superiorDe = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x-1, y-1):
                inferiorIz = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)
            elif (cx, cy) == (x+1, y-1):
                inferiorDer = vecino
                if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                    da = DrawAgent(self.model, vecino, color="yellow")
                    self.model.register_agent(da)

        if cy >26 and self.direction== "arriba":
            self.move_to(derecha)
            self.move_to(derecha)
            self.direction= "derecha"
            
            return
            
        elif cy >26 and self.direction== "derecha":
            self.move_to(abajo)
            self.direction= "abajo"
            
            return
        elif cy <=2 and self.direction== "abajo":
           self.move_to(derecha)
           self.move_to(derecha)
           self.direction= "derecha"
           return
        elif  self.direction== "abajo":
            self.move_to(abajo)
            self.direction= "abajo"
            return
        
            
        else:
             self.move_to(arriba)
             self.direction= "arriba"
             return
             
        print( self.direction)
    def step(self):

       self.move()
       pass
       


class EstacionCarga(CellAgent):
    def __init__(self, model, cell):
      super().__init__(model)
      self.cell=cell
      self.battery = 100
      self.distancia_base = 0          # nivel de batería inicial
      self.direction = ""      # dirección actual
      
    

    def borrarBasura(self):
        basuras = [a for a in self.cell.agents if isinstance(a, Basura)]

        for b in basuras:
            print("Basura encontrada")
            self.battery-=1
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
