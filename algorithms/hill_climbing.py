"""

algorithms/hill_climbing.py


Hill Climbing with Simulated Annealing.
Instead of finding a full path, this acts as a 'local search' agent logic.
It decides the NEXT BEST STEP. 

However, for consistency with the prompt "Ant Eater needs to move...", 
standard Hill Climbing in pathfinding usually means: 
Greedy Best First Search (always pick best neighbor) but without backtracking (no queue).

To implement Simulated Annealing:
We will attempt to generate a full path or a sequence of moves by iterating.
If we get stuck (local optimum), we accept a bad move with probability P.
"""



import random
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.cell import TerrainType

def manhattan_distance(a, b):
    return abs(a.r - b.r) * abs(a.c - b.c)

def hill_climbing_scent(grid, start_cell, ants, max_iterations=1000):
    """
    Hill Climbing based on SCENT (Pheromone).
    The Anteater climbs the gradient of HIGHEST Pheromone level.
    """
    grid.update_scent([])

    current = start_cell
    path = [current]
    explored_nodes = path

    T_initial = 100.0
    alpha = 1.05
    T = T_initial

