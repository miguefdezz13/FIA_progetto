"""
main.py

Main entry point for the Ant Eater Game.
Features:
- Complex Demo Map (Spiral, Swamp, Wall).
- Preview Path (Mode 1, 2, 3) -> Enter to Move.
- Toggleable Minimax (Mode 4).
"""

import pygame
import sys
import time

from config import *
from environment.grid import Grid
from environment.entities import Anteater, Ant
from environment.cell import TerrainType
from algorithms.pathfinding import bfs, astar, dfs
from algorithms.hill_climbing import hill_climbing_scent
from algorithms.minimax import MinimaxAI
from utils.visualization import init_screen, draw_grid, draw_entities, draw_path, draw_info

def get_closest_ant(anteater, ants):
    alive = [a for a in ants if a.is_alive]
    if not alive: return None
    return min(alive, key=lambda a: abs(a.r - anteater.r) + abs(a.c - anteater.c))

def calculate_path_cost(path):
    """Calculates total energy cost for a path (excluding start node)."""
    if not path or len(path) < 2: return 0
    total_cost = 0
    for cell in path[1:]: # Skip start cell
        if cell.terrain_type == TerrainType.MUD:
            total_cost += ENERGY_COST_MUD
        else:
            total_cost += ENERGY_COST_MOVE
    return total_cost

