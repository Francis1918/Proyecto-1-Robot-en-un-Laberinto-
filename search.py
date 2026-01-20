from collections import deque
import heapq


def depth_first_search(problem):
    """
    Algoritmo DFS: Explora primero los nodos más profundos.
    Retorna una lista de estados (ruta).
    """
    # Usamos una pila (LIFO) para DFS
    frontier = [(problem.get_start_state(), [])]
    visited = set()

    while frontier:
        state, path = frontier.pop()

        if problem.is_goal_state(state):
            return path + [state]

        if state not in visited:
            visited.add(state)
            for next_state, action, cost in problem.get_successors(state):
                if next_state not in visited:
                    # Guardamos el camino acumulado
                    new_path = path + [state]
                    frontier.append((next_state, new_path))
    
    return [] # No se encontró ruta


def breadth_first_search(problem):
    """
    Algoritmo BFS (Breadth-First Search):
    Explora primero todos los nodos del mismo nivel antes de profundizar.
    Garantiza encontrar el camino más corto en número de pasos.
    """
    # Usamos una cola (FIFO) para BFS
    frontier = deque([(problem.get_start_state(), [])])
    visited = set()

    while frontier:
        # Extraemos el primer estado agregado (FIFO)
        state, path = frontier.popleft()

        # Verificamos si se alcanzó la meta
        if problem.is_goal_state(state):
            return path + [state]

        # Expandimos el estado si no ha sido visitado
        if state not in visited:
            visited.add(state)

            for next_state, action, cost in problem.get_successors(state):
                if next_state not in visited:
                    # Guardamos el camino acumulado
                    new_path = path + [state]
                    frontier.append((next_state, new_path))

    # No se encontró una ruta
    return []


def uniform_cost_search(problem):
    """
    Algoritmo UCS (Uniform Cost Search):
    Expande siempre el nodo con el menor costo acumulado.
    Considera el costo de los terrenos (plano = 1, empinado = 2).
    """
    # Cola de prioridad: (costo acumulado, estado, camino)
    frontier = []
    heapq.heappush(frontier, (0, problem.get_start_state(), []))

    # Diccionario para guardar el menor costo encontrado por estado
    visited = {}

    while frontier:
        cost_so_far, state, path = heapq.heappop(frontier)

        # Verificamos si se alcanzó la meta
        if problem.is_goal_state(state):
            return path + [state]

        # Expandimos si no se ha visitado o se encontró un costo menor
        if state not in visited or cost_so_far < visited[state]:
            visited[state] = cost_so_far

            for next_state, action, cost in problem.get_successors(state):
                new_cost = cost_so_far + cost
                new_path = path + [state]
                heapq.heappush(frontier, (new_cost, next_state, new_path))

    # No se encontró una ruta
    return []

def manhattan(a, b):
    """
    Heurística Manhattan:
    Estima la distancia entre dos puntos en una grilla.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(problem):
    """
    Algoritmo A*:
    Combina UCS con una heurística (distancia Manhattan)
    para guiar la búsqueda de forma más eficiente.
    """
    start = problem.get_start_state()

    # Cola de prioridad: (prioridad, estado, camino, costo acumulado)
    frontier = []
    heapq.heappush(frontier, (0, start, [], 0))

    visited = {}

    while frontier:
        priority, state, path, cost_so_far = heapq.heappop(frontier)

        # Verificamos si se alcanzó la meta
        if problem.is_goal_state(state):
            return path + [state]

        # Expandimos el estado si es más barato que antes
        if state not in visited or cost_so_far < visited[state]:
            visited[state] = cost_so_far

            for next_state, action, cost in problem.get_successors(state):
                new_cost = cost_so_far + cost
                heuristic = manhattan(next_state, problem.labyrinth.goal_pos)
                new_priority = new_cost + heuristic
                new_path = path + [state]

                heapq.heappush(
                    frontier,
                    (new_priority, next_state, new_path, new_cost)
                )

    # No se encontró una ruta
    return []
