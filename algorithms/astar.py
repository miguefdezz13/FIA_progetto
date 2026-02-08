
import heapq
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.cell import TerrainType


def manhattan_distance(a, b):
    return abs(a.r - b.r) + abs(a.c - b.c)


def astar(grid, start_cell, target_cell, avoid_traps=True):
    """
    A* Algorithm with weighted costs.
    Avoids Traps strictly if avoid_traps=True.
    """
    open_set = []
    
    g_scores = {(start_cell.r, start_cell.c): 0}
    parents = {(start_cell.r, start_cell.c): None}
    
    start_h = manhattan_distance(start_cell, target_cell)
    heapq.heappush(open_set, (start_h, id(start_cell), start_cell))
    
    visited = set()
    explored_nodes = []

    while open_set:
        _, _, current = heapq.heappop(open_set)
        curr_pos = (current.r, current.c)
        
        if curr_pos in visited:
            continue
        visited.add(curr_pos)
        explored_nodes.append(current)

        if current == target_cell:
            return reconstruct_path_astar(current, parents), explored_nodes

        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            neigh_pos = (neighbor.r, neighbor.c)
            if neigh_pos in visited:
                continue

            tentative_g = g_scores[curr_pos] + neighbor.cost
            
            if neigh_pos not in g_scores or tentative_g < g_scores[neigh_pos]:
                parents[neigh_pos] = current
                g_scores[neigh_pos] = tentative_g
                h = manhattan_distance(neighbor, target_cell)
                f = tentative_g + h
                heapq.heappush(open_set, (f, id(neighbor), neighbor))

    return [], explored_nodes


def reconstruct_path_astar(end_node, parents):
    path = []
    current = end_node
    while current:
        path.append(current)
        current = parents.get((current.r, current.c))
    return path[::-1]
