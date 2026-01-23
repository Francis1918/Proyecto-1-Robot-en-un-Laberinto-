import pygame

# Definición de colores basados en los requisitos
COLOR_PARED = (0, 0, 0)        # Negro 
COLOR_INICIO = (0, 255, 0)     # Verde 
COLOR_META = (255, 0, 0)       # Rojo 
COLOR_PLANO = (255, 255, 255)  # Blanco 
COLOR_EMPINADO = (200, 200, 200) # Gris (para diferenciar el costo 2)

class LabyrinthGraphics:
    def __init__(self, labyrinth, screen, tile_size=20, offset_x=0, offset_y=0):
        self.lab = labyrinth
        self.screen = screen
        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.robot_img = pygame.image.load("assets/robot.png").convert_alpha()
        self.robot_img = pygame.transform.scale(
            self.robot_img,
            (tile_size, tile_size)
        )

    def draw_labyrinth(self):
        """Dibuja el laberinto celda por celda."""
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
                    (self.offset_x + c * self.tile_size,
                     self.offset_y + r * self.tile_size,
                     self.tile_size, self.tile_size)
                )

    def draw_path(self, ruta, color):
        for (fila, col) in ruta:
            x = self.offset_x + col * self.tile_size + self.tile_size // 2
            y = self.offset_y + fila * self.tile_size + self.tile_size // 2
            pygame.draw.circle(
                self.screen,
                color,
                (x, y),
                self.tile_size // 4
            )


    def draw_robot(self, state):
        """Dibuja el robot en una posición."""
        r, c = state
        self.screen.blit(
            self.robot_img,
            (self.offset_x + c * self.tile_size,
             self.offset_y + r * self.tile_size)
        )