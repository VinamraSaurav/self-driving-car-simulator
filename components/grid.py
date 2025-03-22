import pygame
from utils.config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, WHITE, BLACK, GREEN

class Grid:
    """Grid with authentic cells and black background"""

    def __init__(self):
        self.width = GRID_WIDTH    # Store grid width
        self.height = GRID_HEIGHT  # Store grid height
        self.dynamic_obstacles = set()
        self.static_obstacles = set()

    def draw(self, screen, goal_x, goal_y):
        """Draw the grid, goal state, and obstacles"""
        screen.fill(BLACK)
    
        # Draw grid cells
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)
    
        # Draw goal state in green
        goal_rect = pygame.Rect(goal_x * CELL_SIZE, goal_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, goal_rect)
    
    def add_dynamic_obstacle(self, x, y):
        """Add dynamic obstacle to the grid"""
        self.dynamic_obstacles.add((x, y))

    def remove_dynamic_obstacle(self, x, y):
        """Remove dynamic obstacle from the grid"""
        self.dynamic_obstacles.discard((x, y))
        
    def add_static_obstacle(self, x, y):
        """Add static obstacle to the grid"""
        self.static_obstacles.add((x, y))

    def is_obstacle(self, x, y):
        """Check if cell is occupied by any obstacle"""
        return (x, y) in self.dynamic_obstacles or (x, y) in self.static_obstacles
        
    def is_occupied(self, x, y):
        """Check if cell is occupied by any obstacle (alias for is_obstacle)"""
        return self.is_obstacle(x, y)