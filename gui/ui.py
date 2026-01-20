# --------------------------------------------------
# Componentes de interfaz gráfica (UI) reutilizables
# --------------------------------------------------

import pygame
import os

# Estados de la aplicación
MENU = "menu"
SELECCION = "seleccion"
RESULTADOS = "resultados"
GRAFICA = "grafica"

# Paleta de colores moderna
COLORES = {
    "fondo_oscuro": (25, 28, 38),
    "fondo_claro": (35, 40, 55),
    "primario": (66, 133, 244),       # Azul
    "primario_hover": (98, 160, 255),
    "secundario": (52, 168, 83),      # Verde
    "secundario_hover": (80, 190, 110),
    "peligro": (234, 67, 53),         # Rojo
    "peligro_hover": (255, 100, 90),
    "texto": (255, 255, 255),
    "texto_secundario": (180, 185, 200),
    "borde": (60, 65, 80),
}


class BotonModerno:
    """
    Botón con estilo moderno: degradado, bordes redondeados, hover
    """

    def __init__(self, texto, x, y, w, h, color_tipo="primario", accion=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color_tipo = color_tipo
        self.accion = accion
        self.hover = False

    def actualizar(self, mouse_pos):
        """Actualiza el estado de hover"""
        self.hover = self.rect.collidepoint(mouse_pos)

    def dibujar(self, screen, fuente):
        """Dibuja el botón con efectos visuales"""
        # Seleccionar color según tipo y estado hover
        if self.color_tipo == "primario":
            color = COLORES["primario_hover"] if self.hover else COLORES["primario"]
        elif self.color_tipo == "secundario":
            color = COLORES["secundario_hover"] if self.hover else COLORES["secundario"]
        elif self.color_tipo == "peligro":
            color = COLORES["peligro_hover"] if self.hover else COLORES["peligro"]
        else:
            color = COLORES["borde"]

        # Sombra
        sombra_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.w, self.rect.h)
        pygame.draw.rect(screen, (0, 0, 0, 80), sombra_rect, border_radius=8)

        # Botón principal
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Efecto de brillo en la parte superior
        brillo_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h // 3)
        color_brillo = tuple(min(c + 30, 255) for c in color)
        pygame.draw.rect(screen, color_brillo, brillo_rect, border_radius=8)

        # Texto centrado
        txt = fuente.render(self.texto, True, COLORES["texto"])
        screen.blit(
            txt,
            (self.rect.x + (self.rect.w - txt.get_width()) // 2,
             self.rect.y + (self.rect.h - txt.get_height()) // 2)
        )

    def click(self, pos):
        """Detecta si el botón fue presionado"""
        return self.rect.collidepoint(pos)


# Mantener compatibilidad con clase Boton original
class Boton(BotonModerno):
    def __init__(self, texto, x, y, w, h, color, accion):
        # Mapear colores antiguos a tipos
        if color == (0, 200, 0) or color == (52, 168, 83):
            tipo = "secundario"
        elif color == (200, 0, 0) or color == (234, 67, 53):
            tipo = "peligro"
        elif color == (100, 150, 255) or color == (66, 133, 244):
            tipo = "primario"
        else:
            tipo = "neutral"
        super().__init__(texto, x, y, w, h, tipo, accion)


class Dropdown:
    """
    Lista desplegable con estilo moderno
    """

    def __init__(self, x, y, w, h, opciones, seleccion=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.opciones = opciones
        self.seleccion = seleccion
        self.abierto = False
        self.hover_index = -1

    def dibujar(self, screen, fuente):
        """Dibuja el dropdown con estilo moderno"""
        # Fondo principal
        pygame.draw.rect(screen, COLORES["fondo_claro"], self.rect, border_radius=6)
        pygame.draw.rect(screen, COLORES["borde"], self.rect, 2, border_radius=6)

        # Texto seleccionado
        txt = fuente.render(self.opciones[self.seleccion], True, COLORES["texto"])
        screen.blit(txt, (self.rect.x + 12, self.rect.y + (self.rect.h - txt.get_height()) // 2))

        # Flecha indicadora
        flecha_x = self.rect.right - 20
        flecha_y = self.rect.centery
        if self.abierto:
            pygame.draw.polygon(screen, COLORES["texto"], [
                (flecha_x - 5, flecha_y + 3),
                (flecha_x + 5, flecha_y + 3),
                (flecha_x, flecha_y - 3)
            ])
        else:
            pygame.draw.polygon(screen, COLORES["texto"], [
                (flecha_x - 5, flecha_y - 3),
                (flecha_x + 5, flecha_y - 3),
                (flecha_x, flecha_y + 3)
            ])

        # Opciones desplegadas
        if self.abierto:
            for i, opcion in enumerate(self.opciones):
                r = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                # Color según hover
                if i == self.hover_index:
                    pygame.draw.rect(screen, COLORES["primario"], r)
                else:
                    pygame.draw.rect(screen, COLORES["fondo_claro"], r)
                pygame.draw.rect(screen, COLORES["borde"], r, 1)

                t = fuente.render(opcion, True, COLORES["texto"])
                screen.blit(t, (r.x + 12, r.y + (r.height - t.get_height()) // 2))

    def manejar_evento(self, event):
        """Gestiona eventos del dropdown"""
        if event.type == pygame.MOUSEMOTION and self.abierto:
            # Actualizar hover
            for i in range(len(self.opciones)):
                r = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                if r.collidepoint(event.pos):
                    self.hover_index = i
                    break
            else:
                self.hover_index = -1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.abierto = not self.abierto
            elif self.abierto:
                for i in range(len(self.opciones)):
                    r = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )
                    if r.collidepoint(event.pos):
                        self.seleccion = i
                        self.abierto = False
                        break
                else:
                    self.abierto = False


def dibujar_fondo_degradado(screen, color_arriba, color_abajo):
    """Dibuja un fondo con degradado vertical"""
    ancho, alto = screen.get_size()
    for y in range(alto):
        ratio = y / alto
        r = int(color_arriba[0] + (color_abajo[0] - color_arriba[0]) * ratio)
        g = int(color_arriba[1] + (color_abajo[1] - color_arriba[1]) * ratio)
        b = int(color_arriba[2] + (color_abajo[2] - color_arriba[2]) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (ancho, y))


def menu_principal_moderno(screen):
    """
    Menú principal con logo, información del grupo e integrantes
    """
    clock = pygame.time.Clock()

    # Cargar logo
    try:
        logo = pygame.image.load(os.path.join("assets", "logo_epn.png")).convert_alpha()
        # Escalar logo a un tamaño apropiado
        logo_size = 120
        logo = pygame.transform.smoothscale(logo, (logo_size, logo_size))
    except:
        logo = None

    # Fuentes
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_proyecto = pygame.font.SysFont("Arial", 22)
    fuente_grupo = pygame.font.SysFont("Arial", 18)
    fuente_integrantes = pygame.font.SysFont("Arial", 16)
    fuente_btn = pygame.font.SysFont("Arial", 22, bold=True)

    # Información del grupo
    titulo_proyecto = "Proyecto 1: Robot en un Laberinto"
    universidad = "Escuela Politécnica Nacional"
    grupo = "Grupo 2"
    integrantes = ["Ismael Freire", "Francis Bravo", "Joel Tinitana", "Daniel Menendez"]

    # Botones - posicionados horizontalmente en la parte inferior
    btn_ancho = 180
    btn_alto = 50
    espacio = 30  # espacio entre botones
    y_botones = 530  # posición Y en la parte inferior
    
    # Calcular posiciones X para centrar ambos botones
    total_ancho = (btn_ancho * 2) + espacio
    inicio_x = (screen.get_width() - total_ancho) // 2
    
    boton_iniciar = BotonModerno("▶  Iniciar", inicio_x, y_botones, btn_ancho, btn_alto, "secundario", "iniciar")
    boton_salir = BotonModerno("✕  Salir", inicio_x + btn_ancho + espacio, y_botones, btn_ancho, btn_alto, "peligro", "salir")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Fondo degradado
        dibujar_fondo_degradado(screen, (25, 35, 60), (15, 20, 35))

        # Logo centrado
        y_pos = 40
        if logo:
            logo_x = screen.get_width() // 2 - logo.get_width() // 2
            screen.blit(logo, (logo_x, y_pos))
            y_pos += logo.get_height() + 15

        # Nombre de la universidad
        txt_uni = fuente_grupo.render(universidad, True, COLORES["texto_secundario"])
        screen.blit(txt_uni, (screen.get_width() // 2 - txt_uni.get_width() // 2, y_pos))
        y_pos += 35

        # Línea separadora
        pygame.draw.line(screen, COLORES["borde"], 
                        (screen.get_width() // 2 - 150, y_pos), 
                        (screen.get_width() // 2 + 150, y_pos), 2)
        y_pos += 20

        # Título del proyecto
        txt_titulo = fuente_titulo.render(titulo_proyecto, True, COLORES["texto"])
        screen.blit(txt_titulo, (screen.get_width() // 2 - txt_titulo.get_width() // 2, y_pos))
        y_pos += 45

        # Grupo
        txt_grupo = fuente_proyecto.render(grupo, True, COLORES["primario"])
        screen.blit(txt_grupo, (screen.get_width() // 2 - txt_grupo.get_width() // 2, y_pos))
        y_pos += 35

        # Integrantes
        txt_int_label = fuente_grupo.render("Integrantes:", True, COLORES["texto_secundario"])
        screen.blit(txt_int_label, (screen.get_width() // 2 - txt_int_label.get_width() // 2, y_pos))
        y_pos += 25

        for integrante in integrantes:
            txt_int = fuente_integrantes.render(f"• {integrante}", True, COLORES["texto"])
            screen.blit(txt_int, (screen.get_width() // 2 - txt_int.get_width() // 2, y_pos))
            y_pos += 22

        # Actualizar y dibujar botones
        boton_iniciar.actualizar(mouse_pos)
        boton_salir.actualizar(mouse_pos)
        boton_iniciar.dibujar(screen, fuente_btn)
        boton_salir.dibujar(screen, fuente_btn)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_iniciar.click(event.pos):
                    return "iniciar"
                if boton_salir.click(event.pos):
                    return "salir"

        pygame.display.flip()
        clock.tick(60)


def seleccionar_laberinto_moderno(screen):
    """
    Pantalla de selección de laberinto con estilo moderno
    """
    clock = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_btn = pygame.font.SysFont("Arial", 20)

    archivos = os.listdir(os.path.join("data", "mazes"))

    # Crear botones para cada laberinto
    botones = []
    btn_ancho = 300
    btn_alto = 45
    centro_x = screen.get_width() // 2 - btn_ancho // 2
    y = 150

    for archivo in archivos:
        # Determinar color según dificultad
        nombre_lower = archivo.lower()
        if "facil" in nombre_lower or "easy" in nombre_lower:
            tipo = "secundario"
        elif "dificil" in nombre_lower or "hard" in nombre_lower:
            tipo = "peligro"
        else:
            tipo = "primario"

        botones.append(BotonModerno(archivo.replace(".txt", ""), centro_x, y, btn_ancho, btn_alto, tipo, archivo))
        y += 60

    # Botón volver
    boton_volver = BotonModerno("← Volver", 20, 20, 100, 35, "neutral", "volver")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Fondo degradado
        dibujar_fondo_degradado(screen, (25, 35, 60), (15, 20, 35))

        # Título
        txt_titulo = fuente_titulo.render("Selecciona un Laberinto", True, COLORES["texto"])
        screen.blit(txt_titulo, (screen.get_width() // 2 - txt_titulo.get_width() // 2, 70))

        # Actualizar y dibujar botones
        boton_volver.actualizar(mouse_pos)
        boton_volver.dibujar(screen, fuente_btn)

        for boton in botones:
            boton.actualizar(mouse_pos)
            boton.dibujar(screen, fuente_btn)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.click(event.pos):
                    return "volver"
                for boton in botones:
                    if boton.click(event.pos):
                        return boton.accion

        pygame.display.flip()
        clock.tick(60)
