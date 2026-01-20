# --------------------------------------------------
# Componentes de interfaz gráfica (UI) reutilizables
# --------------------------------------------------

import pygame

# Estados de la aplicación
MENU = "menu"
SELECCION = "seleccion"
RESULTADOS = "resultados"
GRAFICA = "grafica"


class Boton:
    """
    Clase genérica para botones en Pygame
    """

    def __init__(self, texto, x, y, w, h, color, accion):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color = color
        self.accion = accion

    def dibujar(self, screen, fuente):
        """Dibuja el botón en pantalla"""
        pygame.draw.rect(screen, self.color, self.rect)
        txt = fuente.render(self.texto, True, (0, 0, 0))
        screen.blit(
            txt,
            (self.rect.x + (self.rect.w - txt.get_width()) // 2,
             self.rect.y + (self.rect.h - txt.get_height()) // 2)
        )

    def click(self, pos):
        """Detecta si el botón fue presionado"""
        return self.rect.collidepoint(pos)


class Dropdown:
    """
    Lista desplegable para seleccionar algoritmos
    """

    def __init__(self, x, y, w, h, opciones, seleccion=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.opciones = opciones
        self.seleccion = seleccion
        self.abierto = False

    def dibujar(self, screen, fuente):
        """Dibuja el dropdown y sus opciones"""
        pygame.draw.rect(screen, (180,180,180), self.rect)
        txt = fuente.render(self.opciones[self.seleccion], True, (0,0,0))
        screen.blit(txt, (self.rect.x+10, self.rect.y+10))

        if self.abierto:
            for i, opcion in enumerate(self.opciones):
                r = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i+1)*self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                pygame.draw.rect(screen, (220,220,220), r)
                t = fuente.render(opcion, True, (0,0,0))
                screen.blit(t, (r.x+10, r.y+10))

    def manejar_evento(self, event):
        """Gestiona clics del mouse sobre el dropdown"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.abierto = not self.abierto
            elif self.abierto:
                for i in range(len(self.opciones)):
                    r = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i+1)*self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )
                    if r.collidepoint(event.pos):
                        self.seleccion = i
                        self.abierto = False
