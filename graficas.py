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

    screen.fill((30, 30, 40))
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente = pygame.font.SysFont("Arial", 18)
    fuente_valor = pygame.font.SysFont("Arial", 14)
    fuente_eje = pygame.font.SysFont("Arial", 12)

    algoritmos = [r["algoritmo"] for r in resultados]
    tiempos = [r["tiempo"] for r in resultados]
    pasos = [r["pasos"] for r in resultados]
    costos = [r["costo"] for r in resultados]

    # Configuración de las gráficas
    altura_max = 280
    base_y = 420
    ancho_barra = 40
    separacion = 55
    
    # Posiciones X para cada gráfica (centradas)
    graficas = [
        {"titulo": "Tiempo (s)", "valores": tiempos, "color": (66, 165, 245), "base_x": 50, "formato": "{:.4f}"},
        {"titulo": "Pasos", "valores": pasos, "color": (102, 187, 106), "base_x": 300, "formato": "{}"},
        {"titulo": "Costo", "valores": costos, "color": (255, 167, 38), "base_x": 550, "formato": "{}"},
    ]

    for grafica in graficas:
        valores = grafica["valores"]
        color = grafica["color"]
        base_x = grafica["base_x"]
        titulo = grafica["titulo"]
        formato = grafica["formato"]
        
        # Valor máximo para normalización
        max_val = max(valores) if max(valores) > 0 else 1
        
        # Calcular ancho total del grupo de barras
        ancho_grupo = len(algoritmos) * separacion
        
        # Dibujar título centrado
        txt_titulo = fuente_titulo.render(titulo, True, (255, 255, 255))
        titulo_x = base_x + (ancho_grupo - txt_titulo.get_width()) // 2
        screen.blit(txt_titulo, (titulo_x, 30))
        
        # Dibujar eje Y (línea vertical)
        eje_x = base_x - 15
        pygame.draw.line(screen, (150, 150, 150), (eje_x, base_y), (eje_x, base_y - altura_max - 20), 2)
        
        # Dibujar marcas y valores en eje Y (5 niveles)
        for i in range(6):
            y_pos = base_y - int((i / 5) * altura_max)
            valor_eje = (i / 5) * max_val
            
            # Línea de marca
            pygame.draw.line(screen, (100, 100, 100), (eje_x - 5, y_pos), (base_x + ancho_grupo, y_pos), 1)
            
            # Valor del eje
            if formato == "{:.4f}":
                txt_eje = fuente_eje.render(f"{valor_eje:.3f}", True, (180, 180, 180))
            else:
                txt_eje = fuente_eje.render(f"{int(valor_eje)}", True, (180, 180, 180))
            screen.blit(txt_eje, (eje_x - txt_eje.get_width() - 8, y_pos - 6))
        
        # Dibujar eje X (línea horizontal)
        pygame.draw.line(screen, (150, 150, 150), (eje_x, base_y), (base_x + ancho_grupo + 10, base_y), 2)
        
        # Dibujar barras con degradado y valores
        for i, (alg, val) in enumerate(zip(algoritmos, valores)):
            # Altura proporcional
            altura = int((val / max_val) * altura_max) if max_val > 0 else 0
            x = base_x + i * separacion
            y = base_y - altura
            
            # Barra con borde redondeado (simulado con rectángulo + pequeños rect)
            rect = pygame.Rect(x, y, ancho_barra, altura)
            
            # Color base y highlight
            color_claro = tuple(min(c + 40, 255) for c in color)
            
            # Dibujar barra principal
            pygame.draw.rect(screen, color, rect)
            
            # Efecto de brillo en el lado izquierdo
            pygame.draw.rect(screen, color_claro, (x, y, 8, altura))
            
            # Borde superior redondeado (pequeño rectángulo)
            pygame.draw.rect(screen, color_claro, (x, y, ancho_barra, 3))
            
            # Valor encima de la barra
            if formato == "{:.4f}":
                txt_valor = fuente_valor.render(f"{val:.4f}", True, (255, 255, 255))
            else:
                txt_valor = fuente_valor.render(f"{val}", True, (255, 255, 255))
            
            valor_x = x + (ancho_barra - txt_valor.get_width()) // 2
            screen.blit(txt_valor, (valor_x, y - 18))
            
            # Nombre del algoritmo debajo
            txt_alg = fuente.render(alg, True, (220, 220, 220))
            alg_x = x + (ancho_barra - txt_alg.get_width()) // 2
            screen.blit(txt_alg, (alg_x, base_y + 10))

    # Leyenda al pie
    leyenda_y = 480
    fuente_leyenda = pygame.font.SysFont("Arial", 14)
    txt_leyenda = fuente_leyenda.render("* Valores más bajos indican mejor rendimiento", True, (140, 140, 140))
    screen.blit(txt_leyenda, (screen.get_width() // 2 - txt_leyenda.get_width() // 2, leyenda_y))
