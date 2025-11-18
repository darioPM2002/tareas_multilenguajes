from mesa.discrete_space import CellAgent, FixedAgent
from collections import deque
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

from collections import deque  # Asegúrate de importar esto si no está en tu archivo

class Roomba(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.battery = 100
        self.desviacionx = 0
        self.desviaciony = 0
        self.distancia_base = 0
        self.direction = "arriba"
        self.estadoMovimiento = ""
        self.historialMapeado = [cell]  # Lista de GridCell visitadas

    # BORRAR BASURA
    def borrarBasura(self):
        basuras = [a for a in self.cell.agents if isinstance(a, Basura)]
        for b in basuras:
            print("Basura encontrada")
            self.battery -= 1
            b.remove()

    def distancia_a_base(self):
        x, y = self.cell.coordinate
        return ((x - 1)**2 + (y - 1)**2) ** 0.5

    def ir_a_celda_objetivo(self, celda_objetivo):
        # Obtener coordenada actual
        inicio = self.cell.coordinate
        objetivo = celda_objetivo.coordinate

        # Si ya estamos en el objetivo
        if inicio == objetivo:
            return True

        # Crear set de celdas mapeadas (coordenadas válidas) - Simplificado
        celdas_validas = set(item.coordinate for item in self.historialMapeado)
        celdas_validas.add(inicio)  # Incluir posición actual si no está

        # Verificar que el objetivo está en el historial
        if objetivo not in celdas_validas:
            print("El objetivo no está en el historial mapeado")
            return False

        # BFS para encontrar el camino
        cola = deque([(inicio, [inicio])])
        visitados = {inicio}

        while cola:
            coord_actual, camino = cola.popleft()

            # Si llegamos al objetivo
            if coord_actual == objetivo:
                # Guardar el camino y empezar a seguirlo
                self.camino_objetivo = camino[1:]  # Excluir posición actual
                self.siguiendo_camino = True
                return True

            # Explorar vecinos
            x, y = coord_actual
            vecinos_posibles = [
                (x, y + 1),    # arriba
                (x, y - 1),    # abajo
                (x + 1, y),    # derecha
                (x - 1, y),    # izquierda
            ]

            for vecino in vecinos_posibles:
                if vecino in celdas_validas and vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, camino + [vecino]))

        print("No hay camino disponible al objetivo")
        return False

    def seguir_camino_objetivo(self):
        if not hasattr(self, 'siguiendo_camino') or not self.siguiendo_camino:
            return False

        if not hasattr(self, 'camino_objetivo') or len(self.camino_objetivo) == 0:
            self.siguiendo_camino = False
            print("Objetivo alcanzado")
            return True

        # Obtener siguiente paso
        siguiente_coord = self.camino_objetivo[0]
        x_actual, y_actual = self.cell.coordinate
        x_sig, y_sig = siguiente_coord

        # Encontrar la celda vecina correspondiente
        for vecino in self.cell.neighborhood:
            if vecino and vecino.coordinate == siguiente_coord:
                # Verificar que no haya obstáculos
                if not any(isinstance(a, ObstacleAgent) for a in vecino.agents):
                    self.move_to(vecino)
                    self.camino_objetivo.pop(0)  # Remover paso completado
                    self.battery -= 1
                    return False  # Aún no termina
                else:
                    # Obstáculo en el camino, recalcular
                    print("Obstáculo detectado, recalculando ruta")
                    self.siguiendo_camino = False
                    return False

        # Si no se encuentra el vecino, hay un problema
        print("Error: no se puede acceder a la siguiente celda")
        self.siguiendo_camino = False
        return False

    # MAPEO Y MOVIMIENTO
    def mapeoRoomba(self):
        next_moves = self.cell.neighborhood
        x, y = self.cell.coordinate

        izquierda = derecha = arriba = abajo = izquierdaABajo = derechaAbajo = derechaArriba = izquierdaArriba = None

        # IDENTIFICAR VECINOS
        for vecino in next_moves:
            if vecino is None:
                continue

            cx, cy = vecino.coordinate
            x, y = self.cell.coordinate
            
            # Marcar caminos (solo para visualización, NO agregar al historial aquí)
            if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                print(f"Marcando celda vecina: {vecino.coordinate}")  # Debug
                da = DrawAgent(self.model, vecino, color="yellow")
                self.model.register_agent(da)
          

                

            if (cx, cy) == (x - 1, y):
                izquierda = vecino
            elif (cx, cy) == (x + 1, y):
                derecha = vecino
            elif (cx, cy) == (x, y + 1):
                arriba = vecino
            elif (cx, cy) == (x, y - 1):
                abajo = vecino
            elif (cx, cy) == (x - 1, y - 1):
                izquierdaABajo = vecino
            elif (cx, cy) == (x + 1, y - 1):
                derechaAbajo = vecino
            elif (cx, cy) == (x + 1, y + 1):
                derechaArriba = vecino
            elif (cx, cy) == (x - 1, y + 1):
                izquierdaArriba = vecino

        # FUNCIÓN OBSTÁCULOS (pero None no es obstáculo)
        def hay_obstaculo(vec):
            if vec is None:
                return "BORDE"  # borde, NO obstáculo
            if any(isinstance(a, ObstacleAgent) for a in vec.agents):
                return "OBSTACULO"

        # -------------------------------------------------
        #      ZIG-ZAG ENTRE ARRIBA Y ABAJO (bordes)
        # -------------------------------------------------
        
        # -------------------------------------------------
        #      MANIOBRA ANTI-OBSTÁCULO (NO aplica en bordes)
        # -------------------------------------------------

        ## MAPEO ZIGZAG
        if self.battery < self.distancia_base + 3:
            print("regresar a base")
        else:
            if self.direction == "arriba" and hay_obstaculo(arriba) == "BORDE":
                self.direction = "derecha"
                self.estadoMovimiento = "MOVIMINETOU"
            elif self.direction == "derecha" and self.estadoMovimiento == "MOVIMINETOU":
                self.direction = "derecha"
                self.estadoMovimiento = "MOVIMINETOUFIN"
            elif self.direction == "derecha" and self.estadoMovimiento == "MOVIMINETOUFIN":
                self.direction = "abajo"
                self.estadoMovimiento = ""
            elif self.direction == "abajo" and hay_obstaculo(abajo) == "BORDE":
                self.direction = "derecha"
                self.estadoMovimiento = "MOVIMINETOUA"
            elif self.direction == "derecha" and self.estadoMovimiento == "MOVIMINETOUA":
                self.direction = "derecha"
                self.estadoMovimiento = "MOVIMINETOUFIND"
            elif self.direction == "derecha" and self.estadoMovimiento == "MOVIMINETOUFIND":
                self.direction = "arriba"
                self.estadoMovimiento = ""

        #   EVITAR OBSTACULOS arriba
            elif self.direction == "arriba" and hay_obstaculo(arriba) == "OBSTACULO":
                self.direction = "derecha"
                self.estadoMovimiento = "RODEAROBSTACULO"
            elif self.direction == "derecha" and self.estadoMovimiento == "RODEAROBSTACULO":
                self.direction = "arriba"
                self.desviacionx += 1
            elif self.direction == "arriba" and self.estadoMovimiento == "RODEAROBSTACULO":
                self.direction = "arriba"
                self.desviacionx += 1
                self.estadoMovimiento = "RODEAROBSTACULOREGRE"
            elif self.direction == "arriba" and self.estadoMovimiento == "RODEAROBSTACULOREGRE":
                self.direction = "izquierda"
                self.desviacionx -= 1
                self.estadoMovimiento = "RODEAROBSTACULOREGRE"
            elif self.direction == "izquierda" and self.estadoMovimiento == "RODEAROBSTACULOREGRE":
                self.direction = "arriba"
                self.estadoMovimiento = ""
            # EVITAR OBSTACULOS ABAJO
            elif self.direction == "abajo" and hay_obstaculo(abajo) == "OBSTACULO":
                self.direction = "derecha"
                self.estadoMovimiento = "RODEAROBSTACULOA"
            elif self.direction == "derecha" and self.estadoMovimiento == "RODEAROBSTACULOA":
                self.direction = "abajo"
                print("si llega")
            elif self.direction == "abajo" and self.estadoMovimiento == "RODEAROBSTACULOA":
                self.direction = "abajo"
                self.desviacionx += 1
                self.estadoMovimiento = "RODEAROBSTACULOREGREA"
            elif self.direction == "abajo" and self.estadoMovimiento == "RODEAROBSTACULOREGREA":
                if hay_obstaculo(izquierda) == "OBSTACULO" and hay_obstaculo(izquierdaABajo) == "OBSTACULO":
                    print("SE CUMPLEEEEE")
                else:
                    self.direction = "abajo"
                self.desviacionx -= 1
                self.estadoMovimiento = "RODEAROBSTACULOREGREA"
            elif self.direction == "izquierda" and self.estadoMovimiento == "RODEAROBSTACULOREGREA":
                self.direction = "abajo"
                self.estadoMovimiento = ""

        # MOVER FINAL
        print(f"Direction elegida: {self.direction}, arriba: {arriba is not None}, abajo: {abajo is not None}, derecha: {derecha is not None}, izquierda: {izquierda is not None}")  # Debug

        if self.direction == "arriba" and arriba and hay_obstaculo(arriba) != "OBSTACULO":
            self.move_to(arriba)
            print("Moviendo arriba")  # Debug
        elif self.direction == "abajo" and abajo and hay_obstaculo(abajo) != "OBSTACULO":
            self.move_to(abajo)
            print("Moviendo abajo")  # Debug
        elif self.direction == "derecha" and derecha and hay_obstaculo(derecha) != "OBSTACULO":
            self.move_to(derecha)
            print("Moviendo derecha")  # Debug
        elif self.direction == "izquierda" and izquierda and hay_obstaculo(izquierda) != "OBSTACULO":
            self.move_to(izquierda)
            print("Moviendo izquierda")  # Debug
        else:
            # Fallback: Si no puede moverse en la dirección elegida, intenta otra (gira a la derecha o elige un vecino libre)
            print("No se puede mover en dirección actual, intentando fallback")  # Debug
            for dir_name, vecino in [("arriba", arriba), ("abajo", abajo), ("derecha", derecha), ("izquierda", izquierda)]:
                if vecino and hay_obstaculo(vecino) != "OBSTACULO":
                    self.move_to(vecino)
                    self.direction = dir_name  # Actualiza dirección para consistencia
                    print(f"Fallback: Moviendo a {dir_name}")  # Debug
                    break
            else:
                print("No hay movimientos posibles - Roomba atascado")  # Debug

        return

    def move(self):
        print(f"Inicio de move() - Batería: {self.battery}, Distancia base: {self.distancia_base}")  # Debug

        # Verificar si necesita regresar a base
        if self.battery < self.distancia_base + 3:
            print("Batería baja, regresando a base")
            print(len(self.historialMapeado))
            # Si no está ya yendo a la base, calcular ruta
            if not (hasattr(self, 'siguiendo_camino') and self.siguiendo_camino):
                if len(self.historialMapeado) > 0:
                    # historialMapeado contiene GridCell directamente
                    celda_base = self.historialMapeado[0]
                    if celda_base:
                        self.ir_a_celda_objetivo(celda_base)
                    else:
                        print("Error: celda base no disponible")
                        return
                else:
                    print("Error: historial vacío")
                    return

            # Seguir el camino a la base
            objetivo_alcanzado = self.seguir_camino_objetivo()
            if objetivo_alcanzado:
                print("Base alcanzada - recargando batería")
                self.battery = 100  # Recargar batería
                self.siguiendo_camino = False
            return

        # Si estamos siguiendo un camino objetivo (no base), continuar
        if hasattr(self, 'siguiendo_camino') and self.siguiendo_camino:
            objetivo_alcanzado = self.seguir_camino_objetivo()
            if objetivo_alcanzado:
                self.borrarBasura()  # Limpiar al llegar
            return

        # Si no hay objetivo, hacer mapeo normal
        self.borrarBasura()
        self.mapeoRoomba()
        self.battery -= 1
        self.distancia_base = self.distancia_a_base()
        print(self.cell.neighborhood)
        # Agregar la celda actual al historial DESPUÉS de mover (si no está ya)
        for vecino in  self.cell.neighborhood:
            if vecino is None:
                continue
            

            if vecino not in self.historialMapeado:
                self.historialMapeado.append(vecino)
                print(f"Agregada celda al historial: {self.cell.coordinate}")  # Debug

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
