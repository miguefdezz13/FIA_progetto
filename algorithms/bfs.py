from collections import deque
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.cell import TerrainType


def bfs(grid, start_cell, target_cell, avoid_traps=True):
    """
    Breadth-First Search.
    Guarantees shortest path in terms of STEPS (edges), ignoring weights.
    """
    queue = deque([start_cell])
    visited = set()
    visited.add((start_cell.r, start_cell.c))
    
    parents = {(start_cell.r, start_cell.c): None}
    explored_nodes = []

    while queue:
        current = queue.popleft()
        explored_nodes.append(current)

        if current == target_cell:
            return reconstruct_path_bfs(current, parents), explored_nodes

        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            pos = (neighbor.r, neighbor.c)
            if pos not in visited:
                parents[pos] = current
                visited.add(pos)
                queue.append(neighbor)
    
    return [], explored_nodes


def reconstruct_path_bfs(end_node, parents):
    path = []
    current = end_node
    while current:
        path.append(current)
        current = parents.get((current.r, current.c))
    return path[::-1]
