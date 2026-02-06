"""
environment/cell.py

Defines the Cell class which represents a single tile on the grid.
"""

from enum import Enum
import sys
import os


COST_TRAP = 5  # High cost for traps (for pathfinding)
COST_MUD = 3   # Higher cost for mud (for pathfinding)
COST_NORMAL = 1 # Standard cost for normal terrain

class TerrainType(Enum):
    NORMAL = 1
    MUD = 2
    TRAP = 3
    WALL = 4

class Cell:
    def __init__(self, r, c, terrain_type=TerrainType.NORMAL):
        self.r = r
        self.c = c
        self.terrain_type = terrain_type
        self.pheromone_level = 0.0 # For Hill Climbing Scent

    @property
    def position(self):
        return (self.r, self.c)

    @property
    def cost(self):
        if self.terrain_type == TerrainType.NORMAL:
            # Note: config.COST_NORMAL/MUD are weights for pathfinding
            return COST_NORMAL
        elif self.terrain_type == TerrainType.MUD:
            return COST_MUD
        elif self.terrain_type == TerrainType.TRAP:
            return COST_TRAP
        elif self.terrain_type == TerrainType.WALL:
            return float('inf')
        return 1

    @property
    def is_lethal(self):
        return self.terrain_type == TerrainType.TRAP

    # String representation for debugging, for example: Cell(2, 3, MUD)
    def __repr__(self):
        return f"Cell({self.r}, {self.c}, {self.terrain_type.name})"