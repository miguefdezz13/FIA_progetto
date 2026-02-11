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
    return abs(r1 - r2) + abs(c1 - c2)

class MinimaxAI:
    def __init__(self, depth=4):
        self.max_depth = depth

    def get_best_move(self, grid, anteater, ants):
        """
        Determines the optimal move for the Anteater using Minimax.
        
        Strategy:
        1. Identify the 'Target Ant' (Closest one).
        2. Run Minimax (Depth 4) to predict outcomes.
        3. Anteater (Max) tries to maximize Score (minimize distance).
        4. Ant (Min) tries to minimize Score (maximize distance).
        """
        # 1. Filter Alive Ants
        alive_ants = [a for a in ants if a.is_alive]
        if not alive_ants:
            return None # Victory state
            
        # 2. Select Target: Closest Ant
        # This simplifies the problem from "N Ants" to "1 vs 1 Duel".
        closest_ant = min(alive_ants, key=lambda a: manhattan_distance(a.r, a.c, anteater.r, anteater.c))

        # 3. Get Legal Moves for Anteater (Traps are VALID but LETHAL)
        # User Request: "Anteater can enter and die".
        neighbors = grid.get_neighbors(grid.get_cell(*anteater.position), avoid_traps=False)
        
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        # 4. Evaluate First Layer of Moves
        for move in neighbors:
            # If move is lethal, we don't recurse (Game Over state).
            # We assign a terrible score.
            if move.is_lethal:
                score = -10000 # Instant Death
            else:
                # Simulate Move
                # Recursive Call: It's now the Ant's turn (Maximizing=False)
                score = self.minimax(grid, 
                                     move.position, 
                                     closest_ant.position, 
                                     self.max_depth - 1, 
                                     False, # Next is Minimizer (Ant)
                                     alpha, 
                                     beta, 
                                     anteater.energy - move.cost, 
                                     closest_ant.energy)
            
            # Select Best
            if score > best_score:
                best_score = score
                best_move = move
            
            # Alpha-Beta Pruning
            alpha = max(alpha, best_score)
            
        return best_move

    def minimax(self, grid, anteater_pos, ant_pos, depth, is_maximizing, alpha, beta, ant_energy, anteater_energy):
        """
        Recursive Minimax Function.
        """
        ar, ac = anteater_pos
        tr, tc = ant_pos 
        
        # --- Terminal Conditions ---
        
        # 1. Caught the Ant
        if (ar, ac) == (tr, tc):
            return 10000 # High positive score for Anteater Victory
        
        # 2. Depth limit reached
        if depth == 0:
            return self.evaluate(ar, ac, tr, tc, anteater_energy)

        # --- Recursion ---
        
        if is_maximizing:
            # === ANTEATER'S TURN (Maximize Score) ===
            # Constraint: Can enter Traps (avoid_traps=False)
            max_eval = float('-inf')
            current_cell = grid.get_cell(ar, ac)
            neighbors = grid.get_neighbors(current_cell, avoid_traps=False)
            
            for move in neighbors:
                if move.is_lethal: 
                    # If we step on a trap, we die. Score is minimal.
                    # No recursion needed.
                    eval_score = -10000
                else:
                    new_energy = anteater_energy - move.cost
                    if new_energy <= 0: continue # Cannot move if exhausted
                
                    eval_score = self.minimax(grid, move.position, ant_pos, depth - 1, False, alpha, beta, ant_energy, new_energy)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha: # Prune
                    break
            
            # If no valid moves, it's a loss/stuck state
            return max_eval if max_eval != float('-inf') else -5000
            
        else:
            # === ANT'S TURN (Minimize Score) ===
            # Constraint: Can walk on Traps (Passes avoid_traps=False)
            min_eval = float('inf')
            current_cell = grid.get_cell(tr, tc)
            neighbors = grid.get_neighbors(current_cell, avoid_traps=False)
            
            for move in neighbors:
                new_energy = ant_energy - move.cost
                if new_energy <= 0: continue

                eval_score = self.minimax(grid, anteater_pos, move.position, depth - 1, True, alpha, beta, new_energy, anteater_energy)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha: # Prune
                    break
            
            return min_eval if min_eval != float('inf') else 10000

    def evaluate(self, ar, ac, tr, tc, anteater_energy):
        """
        Heuristic Evaluation.
        High Score = Good for Anteater.
        """
        dist = manhattan_distance(ar, ac, tr, tc)
        
        # AGGRESSIVE SCORING
        # Priority 1: Distance (Weight 20). Reduce distance -> Huge points.
        # Priority 2: Energy (Weight 0.5). Keep some battery.
        
        base_score = 1000
        dist_penalty = dist * 20
        energy_bonus = anteater_energy * 0.5
        
        return base_score - dist_penalty + energy_bonus
