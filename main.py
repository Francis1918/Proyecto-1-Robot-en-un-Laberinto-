from labyrinth import Labyrinth
from graphics import LabyrinthGraphics
from searchAgents import LabyrinthSearchProblem, SearchAgent
from search import depth_first_search
import pygame
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    labyrinth_path = os.path.join(script_dir, "labyrinth_map.txt")
    lab = Labyrinth(labyrinth_path)
    problem = LabyrinthSearchProblem(lab)
    
    # Crear agente y pedirle que resuelva el problema usando DFS
    agent = SearchAgent(depth_first_search)
    ruta_encontrada = agent.get_plan(problem)
    
    gui = LabyrinthGraphics(lab)
    
    running = True
    while running:
        gui.draw_labyrinth()
        
        # Si se encontró una ruta, dibujarla [cite: 48]
        if ruta_encontrada:
            gui.draw_path(ruta_encontrada)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    main()