import pygame
import math
from utils.config import CELL_SIZE

class Car:
    """Self-driving car with animation capabilities"""

    def __init__(self, x, y, goal_x, goal_y, car_image_path):
        self.x = x
        self.y = y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.prev_x = x
        self.prev_y = y
        self.angle = 0  # Current rotation angle
        self.travel_time = 0  # Time taken to reach destination
        self.recalculations = 0  # Number of path recalculations

        # Load and scale the car image
        self.original_image = pygame.image.load(car_image_path)
        self.original_image = pygame.transform.scale(self.original_image, (CELL_SIZE, CELL_SIZE))
        self.car_image = self.original_image.copy()
        
        # For smooth animation
        self.actual_x = float(x * CELL_SIZE)
        self.actual_y = float(y * CELL_SIZE)
        self.target_x = self.actual_x
        self.target_y = self.actual_y
        self.move_speed = 5.0  # Pixels per frame for smooth movement
        self.is_moving = False
        
        self.path = []

    def move(self):
        """Move along the path"""
        if self.path and not self.is_moving:
            next_pos = self.path[0]
            self.path.pop(0)
            
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = next_pos
            
            # Set target for smooth movement
            self.target_x = float(self.x * CELL_SIZE)
            self.target_y = float(self.y * CELL_SIZE)
            self.is_moving = True
            
            # Calculate rotation angle based on movement direction
            dx = self.x - self.prev_x
            dy = self.y - self.prev_y
            
            if dx == 1 and dy == 0:  # Moving right
                self.angle = 0
            elif dx == -1 and dy == 0:  # Moving left
                self.angle = 180
            elif dx == 0 and dy == 1:  # Moving down
                self.angle = 90
            elif dx == 0 and dy == -1:  # Moving up
                self.angle = 270
            
            # Rotate the image
            self.car_image = pygame.transform.rotate(self.original_image, -self.angle)
            
            # Increment travel time
            self.travel_time += 1
    
    def update_animation(self):
        """Update the car's position for smooth animation"""
        if self.is_moving:
            # Calculate direction vector
            dx = self.target_x - self.actual_x
            dy = self.target_y - self.actual_y
            distance = max(0.1, math.sqrt(dx*dx + dy*dy))
            
            # Normalize and scale by speed
            if distance > 0:
                dx = dx / distance * min(self.move_speed, distance)
                dy = dy / distance * min(self.move_speed, distance)
            
            # Update position
            self.actual_x += dx
            self.actual_y += dy
            
            # Check if we've reached the target
            if abs(self.actual_x - self.target_x) < 1 and abs(self.actual_y - self.target_y) < 1:
                self.actual_x = self.target_x
                self.actual_y = self.target_y
                self.is_moving = False

    def draw(self, screen):
        """Draw the car image with rotation"""
        # Get the rect for the rotated image to ensure it's centered
        rect = self.car_image.get_rect(center=(self.actual_x + CELL_SIZE/2, self.actual_y + CELL_SIZE/2))
        screen.blit(self.car_image, rect)