from mesa.discrete_space import CellAgent, FixedAgent
from collections import deque

historialMapeado = []
class Roomba(CellAgent):
    def __init__(self, model, cell):
        print("Creando Roomba en celda:", cell.coordinate)
        super().__init__(model)
        
        self.cell = cell
        self.battery = 100
        self.desviacionx = 0
        self.desviaciony = 0
        self.distancia_base = 0
        self.direction = "izquierda"
        self.estadoMovimiento = ""
        self.historialMapeado = [cell]  # Lista de GridCell visitadas
        self.celda_antes_de_cargar = None  # Guardar última celda antes de ir a cargar
        self.regresando_a_mapeo = False  # Flag para saber si está regresando

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
        print(f"Calculando camino a celda objetivo: {celda_objetivo.coordinate}")
        # Obtener coordenada actual
        inicio = self.cell.coordinate
        objetivo = celda_objetivo.coordinate

        # Si ya estamos en el objetivo
        if inicio == objetivo:
            return True

        # Crear set de celdas mapeadas (coordenadas válidas)
        celdas_validas = set(item.coordinate for item in self.historialMapeado)
        celdas_validas.add(inicio)  # Incluir posición actual si no está

        # Verificar que el objetivo está en el historial
        if objetivo not in celdas_validas:
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

        
        siguiente_coord = self.camino_objetivo[0]
        x_actual, y_actual = self.cell.coordinate
        x_sig, y_sig = siguiente_coord

        # Encontrar la celda vecina correspondiente
        for vecino in self.cell.neighborhood:
            if vecino and vecino.coordinate == siguiente_coord:
                
                if not any(isinstance(a, ObstacleAgent) for a in vecino.agents):
                    self.move_to(vecino)
                    self.camino_objetivo.pop(0) 
                    self.battery -= 1
                    return False  
                else:
                    x, y = self.cell.coordinate
                    for a in self.cell.neighborhood:
                        if a.coordinate ==(x  -1, y):
                            print("Obstáculo a la derecha")
                            self.move_to(a)  
                    
                    print(vecino.coordinate)
                    # Quedarse en la celda actual
                    print("Obstáculo detectado, recalculando ruta")
                    self.siguiendo_camino = False
                    
                    return False

        # Si no se encuentra el vecino, hay un problema
        print("Error: no se puede acceder a la siguiente celda")
        self.siguiendo_camino = False
        return False

    # MAPEO Y MOVIMIENTO
    def mapeoRoomba(self):

        # ----------------------------
        # LEER VECINOS
        # ----------------------------
        next_moves = self.cell.neighborhood
        x, y = self.cell.coordinate


        vecinos = {
            "izquierda": None,
            "derecha": None,
            "arriba": None,
            "abajo": None,
            "izquierdaAbajo": None,
            "derechaAbajo": None,
            "derechaArriba": None,
            "izquierdaArriba": None,
        }

        for vecino in next_moves:
            if vecino is None:
                continue

            cx, cy = vecino.coordinate

            # Marcar visual
            if not any(isinstance(a, DrawAgent) for a in vecino.agents):
                da = DrawAgent(self.model, vecino, color="yellow")
                self.model.register_agent(da)

            if   (cx, cy) == (x - 1, y): vecinos["izquierda"] = vecino
            elif (cx, cy) == (x + 1, y): vecinos["derecha"] = vecino
            elif (cx, cy) == (x, y + 1): vecinos["arriba"] = vecino
            elif (cx, cy) == (x, y - 1): vecinos["abajo"] = vecino
            elif (cx, cy) == (x - 1, y - 1): vecinos["izquierdaAbajo"] = vecino
            elif (cx, cy) == (x + 1, y - 1): vecinos["derechaAbajo"] = vecino
            elif (cx, cy) == (x + 1, y + 1): vecinos["derechaArriba"] = vecino
            elif (cx, cy) == (x - 1, y + 1): vecinos["izquierdaArriba"] = vecino

        arriba = vecinos["arriba"]
        abajo = vecinos["abajo"]
        izquierda = vecinos["izquierda"]
        derecha = vecinos["derecha"]

        # ----------------------------
        # OBSTÁCULOS
        # ----------------------------
       
        if derecha is not None:
            if  any(isinstance(a, Basura) for a in derecha.agents):
                print("Basura a la derecha - moviendo derecha")
                self.estadoMovimiento = "BASURA_DERECHA"
        if izquierda is not None :
            if  any(isinstance(a, Basura) for a in izquierda.agents):
                self.estadoMovimiento = "BASURA_IZQUIERDA"
                print("Basura a la izquierda - moviendo derecha")
        
        def hay_obstaculo(vec):
            if vec is None:
                return "BORDE"
            if any(isinstance(a, ObstacleAgent) for a in vec.agents):
                return "OBSTACULO"
            return "LIBRE"

       
        if not hasattr(self, "estadoMovimiento") or self.estadoMovimiento == "":
            self.estadoMovimiento = "ZIGZAG_UP"

        if not hasattr(self, "direction"):
            self.direction = "arriba"

        estado = self.estadoMovimiento

        # ----------------------------
        # RETORNO A BASE POR BATERÍA
        # ----------------------------
        if self.battery < self.distancia_base + 3:
            self.estadoMovimiento = "RETURN_TO_BASE"
            estado = "RETURN_TO_BASE"

     
        def estado_RETURN_TO_BASE():
            
            if hay_obstaculo(izquierda) == "LIBRE":
                self.direction = "izquierda"
            elif hay_obstaculo(abajo) == "LIBRE":
                print("MOVIENDO ABAJO PARA VOLVER A BASE")
                self.direction = "abajo"
            elif hay_obstaculo(arriba) == "LIBRE":
                self.direction = "arriba"
            else:
                self.direction = "derecha"

       
        def estado_ZIGZAG_UP():
            if hay_obstaculo(arriba) == "BORDE":
                self.estadoMovimiento = "ZIGZAG_RIGHT_UP"
            else:
                self.direction = "arriba"        

        def estado_ZIGZAG_RIGHT_UP():
            self.direction = "derecha"
            self.estadoMovimiento = "ZIGZAG_DOWN"

      
        def estado_ZIGZAG_DOWN():
            if hay_obstaculo(abajo) == "BORDE":
                self.estadoMovimiento = "ZIGZAG_RIGHT_DOWN"
            else:
                self.direction = "abajo"

        def estado_ZIGZAG_RIGHT_DOWN():
            self.direction = "derecha"
            self.estadoMovimiento = "ZIGZAG_UP"

    
        def estado_OBSTACULO_UP():
            if hay_obstaculo(arriba) == "OBSTACULO":
                self.direction = "derecha"
                
            else:
                self.estadoMovimiento = "ZIGZAG_UP"

        def estado_OBSTACULO_DOWN():
            if hay_obstaculo(abajo) == "OBSTACULO":
                print("OBSTACULO ABAJO - MOVIENDO DERECHA")
                self.direction = "derecha"
            else:
                self.estadoMovimiento = "ZIGZAG_DOWN"
        def estado_BASURA_DERECHA():
            self.direction = "derecha"
            self.estadoMovimiento = "BASURA_REGRESO_DERECHA"
        def estado_BASURA_DERECHA_RGRESO():
            self.direction = "izquierda"
            self.estadoMovimiento = ""
            
        def estado_BASURA_IZQUIERDA():
            self.direction = "izquierda"
            self.estadoMovimiento = "BASURA_REGRESO_IZQUIERDA"
        def estado_BASURA_IZQUIERDA_RGRESO():
            self.direction = "derecha"
            self.estadoMovimiento = ""

        tabla_estados = {
            "RETURN_TO_BASE": estado_RETURN_TO_BASE,
            "ZIGZAG_UP": estado_ZIGZAG_UP,
            "ZIGZAG_RIGHT_UP": estado_ZIGZAG_RIGHT_UP,
            "ZIGZAG_DOWN": estado_ZIGZAG_DOWN,
            "ZIGZAG_RIGHT_DOWN": estado_ZIGZAG_RIGHT_DOWN,
            "OBSTACULO_UP": estado_OBSTACULO_UP,
            "OBSTACULO_DOWN": estado_OBSTACULO_DOWN,
            "BASURA_DERECHA": estado_BASURA_DERECHA,
            "BASURA_REGRESO_DERECHA": estado_BASURA_DERECHA_RGRESO,
            "BASURA_IZQUIERDA": estado_BASURA_IZQUIERDA,
            "BASURA_REGRESO_IZQUIERDA": estado_BASURA_IZQUIERDA_RGRESO,
        }

        # Si el estado no existe → zigzag
        if estado not in tabla_estados:
            self.estadoMovimiento = "ZIGZAG_UP"
            estado = "ZIGZAG_UP"
        if estado == "ZIGZAG_UP" and hay_obstaculo(arriba) == "OBSTACULO":
            self.estadoMovimiento = "OBSTACULO_UP"
            estado = "OBSTACULO_UP"
        if estado == "ZIGZAG_DOWN" and hay_obstaculo(abajo) == "OBSTACULO":
            self.estadoMovimiento = "OBSTACULO_DOWN"
            estado = "OBSTACULO_DOWN"
        # Ejecutar estado
        tabla_estados[estado]()

        # ----------------------------
        # MOVIMIENTO FINAL
        # ----------------------------
        direcciones = {
            "arriba": arriba,
            "abajo": abajo,
            "derecha": derecha,
            "izquierda": izquierda,
        }

        destino = direcciones.get(self.direction)

        # Movimiento normal
        if destino and hay_obstaculo(destino) == "LIBRE":
            self.move_to(destino)
            return

        # Fallback
        for d, v in direcciones.items():
            if v and hay_obstaculo(v) == "LIBRE":
                self.direction = d
                self.move_to(v)
                return

        print("Roomba totalmente bloqueado")

    def move(self):

        if self.battery < self.distancia_base + 3 and not self.regresando_a_mapeo:
            print("Batería baja, regresando a base")
            
            # Guardar la celda actual antes de ir a cargar (si no está ya yendo)
            if not (hasattr(self, 'siguiendo_camino') and self.siguiendo_camino):
                self.celda_antes_de_cargar = self.cell
                print(f"Guardada celda antes de cargar: {self.celda_antes_de_cargar.coordinate}")
                
                if len(self.historialMapeado) > 0:
                    celda_base = self.historialMapeado[0]
                    if celda_base:
                        self.ir_a_celda_objetivo(celda_base)
                    else:
                        print("Error: celda base no disponible")
                        return
                else:
                    print("Error: historial vacío")
                    return

            objetivo_alcanzado = self.seguir_camino_objetivo()
            if objetivo_alcanzado:
                print("Base alcanzada - recargando batería")
                self.battery = 100  # Recargar batería
                self.siguiendo_camino = False
                
                # Ahora debe regresar a la última celda donde estaba mapeando
                if self.celda_antes_de_cargar:
                    print(f"Regresando a celda de mapeo: {self.celda_antes_de_cargar.coordinate}")
                    self.regresando_a_mapeo = True
                    self.ir_a_celda_objetivo(self.celda_antes_de_cargar)
            return

        if self.regresando_a_mapeo:
            objetivo_alcanzado = self.seguir_camino_objetivo()
            if objetivo_alcanzado:
                print("Celda de mapeo alcanzada - continuando mapeo")
                self.regresando_a_mapeo = False
                self.celda_antes_de_cargar = None
            return

        # CASO 3: Si estamos siguiendo un camino objetivo (no base, no regreso)
        if hasattr(self, 'siguiendo_camino') and self.siguiendo_camino:
            objetivo_alcanzado = self.seguir_camino_objetivo()
            if objetivo_alcanzado:
                self.borrarBasura()  # Limpiar al llegar
            return

        # CASO 4: Mapeo normal
        self.borrarBasura()
        self.mapeoRoomba()
        self.battery -= 1
        self.distancia_base = self.distancia_a_base()
 
        
        # Agregar la celda actual al historial DESPUÉS de mover (si no está ya)
        for vecino in self.cell.neighborhood:
            if vecino is None  :
        
                continue
            for a in vecino.agents:
                if isinstance(a, ObstacleAgent):
                    continue
            if vecino not in self.historialMapeado:
                self.historialMapeado.append(vecino)
                

    def step(self):
        self.move()
        pass



















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
        self.cell = cell

    def step(self):
        pass
    
    

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
        self.color = "blue"

    def move(self):
        """
        Determines the next empty cell in its neighborhood, and moves to it
        """
        pass

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        pass

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