def main():
    screen = init_screen()
    clock = pygame.time.Clock()
    
    # Initialize World
    grid = Grid(ROWS, COLS) # Default gen
    # Initial State
    grid.generate_navigation_map()
    anteater = Anteater(0, 0)
    # Tactics Map Ants:
    # 1. Behind Gate A (Left Vertical) - Easy to see Trap Block
    # 2. Behind Gate B (Middle Horizontal) - Forces long detour
    # 3. Inside Spiral (Bottom Right)
    # 4. Behind Gate C (Bottom Left Corner)
    ants = [
        Ant(4, 9),    # Behind Left Gate (Trap at 4,6)
        Ant(13, 11),  # Behind Middle Gate (Trap at 10,11)
        Ant(15, 15),  # Spiral
        Ant(17, 2)    # Bottom Left Corner (Trap at 17,5)
    ] 
    
    running = True
    
    # State Machine
    current_algorithm = "None"
    status_text = "Select Mode (1-5)"
    
    preview_path = []  
    is_moving_preview = False 
    
    # Preview Stats for UI
    preview_steps_val = None
    preview_cost_val = None
    
    minimax_active = False 
    
    ai = MinimaxAI(depth=4)
    game_over = False
    anteater_steps = 0 
    
    last_move_time = 0
    move_delay = 100 

    while running:
        current_time = pygame.time.get_ticks()
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # MODE SELECTION
                if event.key == pygame.K_1:
                    current_algorithm = "BFS (Preview)"
                    minimax_active = False
                    is_moving_preview = False
                    preview_path = []
                    
                    target = get_closest_ant(anteater, ants)
                    if target:
                        preview_path, _ = bfs(grid, grid.get_cell(*anteater.position), grid.get_cell(*target.position))
                        # Calculate Stats
                        preview_cost_val = calculate_path_cost(preview_path)
                        preview_steps_val = max(0, len(preview_path) - 1)
                        
                        cost = preview_cost_val
                        steps = preview_steps_val
                        status_text = f"BFS: {steps} Steps | Cost {cost}E"
                    else:
                        status_text = "BFS: No Target"
                        preview_steps_val = None
                        preview_cost_val = None
                    
                elif event.key == pygame.K_2:
                    current_algorithm = "DFS (Preview)"
                    minimax_active = False
                    is_moving_preview = False
                    preview_path = []
                    
                    target = get_closest_ant(anteater, ants)
                    if target:
                        preview_path, _ = dfs(grid, grid.get_cell(*anteater.position), grid.get_cell(*target.position))
                        # Calculate Stats
                        preview_cost_val = calculate_path_cost(preview_path)
                        preview_steps_val = max(0, len(preview_path) - 1)
                        
                        cost = preview_cost_val
                        steps = preview_steps_val
                        status_text = f"DFS: {steps} Steps | Cost {cost}E"
                    else:
                        status_text = "DFS: No Target"
                        preview_steps_val = None
                        preview_cost_val = None

                elif event.key == pygame.K_3:
                    current_algorithm = "A* (Preview)"
                    minimax_active = False
                    is_moving_preview = False
                    preview_path = []
                    
                    target = get_closest_ant(anteater, ants)
                    if target:
                        preview_path, _ = astar(grid, grid.get_cell(*anteater.position), grid.get_cell(*target.position))
                        # Calculate Stats
                        preview_cost_val = calculate_path_cost(preview_path)
                        preview_steps_val = max(0, len(preview_path) - 1)
                        
                        cost = preview_cost_val
                        steps = preview_steps_val
                        status_text = f"A*: {steps} Steps | Cost {cost}E"
                    else:
                        status_text = "A*: No Target"
                        preview_steps_val = None
                        preview_cost_val = None

                elif event.key == pygame.K_4:
                    current_algorithm = "Scent HC (Preview)"
                    minimax_active = False
                    is_moving_preview = False
                    preview_path = []
                    
                    alive_ants = [a for a in ants if a.is_alive]
                    if alive_ants:
                        # Update scent once for preview
                        grid.update_scent(ants) 
                        preview_path, _ = hill_climbing_scent(grid, grid.get_cell(*anteater.position), ants)
                        
                        # Calculate Stats
                        preview_cost_val = calculate_path_cost(preview_path)
                        preview_steps_val = max(0, len(preview_path) - 1)

                        cost = preview_cost_val
                        steps = preview_steps_val
                        status_text = f"HC: {steps} Steps | Cost {cost}E"
                    else:
                        status_text = "HC: No Target"
                        preview_steps_val = None
                        preview_cost_val = None

                elif event.key == pygame.K_5:
                    # === MODE 5: MINIMAX DUEL ===
                    current_algorithm = "Minimax (Sim)"
                    status_text = "AI BATTLE: Duel Mode"
                    minimax_active = True
                    
                    # Disable Preview Mode flags
                    preview_path = []
                    is_moving_preview = False
                    preview_steps_val = None
                    preview_cost_val = None
                    
                    # Scenario Setup:
                    # Select Closest Target
                    target_ant = get_closest_ant(anteater, ants)
                    
                    if target_ant:
                        # Filter: Only keep the target
                        ants = [target_ant]
                        print(f"[DUEL] Focused on Ant at {target_ant.position}")
                    else:
                        status_text = "No Ants to Duel!"
                        minimax_active = False
                    
                    # Note: We do NOT reset the Anteater position. 
                    # The duel starts from WHEREVER the player currently is.

                elif event.key == pygame.K_RETURN:
                    # === EXECUTE MOVEMENT (Modes 1-3) ===
                    # If a preview path exists (from BFS/A*/HC), move along it.
                    if current_algorithm in ["BFS (Preview)", "A* (Preview)", "Scent HC (Preview)", "DFS (Preview)"]:
                        if preview_path:
                            status_text = "Executing..."
                            is_moving_preview = True
                            # Remove start node (current pos) from path if present
                            if preview_path and (preview_path[0].r == anteater.r and preview_path[0].c == anteater.c):
                                preview_path.pop(0)
                            
                            # We can keep showing the total cost of original path, or clear it.
                            # Usually better to clear or decrement. Let's clear for now as it becomes "active" moves.
                            # Or keep it as "Remaining Preview"? The prompt says "when visualized".
                            # When executing, we typically stop visualizing the full future path in the same way.
                            # But let's keep it until it's done or clear it?
                            # Let's clear it to distinguish "Planning" vs "Moving".
                            preview_steps_val = None
                            preview_cost_val = None

                elif event.key == pygame.K_r:
                    # === RESET GAME ===
                    # Reloads the Navigation Map.
                    # Resets Start Positions.
                    grid.generate_navigation_map()
                    anteater = Anteater(0, 0)
                    # Default Tactical Positions
                    ants = [Ant(4, 9), Ant(13, 11), Ant(15, 15), Ant(17, 2)]
                    
                    # Reset Game State
                    anteater_steps = 0
                    game_over = False
                    preview_path = []
                    is_moving_preview = False
                    preview_steps_val = None
                    preview_cost_val = None
                    minimax_active = False
                    current_algorithm = "None"
                    status_text = "Reset! Select Mode."

        # --- UPDATE LOGIC ---
        
        # 1. Preview Movement Execution (Modes 1, 2, 3)
        if is_moving_preview and not game_over:
            if current_time - last_move_time > move_delay:
                last_move_time = current_time
                if preview_path:
                    next_cell = preview_path.pop(0)
                    if anteater.move_to(next_cell):
                        anteater_steps += 1
                    
                    # Check Interactions
                    if next_cell.is_lethal:
                        game_over = True
                        status_text = "Died in Trap!"
                        is_moving_preview = False
                    
                    # Eat Ants
                    for ant in ants:
                        if ant.is_alive and ant.position == anteater.position:
                            ant.is_alive = False
                            anteater.energy = min(anteater.energy + 30, ANTEATER_MAX_ENERGY)
                            status_text = "Ant Eaten! Energy +30"
                            
                            # Check Win Condition
                            if not any(a.is_alive for a in ants):
                                game_over = True
                                status_text = "VICTORY! All Ants Eaten."
                else:
                    # Path Finished
                    is_moving_preview = False
                    if not game_over:
                        status_text = "Movement Complete."

        # 2. Minimax Logic (Mode 4)
        if minimax_active and not game_over:
            if current_time - last_move_time > GAME_SPEED:
                last_move_time = current_time
                
                # Anteater
                if anteater.recovering:
                    anteater.recharge()
                else:
                    best_move = ai.get_best_move(grid, anteater, ants)
                    if best_move:
                        anteater.move_to(best_move)
                        if best_move.is_lethal:
                            game_over = True
                            status_text = "Anteater died!"

                # Check Capture
                for ant in ants:
                    if ant.is_alive and ant.position == anteater.position:
                        ant.is_alive = False
                        status_text = "Ant Eaten!"

                # Ants Flee
                alive_ants = [a for a in ants if a.is_alive]
                if not alive_ants:
                     game_over = True
                     status_text = "All Ants Eaten! Win!"
                
                for ant in alive_ants:
                    if ant.recovering:
                        ant.recharge()
                    else:
                        neighbors = grid.get_neighbors(grid.get_cell(*ant.position))
                        if neighbors:
                            neighbors.sort(key=lambda n: abs(n.r - anteater.r) + abs(n.c - anteater.c), reverse=True)
                            for n in neighbors:
                                if n.terrain_type != TerrainType.WALL:
                                    if ant.move_to(n): break

        # Drawing
        screen.fill(COLOR_WHITE) # Dark Retro BG
        
        show_scent = (current_algorithm == "Scent HC (Preview)")
        draw_grid(screen, grid, show_scent=show_scent)
        
        if preview_path and not minimax_active:
             draw_path(screen, preview_path)

        draw_entities(screen, anteater, ants)
        
        # Pass steps to info
        draw_info(screen, anteater, ants, current_algorithm, status_text, steps=anteater_steps, preview_steps=preview_steps_val, preview_cost=preview_cost_val)
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        import datetime
        with open("crash.log", "w") as f:
            f.write(f"CRASH DATE: {datetime.datetime.now()}\n")
            f.write(traceback.format_exc())
        print("GAME CRASHED! Check crash.log")
        sys.exit(1)
