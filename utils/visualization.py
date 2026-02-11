"""
utils/visualization.py

Handles Pygame rendering with Retro aesthetics.
"""

import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from environment.cell import TerrainType

# Asset Cache
ASSETS = {}

def init_screen():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Ant Eater Simulation: v2.0 Retro")
    return screen

def load_assets():
    if ASSETS: return
    
    try:
        # Load and Scale
        cell_size = config.GRID_SIZE
        
        # Anteater
        img = pygame.image.load(os.path.join("assets", "anteater.png"))
        ASSETS["anteater"] = pygame.transform.scale(img, (cell_size, cell_size))
        
        # Ant
        img = pygame.image.load(os.path.join("assets", "ant.png"))
        ASSETS["ant"] = pygame.transform.scale(img, (int(cell_size*0.8), int(cell_size*0.8)))
        
        # Mud
        img = pygame.image.load(os.path.join("assets", "mud.png"))
        ASSETS["mud"] = pygame.transform.scale(img, (cell_size, cell_size))
        
    except Exception as e:
        print(f"Warning: Could not load assets: {e}. Fallback to shapes.")

def draw_grid(screen, grid, show_scent=False):
    load_assets() # Ensure loaded
    cell_size = config.GRID_SIZE
    
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.get_cell(r, c)
            rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
            
            # Base
            color = config.COLOR_TERRAIN_NORMAL
            
            if cell.terrain_type == TerrainType.MUD:
                color = config.COLOR_TERRAIN_MUD
                pygame.draw.rect(screen, color, rect)
                if "mud" in ASSETS:
                    screen.blit(ASSETS["mud"], (c*cell_size, r*cell_size))
            elif cell.terrain_type == TerrainType.TRAP:
                color = config.COLOR_TERRAIN_TRAP
                pygame.draw.rect(screen, color, rect)
            elif cell.terrain_type == TerrainType.WALL:
                color = config.COLOR_BLACK
                pygame.draw.rect(screen, color, rect)
            else:
                pygame.draw.rect(screen, color, rect)
            
            # Scent Overlay (Original Yellow Uniform)
            if show_scent and cell.pheromone_level > 0:
                intensity = min(20, cell.pheromone_level)
                alpha = int((intensity / 20.0) * 200) 
                
                s = pygame.Surface((cell_size, cell_size))
                s.set_alpha(alpha)
                s.fill((255, 255, 0)) # Yellow
                screen.blit(s, (c * cell_size, r * cell_size))

            pygame.draw.rect(screen, config.COLOR_GRID_LINE, rect, 1) # Border

