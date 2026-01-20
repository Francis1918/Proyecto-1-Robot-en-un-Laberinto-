# --------------------------------------------------
# Visualización gráfica de métricas en Pygame
# --------------------------------------------------

import pygame


def dibujar_graficas_pygame(screen, resultados):
    """
    Dibuja gráficas comparativas de:
    - Tiempo de ejecución
    - Número de pasos
    - Costo del camino
    """

    screen.fill((25, 25, 25))
    fuente_titulo = pygame.font.SysFont(None, 36)
    fuente = pygame.font.SysFont(None, 22)

    algoritmos = [r["algoritmo"] for r in resultados]
    tiempos = [r["tiempo"] for r in resultados]
    pasos = [r["pasos"] for r in resultados]
    costos = [r["costo"] for r in resultados]

    # Normaliza valores para dibujar barras proporcionales
    def normalizar(valores, altura_max):
        m = max(valores)
        return [int((v / m) * altura_max) for v in valores]

    h_t = normalizar(tiempos, 200)
    h_p = normalizar(pasos, 200)
    h_c = normalizar(costos, 200)

    base_y = 450
    ancho = 35
    separacion = 60
    bases_x = [40, 300, 560]

    # Títulos
    screen.blit(fuente_titulo.render("Tiempo", True, (255,255,255)), (120, 50))
    screen.blit(fuente_titulo.render("Pasos", True, (255,255,255)), (380, 50))
    screen.blit(fuente_titulo.render("Costo", True, (255,255,255)), (635, 50))

    # Dibujar barras
    for i, alg in enumerate(algoritmos):
        pygame.draw.rect(screen, (0,140,255),
            (bases_x[0]+i*separacion, base_y-h_t[i], ancho, h_t[i]))
        pygame.draw.rect(screen, (0,255,150),
            (bases_x[1]+i*separacion, base_y-h_p[i], ancho, h_p[i]))
        pygame.draw.rect(screen, (255,160,0),
            (bases_x[2]+i*separacion, base_y-h_c[i], ancho, h_c[i]))

        txt = fuente.render(alg, True, (255,255,255))
        screen.blit(txt, (bases_x[0]+i*separacion, base_y+8))
        screen.blit(txt, (bases_x[1]+i*separacion, base_y+8))
        screen.blit(txt, (bases_x[2]+i*separacion, base_y+8))
