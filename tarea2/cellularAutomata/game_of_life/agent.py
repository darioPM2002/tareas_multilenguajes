# FixedAgent: Immobile agents permanently fixed to cells
from mesa.discrete_space import FixedAgent

class Cell(FixedAgent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0
    ALIVE = 1

 
    @property
    def x(self):
        return self.cell.coordinate[0]

    @property
    def y(self):
        return self.cell.coordinate[1]

    @property
    def is_alive(self):
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.cell.neighborhood.agents
    
    #OBTENER LOS VECINOS SUPERIORES
    @property
    def neighbors3Up(self):
        #Warning 
        result = []
        i=0
        ##Se iteran todos los veciones y si coinciden con las posiciones 2,4 y 7 (superiores) se agregan a la lista result
        for neighbor in self.neighbors:
            if i == 2 or i ==4 or i==7 :
                result.append(neighbor)
        
            i=i+1
        return result
    
    def __init__(self, model, cell, init_state=DEAD):
        """Create a cell, in the given state, at the given x, y position."""
        super().__init__(model)
        self.cell = cell
        self.pos = cell.coordinate
        self.state = init_state
        self._next_state = None
    
        
      
        

    def determine_state(self):
        """Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """
        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.
        live_neighbors = sum(neighbor.is_alive for neighbor in self.neighbors)

        # Assume nextState is unchanged, unless changed below.
        self._next_state = self.state

        #if self.is_alive:
        #    if live_neighbors < 2 or live_neighbors > 3:
        #        self._next_state = self.DEAD
        #else:
        #    if live_neighbors == 3:
        #        self._next_state = self.ALIVE
        valor3 = []
       
        ###
        #Lógica para los 3 vecinos superiores, nos da una lista con los estados}
        # esto nos ayuda a velaur los estados de los 3 vecinos superiores
        for neighbor in self.neighbors3Up:
                if neighbor.state == 1:
                    valor3.append(1) 
                else:
                    valor3.append(0)    
      
      ##Condiciones que nos da el problema para saber si la celda vive o muere
        if (valor3 == [1,1,1] or valor3 == [1,0,1] or valor3 == [0,1,0] or valor3 == [0,0,0]):
            #self.state = Cell.DEAD
            self._next_state = self.DEAD
        if (valor3 == [1,1,0] or valor3 == [1,0,0] or valor3 == [0,1,1] or valor3 == [0,0,1]):
         
            self._next_state = self.ALIVE
            print("CELDA VIVA EN POSICION: ", self.pos)

    def assume_state(self):
        """Set the state to the new computed state -- computed in step()."""
        self.state = self._next_state
    
    def get_neighbors3Up_states(self):
        return [neighbor.state for neighbor in self.neighbors3Up]
