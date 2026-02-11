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
    return abs(a.r - b.r) + abs(a.c - b.c)

def hill_climbing_scent(grid, start_cell, ants, max_iterations=1000):
    """
    Hill Climbing based on SCENT (Pheromone).
    The Anteater climbs the gradient of HIGHEST Pheromone level.
    """
    # 1. Update Scent Grid first
    grid.update_scent(ants)
    
    current = start_cell
    path = [current]
    explored_nodes = [current]
    
    # Annealing Parameters
    T_initial = 100.0
    alpha = 0.95
    T = T_initial

    for i in range(max_iterations):
        # Stop if standing on an ant (Scent is max)
        # Note: In grid.py we set scent = 20 - dist. So on top of ant it is 20.
        if current.pheromone_level >= 20: 
            break

        # User Request: Hill Climbing MUST follow scent even into Traps.
        # "Blindly following the nose"
        neighbors = grid.get_neighbors(current, avoid_traps=False)
        if not neighbors:
            break
        
        # Sort by scent (Descent: Max to Min)
        # If a Trap has high scent (because it's the shortest path for scent propagation),
        # the Anteater will pick it.
        neighbors.sort(key=lambda n: n.pheromone_level, reverse=True)
        
        best_next = None
        for n in neighbors:
            # We only skip Walls (already handled by get_neighbors) or visited loops
            if n not in path:
                if n.pheromone_level > current.pheromone_level:
                    best_next = n
                    break
                elif n.pheromone_level == current.pheromone_level:
                    # Plateau: Pick if better than nothing
                    best_next = n
                    break
        
        # If no non-visited improving or plateau neighbor, pick the best overall (even if visited)
        if best_next is None:
            best_next = neighbors[0] # This is the best_neighbor from original code

        current_scent = current.pheromone_level
        next_scent = best_next.pheromone_level
        
        # Delta E: We want to INCREASE scent.
        # Improvement = Next > Current
        delta = next_scent - current_scent

        chosen = None

        if delta > 0:
            # Improvement!
            chosen = best_next
        else:
            # Worsening (Scent decreases or stays same - Local Maxima / Plateau)
            # Simulated Annealing Probability
            # We want to maximize, so 'bad move' is reducing scent.
            # prob = exp( delta / T ) because delta is negative
            safe_T = max(T, 0.0001)
            probability = math.exp(delta / safe_T)
            
            if random.random() < probability:
                # Accept bad move (wander randomly)
                chosen = random.choice(neighbors) 
            else:
                # Reject - but we must move or stop? 
                # In strict HC we stop. In Game, we might just pick best available or stay.
                # Let's pick best available to keep moving towards 'flat' if necessary
                chosen = best_next
        
        current = chosen
        path.append(current)
        explored_nodes.append(current)

        T = T * alpha
    
    return path, explored_nodes