def draw_entities(screen, anteater, ants):
    load_assets()
    cell_size = config.GRID_SIZE
    
    # Draw Anteater
    ax, ay = anteater.c * cell_size, anteater.r * cell_size
    if "anteater" in ASSETS:
        screen.blit(ASSETS["anteater"], (ax, ay))
    else:
        pygame.draw.circle(screen, config.COLOR_ANTEATER, (ax + cell_size//2, ay + cell_size//2), cell_size//3)
    
    # Draw Ants
    for ant in ants:
        if ant.is_alive:
            tx, ty = ant.c * cell_size, ant.r * cell_size
            if "ant" in ASSETS:
                offset = (cell_size - ASSETS["ant"].get_width()) // 2
                screen.blit(ASSETS["ant"], (tx + offset, ty + offset))
            else:
                pygame.draw.circle(screen, config.COLOR_ANT, (tx + cell_size//2, ty + cell_size//2), cell_size//4)

def draw_path(screen, path):
    if not path: return
    cell_size = config.GRID_SIZE
    
    for cell in path:
        rect = pygame.Rect(cell.c * cell_size, cell.r * cell_size, cell_size, cell_size)
        s = pygame.Surface((cell_size, cell_size))
        s.set_alpha(100) # Transparent overlay
        s.fill(config.COLOR_PATH)
        screen.blit(s, (cell.c * cell_size, cell.r * cell_size))

def draw_info(screen, anteater, ants, current_algo, status_text, steps=0, preview_steps=None, preview_cost=None):
    font = pygame.font.SysFont("Courier New", 15, bold=True) # Slightly smaller font
    title_font = pygame.font.SysFont("Verdana", 20, bold=True)
    
    # UI Panel Settings
    panel_x = config.COLS * config.GRID_SIZE
    panel_width = config.SCREEN_WIDTH - panel_x
    panel_height = config.SCREEN_HEIGHT
    
    # Retro Dark Panel
    pygame.draw.rect(screen, (10, 10, 20), (panel_x, 0, panel_width, panel_height))
    pygame.draw.line(screen, (0, 255, 255), (panel_x, 0), (panel_x, panel_height), 3) # Cyan Border
    
    margin_left = panel_x + 20
    y_offset = 30
    
    # Title
    title = title_font.render("ANT EATER", True, (255, 0, 255)) # Magenta Title
    screen.blit(title, (margin_left, y_offset))
    y_offset += 40
    
    # Helper to draw text
    def draw_line(label, value, color=(200, 200, 200)):
        nonlocal y_offset
        lbl = font.render(label, True, (150, 150, 150))
        val = font.render(str(value), True, color)
        screen.blit(lbl, (margin_left, y_offset))
        screen.blit(val, (margin_left + 160, y_offset)) # More offset for values
        y_offset += 25

    # --- SECTION: GAME STATUS ---
    status_header = font.render("--- GAME STATUS ---", True, (0, 255, 255))
    screen.blit(status_header, (margin_left, y_offset))
    y_offset += 25

    draw_line("ALGO:", current_algo, (0, 255, 0))
    draw_line("STATUS:", status_text, (255, 255, 0))
    y_offset += 10
    draw_line("STEPS:", str(steps), (255, 255, 255))
    
    y_offset += 25
    
    # --- SECTION: ANTEATER ---
    player_header = font.render("--- ANTEATER ---", True, (0, 255, 255))
    screen.blit(player_header, (margin_left, y_offset))
    y_offset += 25

    # Anteater Stats
    draw_line("ENERGY:", f"{anteater.energy}/{anteater.max_energy}", config.COLOR_ANTEATER)
    
    pass_y = y_offset
    # Health Bar for Anteater
    bar_width = 150
    ratio = anteater.energy / anteater.max_energy
    pygame.draw.rect(screen, (50, 0, 0), (margin_left, pass_y, bar_width, 8))
    pygame.draw.rect(screen, config.COLOR_ANTEATER, (margin_left, pass_y, bar_width * ratio, 8))
    y_offset += 20
    
    # Path Cost Widget
    if preview_cost is not None:
        draw_line("PATH COST:", f"{preview_cost}E", (255, 100, 100))
        y_offset += 5 

    if preview_steps is not None:
        draw_line("PREVIEW:", str(preview_steps), (100, 255, 255))
    
    y_offset += 25

    # --- SECTION: ANTS ---
    enemy_header = font.render("--- ANTS ---", True, (0, 255, 255))
    screen.blit(enemy_header, (margin_left, y_offset))
    y_offset += 25

    alive_count = sum(1 for a in ants if a.is_alive)
    draw_line("ANTS LEFT:", f"{alive_count}/{len(ants)}", config.COLOR_ANT)
    
    for i, ant in enumerate(ants):
        name = f"ANT {i+1}"
        if not ant.is_alive:
            draw_line(name, "DEAD", (50, 50, 50))
        else:
            draw_line(name, f"{ant.energy}/{ant.max_energy}", config.COLOR_ANT)
            # Mini Bar
            r_ant = ant.energy / ant.max_energy
            pygame.draw.rect(screen, (0, 0, 50), (margin_left, y_offset-5, 100, 4))
            pygame.draw.rect(screen, config.COLOR_ANT, (margin_left, y_offset-5, 100 * r_ant, 4))
            y_offset += 5

    y_offset += 30
    
    # --- SECTION: CONTROLS ---
    ctrl_header = font.render("--- CONTROLS ---", True, (0, 255, 255))
    screen.blit(ctrl_header, (margin_left, y_offset))
    y_offset += 25

    controls = [
        ("1", "BFS PREVIEW"),
        ("2", "DFS PREVIEW"),
        ("3", "A* PREVIEW"),
        ("4", "SCENT PREVIEW"),
        ("5", "AI BATTLE"),
        ("ENTER", "EXECUTE MOVE"),
        ("R", "RESET GAME"),
    ]
    
    for k, d in controls:
        draw_line(k, d, (255, 165, 0))
