
Ant-Eater AI Simulator 
        Authors: Miguel Angel Fernández y Miguel Alvarez


An interactive Artificial Intelligence simulator developed in Python using Pygame. This project demonstrates the use of various search algorithms and AI techniques in a dynamic environment where an Ant Eater must hunt ants while managing energy levels and avoiding traps.
Project Objective

The main goal is to compare and visualize the behavior of different search algorithms (informed and uninformed) and decision-making techniques (Minimax) within an environment featuring diverse terrain types and movement penalties.


Key Features

    Search Algorithms: Implementation of BFS, DFS, A*, Hill Climbing (scent trail-based), and Minimax.

    Dynamic Environment:

        Different terrains: Normal, Mud, and Walls.

        Lethal traps that end the simulation.

        Energy System: Movement consumes energy; food (ants) restores it.

    Interactive Graphical Interface:

        Path pre-visualization before execution.

        Keyboard-selectable game modes.

        Real-time statistics (steps, energy cost, algorithm status).



Repository Structure

    main.py: Entry point of the simulator. Manages the main loop and events.

    config.py: Global configurations (grid size, colors, energy costs, speed).

    algorithms/: Implementation of search engines.

        pathfinding.py: BFS, DFS, A*.

        hill_climbing.py: Scent-based optimization.

        minimax.py: Logic for the AI duel.

    environment/: Physical world definition.

        grid.py: Map management and navigation generation.

        entities.py: Classes for the Ant Eater and Ants.

        cell.py: Terrain types and their properties.

    utils/: Auxiliary utilities.
        visualization.py: Tool for the graphical interface
Usage
    Controls:

        1: BFS Mode (Breadth-First Search).

        2: DFS Mode (Depth-First Search).

        3: A* Mode (Optimal Search).

        4: Hill Climbing Mode (Scent Trail).

        5: Minimax Mode (AI Duel).

        ENTER: Execute pre-visualized movement.

        R: Reset simulation.


Regarding the replication of this work, our process was structured as follows:

First, we identified a suitable context to test various algorithms, allowing for a comprehensive comparison of their respective characteristics. The course platform served as a primary source of inspiration and provided significant guidance regarding the analytical aspects of the project.

The algorithms were implemented based on the theoretical principles covered in class. For the Graphical User Interface (GUI), we adapted and reused a framework from a previous project with similar functional requirements. Throughout the development phase, we utilized AI-assisted debugging 
to resolve complex technical errors. Once the code reached a stable state, it was documented and managed via GitHub.

Ultimately, the most critical factor was ensuring the project’s conceptual framework was thoroughly structured prior to implementation.

