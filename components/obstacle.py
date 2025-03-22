import random
import pygame
from utils.config import CELL_SIZE

class Obstacle:
    """Dynamic obstacle using safety-cone image"""

    def __init__(self, x, y, obstacle_image_path):
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y

        # Load and scale the obstacle image
        self.obstacle_image = pygame.image.load(obstacle_image_path)
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (CELL_SIZE, CELL_SIZE))

    def move(self, grid):
        """Move obstacle randomly and track previous position"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dx, dy = random.choice(directions)

        self.previous_x, self.previous_y = self.x, self.y

        new_x = (self.x + dx) % grid.width
        new_y = (self.y + dy) % grid.height

        if not grid.is_occupied(new_x, new_y):
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        """Draw obstacle as a safety cone image"""
        screen.blit(self.obstacle_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
