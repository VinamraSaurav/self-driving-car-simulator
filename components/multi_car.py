import pygame
import random
from components.car import Car
from components.pathfinding import a_star, manhattan_distance
from utils.config import GRID_WIDTH, GRID_HEIGHT

class MultiCar:
    """Class for handling multiple cars and traffic simulation"""
    
    def __init__(self, grid, num_cars, car_image_path):
        self.grid = grid
        self.cars = []
        self.car_image_path = car_image_path
        
        # Generate random start and goal positions for each car
        for _ in range(num_cars):
            # Try to find unoccupied positions
            start_pos = self._get_random_unoccupied_position()
            goal_pos = self._get_random_unoccupied_position()
            
            # Ensure start and goal are different positions
            while manhattan_distance(start_pos, goal_pos) < 5:
                goal_pos = self._get_random_unoccupied_position()
            
            # Create and add the car
            car = Car(start_pos[0], start_pos[1], goal_pos[0], goal_pos[1], car_image_path)
            self.cars.append(car)
            
            # Calculate initial path
            car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
    
    def _get_random_unoccupied_position(self):
        """Find a random unoccupied position on the grid"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if not self.grid.is_occupied(x, y):
                return (x, y)
    
    

    def draw(self, screen):
        """Draw all cars"""
        for car in self.cars:
            car.draw(screen)

    def update(self):
        """Update all cars, recalculate paths if necessary"""
        car_positions = {(car.x, car.y) for car in self.cars}
    
        for car in self.cars:
        # Check if car has reached its goal
            if (car.x, car.y) == (car.goal_x, car.goal_y):
            # Set new random goal
                new_goal = self._get_random_unoccupied_position()
                car.goal_x, car.goal_y = new_goal
                car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
                continue
            
        # Move the car if it has a path
            if car.path:
            # Check next position for collision with other cars
                next_pos = car.path[0] if car.path else (car.x, car.y)
            
            # If next position is occupied by another car, recalculate path
                if next_pos in car_positions and next_pos != (car.x, car.y):
                # Try to find an alternative path by temporarily marking the blocked position as an obstacle
                    self.grid.add_dynamic_obstacle(next_pos[0], next_pos[1])
                    car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
                    self.grid.remove_dynamic_obstacle(next_pos[0], next_pos[1])
                    car.recalculations += 1
                else:
                # Safe to move
                    car_positions.remove((car.x, car.y))
                    car.move()
                    car_positions.add((car.x, car.y))
            else:
            # No path exists, try to recalculate
                car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
                car.recalculations += 1