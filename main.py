import pygame
import os

# Clases del laberinto (desde src/)
from src.labyrinth import Labyrinth
from src.search_agents import LabyrinthSearchProblem

# Algoritmos de búsqueda (desde src/)
from src.search import (
    depth_first_search,
    breadth_first_search,
    uniform_cost_search,
    a_star_search
)

# Utilidades (desde utils/)
from utils.evaluacion import evaluar_algoritmo, elegir_mejor_algoritmo

# Interfaz gráfica (desde gui/)
from gui.ui import (
    Boton,
    BotonModerno,
    Dropdown,
    MENU,
    SELECCION,
    MODO_VISUALIZACION,
    RESULTADOS,
    GRAFICA,
    COLORES,
    menu_principal_moderno,
    seleccionar_laberinto_moderno,
    seleccionar_modo_visualizacion,
    dibujar_fondo_degradado
)
from gui.graphics import LabyrinthGraphics
from gui.charts import dibujar_graficas_pygame

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
    archivo_seleccionado = None
    modo_visualizacion = "mejor"  # "mejor" o "todos"

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

            archivo_seleccionado = archivo
            estado = MODO_VISUALIZACION

        # -------------------------
        # MODO DE VISUALIZACIÓN
        # -------------------------
        elif estado == MODO_VISUALIZACION:
            modo = seleccionar_modo_visualizacion(screen, archivo_seleccionado)
            if modo is None:
                break
            if modo == "volver":
                estado = SELECCION
                continue

            modo_visualizacion = modo

            # Cargar laberinto seleccionado
            lab = Labyrinth(os.path.join("data", "mazes", archivo_seleccionado))
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
            
            fuente_btn = pygame.font.SysFont(None, 28)
            clock = pygame.time.Clock()

            # Variables para animación
            algoritmos_orden = ["DFS", "BFS", "UCS", "A*"]
            colores_algoritmos = {
                "DFS": (255, 0, 0),
                "BFS": (0, 255, 0),
                "UCS": (0, 150, 255),
                "A*":  (255, 255, 0)
            }

            if modo_visualizacion == "todos":
                # ========================================
                # MODO TODOS: 4 laberintos en paralelo
                # ========================================
                # Calcular tamaño de cada laberinto para que quepan 4 (2x2)
                lab_filas = len(lab.grid)
                lab_cols = len(lab.grid[0]) if lab.grid else 0

                # Área disponible: pantalla 800x600, reservar espacio para botones
                area_laberintos_ancho = 800
                area_laberintos_alto = 450  # Dejar espacio para botones abajo

                # Calcular tile_size para que quepan 2 laberintos por fila/columna
                tile_size_w = (area_laberintos_ancho // 2 - 20) // lab_cols if lab_cols > 0 else 15
                tile_size_h = (area_laberintos_alto // 2 - 40) // lab_filas if lab_filas > 0 else 15
                tile_size = min(tile_size_w, tile_size_h, 20)  # Max 20 para que no sea muy grande

                # Calcular dimensiones reales del laberinto
                lab_ancho = lab_cols * tile_size
                lab_alto = lab_filas * tile_size

                # Calcular offsets para centrar los 4 laberintos en grilla 2x2
                espacio_h = (area_laberintos_ancho - 2 * lab_ancho) // 3
                espacio_v = (area_laberintos_alto - 2 * lab_alto) // 3

                posiciones = [
                    (espacio_h, espacio_v + 20),  # DFS - arriba izquierda
                    (espacio_h * 2 + lab_ancho, espacio_v + 20),  # BFS - arriba derecha
                    (espacio_h, espacio_v * 2 + lab_alto + 20),  # UCS - abajo izquierda
                    (espacio_h * 2 + lab_ancho, espacio_v * 2 + lab_alto + 20),  # A* - abajo derecha
                ]

                # Crear 4 instancias de gráficos
                guis = []
                for i, (ox, oy) in enumerate(posiciones):
                    guis.append(LabyrinthGraphics(lab, screen, tile_size, ox, oy))

                # Índices de ruta para cada algoritmo
                indices_ruta = [0, 0, 0, 0]

                boton_volver = Boton("Volver", 200, 520, 120, 40, (180, 180, 180), "volver")
                boton_grafica = Boton("Ver Grafica", 340, 520, 130, 40, (100, 150, 255), "grafica")
                boton_salir = Boton("Salir", 490, 520, 100, 40, (200, 0, 0), "salir")

                viendo = True
                while viendo:
                    screen.fill((30, 30, 40))

                    # Título
                    fuente_titulo = pygame.font.SysFont(None, 28)
                    txt_titulo = fuente_titulo.render("Comparacion de Algoritmos - Animacion Paralela", True, (255, 255, 255))
                    screen.blit(txt_titulo, (800 // 2 - txt_titulo.get_width() // 2, 5))

                    # Dibujar cada laberinto con su algoritmo
                    for i, alg in enumerate(algoritmos_orden):
                        r_sel = next(r for r in resultados if r["algoritmo"] == alg)
                        ruta_activa = r_sel["ruta"]
                        color = colores_algoritmos[alg]
                        ox, oy = posiciones[i]

                        # Dibujar laberinto
                        guis[i].draw_labyrinth()

                        # Dibujar ruta
                        guis[i].draw_path(ruta_activa, color)

                        # Dibujar robot animado
                        if ruta_activa and indices_ruta[i] < len(ruta_activa):
                            guis[i].draw_robot(ruta_activa[indices_ruta[i]])
                            indices_ruta[i] += 1
                        elif ruta_activa:
                            guis[i].draw_robot(ruta_activa[-1])

                        # Etiqueta del algoritmo
                        fuente_label = pygame.font.SysFont(None, 22)
                        es_mejor = (alg == mejor["algoritmo"])
                        label_text = f"{alg}" + (" (MEJOR)" if es_mejor else "")
                        txt_label = fuente_label.render(label_text, True, color)
                        screen.blit(txt_label, (ox + lab_ancho // 2 - txt_label.get_width() // 2, oy - 18))

                        # Mostrar estadísticas debajo
                        fuente_stats = pygame.font.SysFont(None, 16)
                        stats_text = f"Pasos: {r_sel['pasos']} | Costo: {r_sel['costo']}"
                        txt_stats = fuente_stats.render(stats_text, True, (200, 200, 200))
                        screen.blit(txt_stats, (ox + lab_ancho // 2 - txt_stats.get_width() // 2, oy + lab_alto + 2))

                    # Dibujar botones
                    boton_volver.dibujar(screen, fuente_btn)
                    boton_grafica.dibujar(screen, fuente_btn)
                    boton_salir.dibujar(screen, fuente_btn)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                viendo = False
                            if event.key == pygame.K_r:  # Reiniciar animación
                                indices_ruta = [0, 0, 0, 0]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if boton_volver.click(event.pos):
                                estado = SELECCION
                                viendo = False
                            if boton_grafica.click(event.pos):
                                estado = GRAFICA
                                viendo = False
                            if boton_salir.click(event.pos):
                                pygame.quit()
                                return

                    pygame.display.flip()
                    clock.tick(10)

            else:
                # ========================================
                # MODO MEJOR: Un solo laberinto
                # ========================================
                boton_volver = Boton("Volver", 620, 420, 150, 45, (180, 180, 180), "volver")
                boton_grafica = Boton("Ver Grafica", 620, 475, 150, 45, (100, 150, 255), "grafica")
                boton_salir = Boton("Salir", 620, 530, 150, 45, (200, 0, 0), "salir")

                gui = LabyrinthGraphics(lab, screen)
                ruta = mejor["ruta"]

                viendo = True
                indice_ruta = 0
                seleccion_anterior = "MEJOR"

                opciones = ["MEJOR", "DFS", "BFS", "UCS", "A*"]
                dropdown = Dropdown(450, 420, 150, 30, opciones, seleccion=0)

                while viendo:
                    screen.fill((0, 0, 0))
                    gui.draw_labyrinth()

                    seleccion = dropdown.opciones[dropdown.seleccion]

                    if seleccion != seleccion_anterior:
                        indice_ruta = 0

                    if seleccion == "MEJOR":
                        ruta_activa = mejor["ruta"]
                        COLOR_MEJOR = (255, 215, 0)
                        gui.draw_path(ruta_activa, COLOR_MEJOR)

                        if ruta_activa and indice_ruta < len(ruta_activa):
                            gui.draw_robot(ruta_activa[indice_ruta])
                            indice_ruta += 1
                        elif ruta_activa:
                            gui.draw_robot(ruta_activa[-1])
                    else:
                        r_sel = next(r for r in resultados if r["algoritmo"] == seleccion)
                        ruta_activa = r_sel["ruta"]
                        color = colores_algoritmos[seleccion]

                        gui.draw_path(ruta_activa, color)

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
                                estado = SELECCION
                                viendo = False
                            if boton_grafica.click(event.pos):
                                estado = GRAFICA
                                viendo = False
                            if boton_salir.click(event.pos):
                                pygame.quit()
                                return

                    pygame.display.flip()
                    clock.tick(10)
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