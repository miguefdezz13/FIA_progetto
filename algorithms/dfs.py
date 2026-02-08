import sys
import os

# Configuración de ruta para importar desde el entorno
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def dfs(grid, start_cell, target_cell, avoid_traps=True):
    """
    Depth-First Search (Búsqueda en Profundidad).
    Explora lo más lejos posible por cada rama antes de retroceder.
    NO garantiza el camino más corto.
    """
    # Usamos una lista como Pila (Stack) -> LIFO
    stack = [start_cell]
    visited = set()
    visited.add((start_cell.r, start_cell.c))
    
    # Diccionario para reconstruir el camino: hijo -> padre
    parents = { (start_cell.r, start_cell.c): None }
    explored_nodes = []

    while stack:
        # Sacamos el ÚLTIMO elemento añadido (comportamiento de oso hormiguero)
        current = stack.pop()
        explored_nodes.append(current)

        # Si llegamos al objetivo, reconstruimos la ruta
        if current == target_cell:
            return reconstruct_path(current, parents), explored_nodes

        # Expandimos a los vecinos
        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            pos = (neighbor.r, neighbor.c)
            if pos not in visited:
                parents[pos] = current  
                visited.add(pos)
                stack.append(neighbor)
    
    # Si el stack se vacía sin encontrar la meta
    return [], explored_nodes

def reconstruct_path(end_node, parents):
    """
    Camina hacia atrás desde la meta usando el diccionario de padres.
    """
    path = []
    current = end_node
    while current:
        path.append(current)
        current = parents.get((current.r, current.c))
    return path[::-1] # Invertimos para que vaya de Inicio a Fin