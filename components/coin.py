import pygame
from utils.config import CELL_SIZE

class Coin:
    """Collectible coin for player to earn points"""
    
    def __init__(self, x, y, image_path='assets/rupee.png'):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_counter = 0

        # Load coin image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        """Draw coin using rupee.png image with animation"""
        if not self.collected:
            # Add simple pulsing animation effect
            self.animation_counter = (self.animation_counter + 1) % 60
            size_mod = abs(self.animation_counter - 30) / 30

            scaled_size = CELL_SIZE * (0.8 + size_mod * 0.2)
            scaled_image = pygame.transform.scale(self.image, (int(scaled_size), int(scaled_size)))

            screen.blit(scaled_image, (
                self.x * CELL_SIZE + (CELL_SIZE - scaled_size) / 2,
                self.y * CELL_SIZE + (CELL_SIZE - scaled_size) / 2
            ))
