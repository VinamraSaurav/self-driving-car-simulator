import pygame
from utils.config import CELL_SIZE, YELLOW

class Coin:
    """Collectible coin for player to earn points"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_counter = 0
        
    def draw(self, screen):
        """Draw coin with simple pulsing animation"""
        if not self.collected:
            self.animation_counter = (self.animation_counter + 1) % 60
            size_mod = abs(self.animation_counter - 30) / 30  # 0 to 1 to 0...
            
            coin_rect = pygame.Rect(
                self.x * CELL_SIZE + CELL_SIZE * 0.2 + (size_mod * 2),
                self.y * CELL_SIZE + CELL_SIZE * 0.2 + (size_mod * 2),
                CELL_SIZE * 0.6 - (size_mod * 4),
                CELL_SIZE * 0.6 - (size_mod * 4)
            )
            pygame.draw.ellipse(screen, YELLOW, coin_rect)
           