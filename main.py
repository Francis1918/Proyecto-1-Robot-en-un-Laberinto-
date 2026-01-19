from labyrinth import Labyrinth
from graphics import LabyrinthGraphics
from searchAgents import LabyrinthSearchProblem
from search import (
    depth_first_search,
    breadth_first_search,
    uniform_cost_search,
    a_star_search
)
import pygame
import os
import time
import matplotlib.pyplot as plt


def evaluar_algoritmo(nombre, algoritmo, problem, lab):
    """
    Ejecuta un algoritmo de búsqueda y mide su rendimiento.
    """
    inicio = time.perf_counter()
    ruta = algoritmo(problem)
    fin = time.perf_counter()

    tiempo = fin - inicio
    pasos = len(ruta)

    # Calcular costo total del camino
    costo = 0
    for state in ruta:
        costo += lab.get_cost(state)

    return {
        "algoritmo": nombre,
        "tiempo": tiempo,
        "pasos": pasos,
        "costo": costo,
        "ruta": ruta
    }

def elegir_mejor_algoritmo(resultados):
    max_t = max(r["tiempo"] for r in resultados)
    max_p = max(r["pasos"] for r in resultados)
    max_c = max(r["costo"] for r in resultados)

    for r in resultados:
        r["score"] = (
            r["tiempo"] / max_t +
            r["pasos"] / max_p +
            r["costo"] / max_c
        )

    return min(resultados, key=lambda r: r["score"])


MENU = "menu"
SELECCION = "seleccion"
RESULTADOS = "resultados"
GRAFICA = "grafica"
class Boton:
    def __init__(self, texto, x, y, w, h, color, accion):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color = color
        self.accion = accion

    def dibujar(self, screen, fuente):
        pygame.draw.rect(screen, self.color, self.rect)
        txt = fuente.render(self.texto, True, (0, 0, 0))
        screen.blit(
            txt,
            (self.rect.x + (self.rect.w - txt.get_width()) // 2,
             self.rect.y + (self.rect.h - txt.get_height()) // 2)
        )

    def click(self, pos):
        return self.rect.collidepoint(pos)

def dibujar_graficas_pygame(screen, resultados):
    screen.fill((25, 25, 25))
    fuente_titulo = pygame.font.SysFont(None, 36)
    fuente = pygame.font.SysFont(None, 22)

    algoritmos = [r["algoritmo"] for r in resultados]
    tiempos = [r["tiempo"] for r in resultados]
    pasos = [r["pasos"] for r in resultados]
    costos = [r["costo"] for r in resultados]

    # Normalizar valores
    def normalizar(valores, altura_max):
        m = max(valores)
        return [int((v / m) * altura_max) for v in valores]

    h_t = normalizar(tiempos, 200)
    h_p = normalizar(pasos, 200)
    h_c = normalizar(costos, 200)

    base_y = 450
    ancho = 35
    separacion = 60

    # Posiciones base
    bases_x = [40, 300, 560]

    # ---- TITULOS ----
    screen.blit(fuente_titulo.render("Tiempo", True, (255,255,255)), (120, 50))
    screen.blit(fuente_titulo.render("Pasos", True, (255,255,255)), (380, 50))
    screen.blit(fuente_titulo.render("Costo", True, (255,255,255)), (635, 50))

    for i, alg in enumerate(algoritmos):

        # Tiempo
        pygame.draw.rect(
            screen, (0, 140, 255),
            (bases_x[0] + i*separacion, base_y - h_t[i], ancho, h_t[i])
        )

        # Pasos
        pygame.draw.rect(
            screen, (0, 255, 150),
            (bases_x[1] + i*separacion, base_y - h_p[i], ancho, h_p[i])
        )

        # Costo
        pygame.draw.rect(
            screen, (255, 160, 0),
            (bases_x[2] + i*separacion, base_y - h_c[i], ancho, h_c[i])
        )

        # Etiquetas
        txt = fuente.render(alg, True, (255,255,255))
        screen.blit(txt, (bases_x[0] + i*separacion, base_y + 8))
        screen.blit(txt, (bases_x[1] + i*separacion, base_y + 8))
        screen.blit(txt, (bases_x[2] + i*separacion, base_y + 8))


def seleccionar_laberinto(screen):
    fuente = pygame.font.SysFont(None, 32)
    archivos = os.listdir("laberintos")

    botones = []
    y = 150
    for archivo in archivos:
        botones.append(
            Boton(archivo, 250, y, 300, 40, (180, 180, 180), archivo)
        )
        y += 60

    while True:
        screen.fill((200, 200, 200))

        for boton in botones:
            boton.dibujar(screen, fuente)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton.click(event.pos):
                        return boton.accion

        pygame.display.flip()

def menu_principal(screen):
    fuente = pygame.font.SysFont(None, 40)

    boton_iniciar = Boton("Iniciar", 300, 200, 200, 60, (0, 200, 0), "iniciar")
    boton_salir = Boton("Salir", 300, 300, 200, 60, (200, 0, 0), "salir")

    while True:
        screen.fill((220, 220, 220))

        boton_iniciar.dibujar(screen, fuente)
        boton_salir.dibujar(screen, fuente)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_iniciar.click(event.pos):
                    return "iniciar"
                if boton_salir.click(event.pos):
                    return "salir"

        pygame.display.flip()

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
            color = (0, 255, 0)      # VERDE → método elegido
        else:
            color = (255, 255, 255)  # BLANCO → los demás

        render = fuente.render(texto, True, color)
        screen.blit(render, (x, y))
        y += 25

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

            while viendo:
                screen.fill((0, 0, 0))

                gui.draw_labyrinth()

                # Dibujar robot en la posición actual
                if ruta and indice_ruta < len(ruta):
                    gui.draw_robot(ruta[indice_ruta])
                    indice_ruta += 1
                elif ruta:
                    gui.draw_robot(ruta[-1])

                mostrar_resultados_texto(screen, resultados, mejor)

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