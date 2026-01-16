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