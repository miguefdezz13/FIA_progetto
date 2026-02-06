"""
environment/entities.py

Defines the Entity class and its subclasses (Anteater, Ant).
Handles position, energy management, and types.
"""

import sys
import os

ENERGY_COST_MUD = 2  # Higher cost for moving through mud
ENERGY_COST_MOVE = 1  # Standard cost for moving through normal terrain 
RECHARGE_ANTEATER = 3  # Anteater recovers faster
RECHARGE_ANT = 1  # Ant recovers slower

class Entity:
    def __init__(self, r, c, max_energy, recharge_rate, name="Entity"):
        self.r = r
        self.c = c
        self.max_energy = max_energy
        self.recharge_rate = recharge_rate
        self.energy = max_energy
        self.name = name
        self.is_alive = True
        self.recovering = False  # Status when restoring energy

    @property
    def position(self):
        return (self.r, self.c)

    def move_to(self, cell):
        """
        Moves to a target cell if enough energy is available.
        """
        #If recovering, we skip turn (simulate in main logic by not calling move)
        if self.recovering:
            self.recharge()
            return False

        t_name = cell.terrain_type.name
        
        if t_name == "MUD":
            energy_cost = ENERGY_COST_MUD
        elif t_name == "WALL":
            return False
        else:
            energy_cost = ENERGY_COST_MOVE
        
        # Check affordability
        if self.energy >= energy_cost:
            self.r = cell.r
            self.c = cell.c
            self.energy -= energy_cost
            return True
        else:
            self.start_recovery()
            return False

    def start_recovery(self):
        """Enters recovery mode."""
        self.recovering = True
        print(f"{self.name} is exhausted! Resting...")

    def recharge(self):
        """Restores energy."""
        self.energy += self.recharge_rate
        if self.energy >= self.max_energy:
            self.energy = self.max_energy
            self.recovering = False
            print(f"{self.name} fully recovered!")

class Anteater(Entity):
    def __init__(self, r, c):
        super().__init__(r, c, ANTEATER_MAX_ENERGY, RECHARGE_ANTEATER, "Anteater")

class Ant(Entity):
    def __init__(self, r, c):
        super().__init__(r, c, ANT_MAX_ENERGY, RECHARGE_ANT, "Ant")
