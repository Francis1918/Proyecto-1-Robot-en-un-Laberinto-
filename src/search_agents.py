from .labyrinth import Labyrinth

class LabyrinthSearchProblem:
    def __init__(self, labyrinth):
        """
        Adapta el problema del laberinto al formato de búsqueda.
        """
        self.labyrinth = labyrinth

    def get_start_state(self):
        """Retorna la posición inicial 'S'."""
        return self.labyrinth.start_pos

    def is_goal_state(self, state):
        """Verifica si el estado es la meta 'G'."""
        return self.labyrinth.is_goal(state)

    def get_successors(self, state):
        """
        Retorna una lista de sucesores.
        Cada sucesor es una tupla: (nueva_posicion, accion, costo).
        """
        successors = []
        for next_state in self.labyrinth.get_neighbors(state):
            # Calculamos el costo según el tipo de terreno (1 o 2).
            cost = self.labyrinth.get_cost(next_state)
            # En esta fase inicial, la 'acción' puede ser simplemente la coordenada
            successors.append((next_state, next_state, cost))
        return successors

class SearchAgent:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def get_plan(self, problem):
        """Utiliza el algoritmo para planificar la ruta desde S hasta G."""
        return self.algorithm(problem)