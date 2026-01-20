# --------------------------------------------------
# Funciones encargadas de evaluar el rendimiento
# de los algoritmos de búsqueda sobre el laberinto
# --------------------------------------------------

import time


def evaluar_algoritmo(nombre, algoritmo, problem, lab):
    """
    Ejecuta un algoritmo de búsqueda y mide su desempeño.

    Parámetros:
    - nombre: nombre del algoritmo (DFS, BFS, UCS, A*)
    - algoritmo: función del algoritmo de búsqueda
    - problem: problema de búsqueda del laberinto
    - lab: objeto Labyrinth para obtener costos

    Retorna:
    - Diccionario con métricas y la ruta encontrada
    """

    # Medición del tiempo de ejecución
    inicio = time.perf_counter()
    ruta = algoritmo(problem)
    fin = time.perf_counter()

    tiempo = fin - inicio
    pasos = len(ruta)

    # Cálculo del costo total del camino
    costo = sum(lab.get_cost(state) for state in ruta)

    return {
        "algoritmo": nombre,
        "tiempo": tiempo,
        "pasos": pasos,
        "costo": costo,
        "ruta": ruta
    }


def elegir_mejor_algoritmo(resultados):
    """
    Selecciona el mejor algoritmo usando una puntuación
    normalizada basada en tiempo, pasos y costo.
    """

    # Valores máximos para normalización
    max_t = max(r["tiempo"] for r in resultados)
    max_p = max(r["pasos"] for r in resultados)
    max_c = max(r["costo"] for r in resultados)

    # Cálculo del score de cada algoritmo
    for r in resultados:
        r["score"] = (
            r["tiempo"] / max_t +
            r["pasos"] / max_p +
            r["costo"] / max_c
        )

    # Retorna el algoritmo con menor puntuación
    return min(resultados, key=lambda r: r["score"])

