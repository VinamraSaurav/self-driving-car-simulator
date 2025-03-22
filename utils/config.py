# Grid size
GRID_WIDTH = 20      # Number of cells horizontally
GRID_HEIGHT = 15     # Number of cells vertically
CELL_SIZE = 40       # Size of each cell in pixels

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
GREY = (150, 150, 150)
DARK_GREY = (80, 80, 80)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Animation and timing
FPS = 60          # Frames per second
ANIMATION_SPEED = 5  # Pixels per frame for smooth car movement

# Car settings
CAR_SPEED = 2     # Speed factor for the car

# Simulation settings
OBSTACLE_MOVE_INTERVAL = 90  # Frames between obstacle movements
PATH_RECALC_INTERVAL = 60    # Frames between path recalculations
TRAFFIC_DENSITY = 5          # Number of AI-controlled cars

# Game modes
MODE_SIMULATION = 0
MODE_RACE = 1
MODE_COLLECT = 2
MODE_MANUAL = 3

# Point system
POINTS_GOAL_REACHED = 100
POINTS_COIN_COLLECTED = 25
POINTS_OBSTACLE_AVOIDED = 5
POINTS_COLLISION = -50