"""
config.py

Global configurations for the Ant Eater Game.
Includes screen dimensions, colors, terrain costs, and game settings.
"""

# Screen & Grid Settings
GRID_SIZE = 35  # Increased from 20 for larger icons/map
ROWS = 20
COLS = 20

# Auto-calc screen size to fit grid + panel
SCREEN_WIDTH = (COLS * GRID_SIZE) + 400 # 400px for side panel (increased from 300)
SCREEN_HEIGHT = max((ROWS * GRID_SIZE), 800) # Increased from 700 to 800 for more space

# Colors (Vivid Retro Palette)
COLOR_WHITE = (20, 20, 30)      # Dark Board Background (Space/Arcade)
COLOR_BLACK = (0, 0, 0)         # Walls
COLOR_GRID_LINE = (50, 50, 70)  # Subtle grid

# Terrain Colors (Neon/Vivid)
COLOR_TERRAIN_NORMAL = (30, 30, 40)    # Dark background for tiles
COLOR_TERRAIN_MUD = (139, 69, 19)      # Classic Mud Brown (Texture covers this mostly)
COLOR_TERRAIN_TRAP = (255, 0, 255)     # Hot Magenta (Lethal)

# Entity Colors (Fallbacks if images fail)
COLOR_ANTEATER = (255, 50, 50)   # Bright Red
COLOR_ANT = (0, 255, 255)        # Cyan
COLOR_PATH = (0, 120, 255)       # Dodger Blue (Requested)
COLOR_OPEN_SET = (173, 216, 230)
COLOR_CLOSED_SET = (100, 149, 237)

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

# Delay for visualization (ms)
GAME_SPEED = 200