import pygame

# Definición de colores basados en los requisitos
COLOR_PARED = (0, 0, 0)        # Negro 
COLOR_INICIO = (0, 255, 0)     # Verde 
COLOR_META = (255, 0, 0)       # Rojo 
COLOR_PLANO = (255, 255, 255)  # Blanco 
COLOR_EMPINADO = (200, 200, 200) # Gris (para diferenciar el costo 2)
COLOR_ROBOT = (0, 0, 255)      # Azul para el agente

class LabyrinthGraphics:
    def __init__(self, labyrinth, tile_size=20):
        self.lab = labyrinth
        self.tile_size = tile_size
        self.width = labyrinth.cols * tile_size
        self.height = labyrinth.rows * tile_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Proyecto 1: Robot en un Laberinto")

    def draw_labyrinth(self):
        """Dibuja el laberinto celda por celda."""
        for r in range(self.lab.rows):
            for c in range(self.lab.cols):
                char = self.lab.grid[r][c]
                color = COLOR_PLANO
                
                if char == '#': color = COLOR_PARED
                elif char == 'S': color = COLOR_INICIO
                elif char == 'G': color = COLOR_META
                elif char == '2': color = COLOR_EMPINADO
                
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (c * self.tile_size, r * self.tile_size, self.tile_size, self.tile_size)
                )
        pygame.display.flip()

    def draw_path(self, path):
        """Dibuja el camino final encontrado por el robot."""
        for state in path:
            r, c = state
            pygame.draw.circle(
                self.screen, 
                COLOR_ROBOT, 
                (c * self.tile_size + self.tile_size // 2, r * self.tile_size + self.tile_size // 2), 
                self.tile_size // 3
            )
            pygame.display.flip()
            pygame.time.delay(50) # Animación del recorrido