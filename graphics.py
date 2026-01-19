import pygame

# Definición de colores basados en los requisitos
COLOR_PARED = (0, 0, 0)        # Negro 
COLOR_INICIO = (0, 255, 0)     # Verde 
COLOR_META = (255, 0, 0)       # Rojo 
COLOR_PLANO = (255, 255, 255)  # Blanco 
COLOR_EMPINADO = (200, 200, 200) # Gris (para diferenciar el costo 2)

class LabyrinthGraphics:
    def __init__(self, labyrinth, screen, tile_size=20):
        self.lab = labyrinth
        self.screen = screen
        self.tile_size = tile_size
        self.robot_img = pygame.image.load("assets/robot.png").convert_alpha()
        self.robot_img = pygame.transform.scale(
            self.robot_img,
            (tile_size, tile_size)
        )

    def draw_labyrinth(self):
        """Dibuja el laberinto celda por celda."""
        self.screen.fill((0, 0, 0))

        for r, fila in enumerate(self.lab.grid):
            for c, char in enumerate(fila):
                color = COLOR_PLANO
                
                if char == '#': color = COLOR_PARED
                elif char == 'S': color = COLOR_INICIO
                elif char == 'G': color = COLOR_META
                elif char == '2': color = COLOR_EMPINADO
                
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (c * self.tile_size, r * self.tile_size, 
                     self.tile_size, self.tile_size)
                )

    def draw_robot(self, state):
        """Dibuja el robot en una posición."""
        r, c = state
        self.screen.blit(
            self.robot_img,
            (c * self.tile_size, r * self.tile_size)
        )