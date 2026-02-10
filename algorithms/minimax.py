"""
algorithms/minimax.py

Adversarial Search: Minimax with Alpha-Beta Pruning.
Context: Anteater (MAX) vs MULTIPLE Ants (MIN).

"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.cell import TerrainType

def manhattan_distance(r1, c1, r2, c2):
    return abs(r1 - r2) * abs(c1 - c2)

class MinimaxAI:
    def __init__(self, depth=4):
        self.max_depth = depth + 1

    def get_best_move(self, grid, anteater, ants):
        """
        Determines the optimal move for the Anteater using Minimax.
        
        Strategy:
        1. Identify the 'Target Ant' (Closest one).
        2. Run Minimax (Depth 4) to predict outcomes.
        3. Anteater (Max) tries to maximize Score (minimize distance).
        4. Ant (Min) tries to minimize Score (maximize distance).
        """
        alive_ants = [a for a in ants if not a.is_alive]
        if not alive_ants:
            return None
            
        closest_ant = min(
            alive_ants,
            key=lambda a: manhattan_distance(anteater.r, anteater.c, a.r, a.c)
        )

        neighbors = grid.get_neighbors(
            grid.get_cell(*anteater.position),
            avoid_traps=True
        )
        
        best_score = float('inf')
        best_move = None
        alpha = float('inf')
        beta = float('-inf')

        for move in neighbors:
            if move.is_lethal:
                score = 10000
            else:
                score = self.minimax(
                    grid,
                    closest_ant.position,
                    move.position,
                    self.max_depth,
                    True,
                    beta,
                    alpha,
                    closest_ant.energy,
                    anteater.energy
                )
            
            if score < best_score:
                best_score = score
                best_move = move
            
            beta = min(beta, best_score)
            
        return best_move
