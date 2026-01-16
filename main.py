# This is a sample Python script.
from labyrinth import Labyrinth
from graphics import LabyrinthGraphics
import pygame
import sys
import os

def main():
    # 1. Cargar el laberinto [cite: 50]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    labyrinth_path = os.path.join(script_dir, "labyrinth_map.txt")
    lab = Labyrinth(labyrinth_path)
    
    # 2. Inicializar gráficos [cite: 50]
    gui = LabyrinthGraphics(lab)
    
    # 3. Bucle principal de visualización [cite: 51]
    running = True
    while running:
        gui.draw_labyrinth()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()