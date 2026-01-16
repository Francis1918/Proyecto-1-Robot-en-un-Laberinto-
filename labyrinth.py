class Labyrinth:
    def __init__(self, filename):
        """
        Carga el mapa del laberinto desde un archivo de texto.
        """
        self.grid = []
        self.start_pos = None
        self.goal_pos = None
        
        with open(filename, 'r') as f:
            for r, line in enumerate(f):
                row = list(line.strip())
                self.grid.append(row)
                for c, char in enumerate(row):
                    if char == 'S':
                        self.start_pos = (r, c) # Posición inicial 
                    elif char == 'G':
                        self.goal_pos = (r, c) # Posición meta 

        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0

    def is_wall(self, state):
        """
        Verifica si una posición es un obstáculo[cite: 26, 46].
        """
        r, c = state
        return self.grid[r][c] == '#'

    def is_goal(self, state):
        """
        Verifica si se ha alcanzado la meta.
        """
        return state == self.goal_pos

    def get_cost(self, state):
        """
        Define el costo de cada celda según el tipo de terreno[cite: 21].
        Terreno plano (.) = 1, Terreno empinado (2) = 2.
        """
        r, c = state
        char = self.grid[r][c]
        if char == '2':
            return 2
        return 1

    def get_neighbors(self, state):
        """
        Retorna los movimientos válidos (acciones) desde la posición actual.
        """
        r, c = state
        neighbors = []
        # Acciones posibles: Arriba, Abajo, Izquierda, Derecha
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if not self.is_wall((nr, nc)):
                    neighbors.append((nr, nc))
        return neighbors