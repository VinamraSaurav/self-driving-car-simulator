import pygame
import random
from utils.config import CELL_SIZE

class StaticObstacle:
    """Static obstacles like trees, buildings, etc."""

    def __init__(self, x, y, obstacle_type=None):
        self.x = x
        self.y = y
        
        # Available obstacle types and their image paths
        self.obstacle_types = {
            'tree': 'assets/tree.png',
            'palm-tree': 'assets/palm-tree.png',
            'pine-tree': 'assets/pine-tree.png',
            'mansion': 'assets/mansion.png',
            'pedestrians': 'assets/pedestrians.png'
        }
        
        # Select random obstacle type if none specified
        if obstacle_type is None:
            obstacle_type = random.choice(list(self.obstacle_types.keys()))
        
        # Ensure the obstacle type is valid
        if obstacle_type not in self.obstacle_types:
            obstacle_type = 'tree'  # Default to tree
            
        self.obstacle_type = obstacle_type
        self.image_path = self.obstacle_types[obstacle_type]
        
        # Load and scale the obstacle image
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
    
    def draw(self, screen):
        """Draw the static obstacle"""
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))