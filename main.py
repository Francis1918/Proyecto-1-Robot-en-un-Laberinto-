import pygame
import os

# Clases del laberinto
from labyrinth import Labyrinth
from graphics import LabyrinthGraphics
from searchAgents import LabyrinthSearchProblem

# Algoritmos de búsqueda
from search import (
    depth_first_search,
    breadth_first_search,
    uniform_cost_search,
    a_star_search
)

# Funciones propias (ya separadas)
from evaluacion import evaluar_algoritmo, elegir_mejor_algoritmo
from ui import (
    Boton,
    BotonModerno,
    Dropdown,
    MENU,
    SELECCION,
    RESULTADOS,
    GRAFICA,
    COLORES,
    menu_principal_moderno,
    seleccionar_laberinto_moderno,
    dibujar_fondo_degradado
)
from graficas import dibujar_graficas_pygame

# --------------------------------------------------
# Selección de laberinto
# --------------------------------------------------

def seleccionar_laberinto(screen):
    """Wrapper para la función moderna de selección"""
    return seleccionar_laberinto_moderno(screen)

# --------------------------------------------------
# Menú principal
# --------------------------------------------------

def menu_principal(screen):
    """Wrapper para la función moderna del menú"""
    return menu_principal_moderno(screen)

# --------------------------------------------------
# Mostrar métricas de los algoritmos
# --------------------------------------------------  

def mostrar_resultados_texto(screen, resultados, mejor):
    fuente = pygame.font.SysFont(None, 24)
    x = 20
    y = screen.get_height() - 140

    for r in resultados:
        texto = (
            f"{r['algoritmo']} | "
            f"t={r['tiempo']:.4f}s | "
            f"pasos={r['pasos']} | "
            f"costo={r['costo']}"
        )

        if r == mejor:
            color = (255, 215, 0) # Dorado
        else:
            color = (255, 255, 255)  # BLANCO 

        render = fuente.render(texto, True, color)
        screen.blit(render, (x, y))
        y += 25

# --------------------------------------------------
# Bucle principal
# --------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robot en un Laberinto")

    estado = MENU
    resultados = []
    mejor = None
    lab = None
    problem = None

    while True:

        # -------------------------
        # MENU PRINCIPAL
        # -------------------------
        if estado == MENU:
            accion = menu_principal(screen)
            if accion == "salir":
                break
            estado = SELECCION

        # -------------------------
        # SELECCIÓN DE LABERINTO
        # -------------------------
        elif estado == SELECCION:
            archivo = seleccionar_laberinto(screen)
            if archivo is None:
                break
            if archivo == "volver":
                estado = MENU
                continue

            # Cargar laberinto seleccionado
            lab = Labyrinth(os.path.join("laberintos", archivo))
            problem = LabyrinthSearchProblem(lab)

            # Ejecutar algoritmos
            resultados = []
            algoritmos = [
                ("DFS", depth_first_search),
                ("BFS", breadth_first_search),
                ("UCS", uniform_cost_search),
                ("A*", a_star_search)
            ]

            for nombre, algoritmo in algoritmos:
                resultados.append(
                    evaluar_algoritmo(nombre, algoritmo, problem, lab)
                )

            mejor = elegir_mejor_algoritmo(resultados)

            estado = RESULTADOS

        # -------------------------
        # RESULTADOS 
        # -------------------------
        elif estado == RESULTADOS:
            
            boton_volver   = Boton("Volver",     620, 420, 150, 45, (180, 180, 180), "volver")
            boton_grafica  = Boton("Ver Gráfica",620, 475, 150, 45, (100, 150, 255), "grafica")
            boton_salir    = Boton("Salir",      620, 530, 150, 45, (200, 0, 0), "salir")
    

            fuente_btn = pygame.font.SysFont(None, 28)
            clock = pygame.time.Clock()


            # Visualizar la ruta del mejor algoritmo
            gui = LabyrinthGraphics(lab, screen)
            ruta = mejor["ruta"]

            viendo = True
            indice_ruta = 0

            seleccion_anterior = "MEJOR"

            # Dropdown para seleccionar algoritmo (opcional)
            opciones = ["MEJOR", "DFS", "BFS", "UCS", "A*"]
            dropdown = Dropdown(450, 420, 150, 30, opciones, seleccion=0)


            while viendo:
                screen.fill((0, 0, 0))

                gui.draw_labyrinth()

                # Dibujar robot en la posición actual
                seleccion = dropdown.opciones[dropdown.seleccion]

                if seleccion != seleccion_anterior:
                    indice_ruta = 0

                if seleccion == "MEJOR":
                    ruta_activa = mejor["ruta"]

                    COLOR_MEJOR = (255, 215, 0) # Dorado

                    gui.draw_path(ruta_activa, COLOR_MEJOR)

                    if ruta_activa and indice_ruta < len(ruta_activa):
                        gui.draw_robot(ruta_activa[indice_ruta])
                        indice_ruta += 1
                    elif ruta_activa:
                        gui.draw_robot(ruta_activa[-1])

                # -----------------------------------
                # OTROS → pintar ruta + robot animado
                # -----------------------------------
                else:
                    r_sel = next(r for r in resultados if r["algoritmo"] == seleccion)
                    ruta_activa = r_sel["ruta"]

                    color = {
                        "DFS": (255, 0, 0),
                        "BFS": (0, 255, 0),
                        "UCS": (0, 150, 255),
                        "A*":  (255, 255, 0)
                    }[seleccion]

                    # 🟢 Pintar TODA la ruta
                    gui.draw_path(ruta_activa, color)

                    # 🤖 Animar robot SOBRE la ruta
                    if ruta_activa and indice_ruta < len(ruta_activa):
                        gui.draw_robot(ruta_activa[indice_ruta])
                        indice_ruta += 1
                    elif ruta_activa:
                        gui.draw_robot(ruta_activa[-1])

                mostrar_resultados_texto(screen, resultados, mejor)

                boton_volver.dibujar(screen, fuente_btn)
                boton_grafica.dibujar(screen, fuente_btn)
                boton_salir.dibujar(screen, fuente_btn)
                dropdown.dibujar(screen, fuente_btn)


                for event in pygame.event.get():
                    dropdown.manejar_evento(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            viendo = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if boton_volver.click(event.pos):
                            estado = MENU
                            viendo = False
                        if boton_grafica.click(event.pos):
                            estado = GRAFICA
                            viendo = False
                        if boton_salir.click(event.pos):
                            pygame.quit()
                            return

                pygame.display.flip()
                clock.tick(10)  # controla velocidad del robot
                seleccion_anterior = seleccion

        # -------------------------
        # GRAFICAS
        # -------------------------
        elif estado == GRAFICA:

            boton_volver = Boton("Volver", 325, 520, 150, 45, (180,180,180), "volver")
            fuente_btn = pygame.font.SysFont(None, 28)
            clock = pygame.time.Clock()

            viendo = True
            while viendo:

                dibujar_graficas_pygame(screen, resultados)
                boton_volver.dibujar(screen, fuente_btn)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if boton_volver.click(event.pos):
                            estado = RESULTADOS
                            viendo = False

                pygame.display.flip()
                clock.tick(60)

        


    pygame.quit()


    

if __name__ == "__main__":
    main()