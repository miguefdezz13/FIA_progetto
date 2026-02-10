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

