"""
config.py

Global configurations for the Ant Eater Game.
Includes screen dimensions, colors, terrain costs, and game settings.
"""

# Screen & Grid Settings
ROWS = 20
COLS = 20

# Costs
COST_NORMAL = 1
COST_MUD = 2
COST_TRAP = 999 

# Energy Settings
ANTEATER_MAX_ENERGY = 150
ANT_MAX_ENERGY = 50
ENERGY_COST_MOVE = 5
ENERGY_COST_MUD = 20
RECHARGE_ANTEATER = 15 # Fast recovery for the hunter
RECHARGE_ANT = 5       # Slower recovery for the prey
