# Proyecto 1: Robot en un Laberinto

**Escuela Politécnica Nacional**  
**Grupo 2**

## Integrantes
- Ismael Freire
- Francis Bravo
- Joel Tinitana
- Daniel Menendez

## Descripción
Aplicación interactiva que simula un robot navegando a través de laberintos utilizando diferentes algoritmos de búsqueda de Inteligencia Artificial.

## Algoritmos Implementados
- **DFS** (Depth-First Search)
- **BFS** (Breadth-First Search)  
- **UCS** (Uniform Cost Search)
- **A*** (A-Star con heurística Manhattan)

## Estructura del Proyecto
```
├── main.py                 # Punto de entrada
├── src/                    # Lógica del laberinto y búsqueda
│   ├── labyrinth.py
│   ├── search.py
│   └── search_agents.py
├── gui/                    # Interfaz gráfica
│   ├── ui.py
│   ├── graphics.py
│   └── charts.py
├── utils/                  # Utilidades
│   └── evaluacion.py
├── assets/                 # Recursos gráficos
│   ├── logo_epn.png
│   └── robot.png
└── data/mazes/             # Laberintos
    ├── Facil_1.txt
    ├── Medio_1.txt
    ├── Dificil_1.txt
    └── Dificil_2.txt
```
