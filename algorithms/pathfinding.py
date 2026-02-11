"""
algorithms/pathfinding.py

Implementations of BFS and A* (A-Star).
"""

from collections import deque
import heapq
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.cell import TerrainType

def manhattan_distance(a, b):
    return abs(a.r - b.r) + abs(a.c - b.c)

class PathfindingTypes:
    BFS = "BFS"
    DFS = "DFS"
    ASTAR = "A*"

def bfs(grid, start_cell, target_cell, avoid_traps=True):
    """
    Breadth-First Search.
    Guarantees shortest path in terms of STEPS (edges), ignoring weights.
    """
    queue = deque([start_cell])
    visited = set()
    visited.add((start_cell.r, start_cell.c))
    
    # Store parents locally for path reconstruction
    parents = { (start_cell.r, start_cell.c): None }
    explored_nodes = []

    while queue:
        current = queue.popleft()
        explored_nodes.append(current)

        if current == target_cell:
            return reconstruct_path(current, parents), explored_nodes

        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            pos = (neighbor.r, neighbor.c)
            if pos not in visited:
                parents[pos] = current  
                visited.add(pos)
                queue.append(neighbor)
    
    return [], explored_nodes

def dfs(grid, start_cell, target_cell, avoid_traps=True):
    """
    Depth-First Search.
    Does NOT guarantee shortest path.
    """
    stack = [start_cell]
    visited = set()
    visited.add((start_cell.r, start_cell.c))
    
    # Store parents locally for path reconstruction
    parents = { (start_cell.r, start_cell.c): None }
    explored_nodes = []

    while stack:
        current = stack.pop()
        explored_nodes.append(current)

        if current == target_cell:
            return reconstruct_path(current, parents), explored_nodes

        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            pos = (neighbor.r, neighbor.c)
            if pos not in visited:
                parents[pos] = current  
                visited.add(pos)
                stack.append(neighbor)
    
    return [], explored_nodes

def multi_source_bfs(grid, sources, max_level):
    """
    Multi-source BFS for calculating scent/distance levels.
    sources: list of (cell, initial_level)
    Returns: dict of {(r, c): level}
    """
    visited = {} # pos: level
    queue = deque()

    for cell, level in sources:
        pos = (cell.r, cell.c)
        visited[pos] = level
        queue.append((cell, level))

    while queue:
        current, level = queue.popleft()
        
        if level <= 1: continue
        
        next_level = level - 1
        for neighbor in grid.get_neighbors(current, avoid_traps=False):
            pos = (neighbor.r, neighbor.c)
            # Only update if new level is higher (classic Dijkstra/BFS)
            if pos not in visited or visited[pos] < next_level:
                visited[pos] = next_level
                queue.append((neighbor, next_level))
                
    return visited

def astar(grid, start_cell, target_cell, avoid_traps=True):
    """
    A* Algorithm with weighted costs.
    Avoids Traps strictly if avoid_traps=True.
    """
    open_set = []
    # heapq format: (f_score, tie_breaker, cell)
    # We'll calculate f, g, h locally.
    
    g_scores = { (start_cell.r, start_cell.c): 0 }
    parents = { (start_cell.r, start_cell.c): None }
    
    start_h = manhattan_distance(start_cell, target_cell)
    """open_set se llama la cola, 1er es de comparacion, 2do desempate"""
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
            return reconstruct_path(current, parents), explored_nodes

        for neighbor in grid.get_neighbors(current, avoid_traps=avoid_traps):
            neigh_pos = (neighbor.r, neighbor.c)
            if neigh_pos in visited:
                continue

            # Standard A* g-score update
            tentative_g = g_scores[curr_pos] + neighbor.cost
            
            if neigh_pos not in g_scores or tentative_g < g_scores[neigh_pos]:
                parents[neigh_pos] = current
                g_scores[neigh_pos] = tentative_g
                h = manhattan_distance(neighbor, target_cell)
                f = tentative_g + h
                heapq.heappush(open_set, (f, id(neighbor), neighbor))

    return [], explored_nodes

def reconstruct_path(end_node, parents):
    path = []
    current = end_node
    while current:
        path.append(current)
        current = parents.get((current.r, current.c))
    return path[::-1] # Return reversed
