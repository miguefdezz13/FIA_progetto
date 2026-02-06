"""
environment/grid.py

Defines the Grid class which manages the 2D array of Cells.
"""

import random
from .cell import Cell, TerrainType
import sys
import os

ROWS = 20
COLS = 20


class Grid:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.generate_navigation_map()

    def generate_navigation_map(self):
        """
        Generates the main game map (The "Tactical Playground").
        
        Zones:
        1. scattered_mud: Random patches of high cost terrain.
        2. trap_gates: Walls with a Trap in the middle. 
           - Ants can pass (TerrainType.TRAP does not block them).
           - Anteater cannot pass (Treats TRAP as Wall).
        3. spiral: A spiral wall structure at bottom-right to test pathfinding/HC depth.
        """
        # Reset grid to plain
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].terrain_type = TerrainType.NORMAL

        # --- 1. Scattered Mud (High Cost Zones) ---
        # Existing hardcoded spots + Random Scatter
        mud_spots = [
            (3, 3), (3, 4), (4, 3),
            (7, 8), (8, 7), (8, 8), (8, 9), (9, 8),
            (12, 2), (12, 3), (13, 2),
            (2, 15), (2, 16), (3, 15)
        ]
        for r, c in mud_spots:
            self.cells[r][c].terrain_type = TerrainType.MUD
            
        # Add MORE Mud randomly (approx 10% of remaining free space)
        # Avoid overwriting Walls or Traps
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].terrain_type == TerrainType.NORMAL:
                    if random.random() < 0.15: # 15% chance for mud
                        self.cells[r][c].terrain_type = TerrainType.MUD

        # --- 2. Trap Gates (The "Filters") ---
        # Gate A: Vertical Barrier on the Left
        for r in range(2, 7): self.cells[r][6].terrain_type = TerrainType.WALL
        self.cells[4][6].terrain_type = TerrainType.TRAP # The Hole
        
        # Gate B: Horizontal Barrier in the Middle
        for c in range(8, 14): self.cells[10][c].terrain_type = TerrainType.WALL
        self.cells[10][11].terrain_type = TerrainType.TRAP
        
        # Gate C: Protecting the bottom-left corner
        for r in range(15, 19): self.cells[r][5].terrain_type = TerrainType.WALL
        self.cells[17][5].terrain_type = TerrainType.TRAP

        # --- 3. The Spiral (Hill Climbing Trap) ---
        for c in range(14, 19): self.cells[14][c].terrain_type = TerrainType.WALL
        for r in range(14, 19): self.cells[r][18].terrain_type = TerrainType.WALL
        for c in range(14, 19): self.cells[18][c].terrain_type = TerrainType.WALL
        for r in range(16, 19): self.cells[r][14].terrain_type = TerrainType.WALL
        # Inner part
        for c in range(15, 17): self.cells[16][c].terrain_type = TerrainType.WALL
        self.cells[15][16].terrain_type = TerrainType.WALL
        
        # --- 4. Extra Walls (New Request) ---
        # Add some random internal walls to create choke points
        # Horizontal snippet
        for c in range(1, 5): self.cells[6][c].terrain_type = TerrainType.WALL
        # Vertical snippet
        for r in range(8, 12): self.cells[r][2].terrain_type = TerrainType.WALL
        
        # Ensure Start is clear
        self.cells[0][0].terrain_type = TerrainType.NORMAL
            
    def smooth_map(self):
        # Disabled for fixed map
        pass

    def get_neighbors_8(self, r, c):
        """Get 8-way neighbors for CA smoothing."""
        n = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    n.append((nr, nc))
        return n

    def clear_zone(self, center_r, center_c, radius):
        """Clears obstacles around a point."""
        for r in range(center_r - radius, center_r + radius + 1):
            for c in range(center_c - radius, center_c + radius + 1):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.cells[r][c].terrain_type = TerrainType.NORMAL

    def get_neighbors(self, cell, avoid_traps=False):
        """Returns valid neighbors (Up, Down, Left, Right)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = cell.r + dr, cell.c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.cells[nr][nc]
                if neighbor.terrain_type == TerrainType.WALL:
                    continue
                if avoid_traps and neighbor.terrain_type == TerrainType.TRAP:
                    continue
                    
                neighbors.append(neighbor)
        return neighbors
        
    def update_scent(self, ants):
        """
        Updates the 'pheromone_level' using BFS (Dijkstra) propagation.
        Scent should NOT pass through walls and should decay with distance.
        """
        # Reset
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].pheromone_level = 0.0
        
        # Multi-Source BFS
        queue = []
        visited = set()
        
        for ant in ants:
            if ant.is_alive:
                cell = self.cells[ant.r][ant.c]
                cell.pheromone_level = 20.0 # Max Scent
                queue.append((cell, 20.0))
                visited.add((ant.r, ant.c))
        
        while queue:
            # SAFETY CHECK: Prevent infinite loops
            # In a 20x20 grid, BFS shouldn't take more than ~400 expansions.
            # But we re-visit nodes due to noise. Let's cap at 5000.
            if len(visited) > 10000: # Just a sanity clamp
                 break
                 
            current, level = queue.pop(0)
            
            if level <= 1: continue # Decay limit
            
            next_level = level - 1 # Linear decay per step
            
            neighbors = self.get_neighbors(current)
            for n in neighbors:
                # Scent blocked only by Walls (handled by get_neighbors)
                    
                if (n.r, n.c) not in visited:
                    # Update scent
                    n.pheromone_level = next_level
                    visited.add((n.r, n.c))
                    queue.append((n, next_level))

    def get_cell(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.cells[r][c]
        return None