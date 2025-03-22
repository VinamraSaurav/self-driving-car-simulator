import pygame
import random
from components.coin import Coin
from components.pathfinding import a_star
from utils.config import CELL_SIZE, POINTS_COIN_COLLECTED, POINTS_GOAL_REACHED, MODE_SIMULATION, MODE_COLLECT, MODE_MANUAL, MODE_RACE
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d

class GameController:
    """Controls game modes and scoring for human-playable games"""
    
    def __init__(self, grid, player_car, metrics_panel):
        self.grid = grid
        self.player_car = player_car
        self.metrics_panel = metrics_panel
        
        # Game state
        self.mode = MODE_SIMULATION
        self.score = 0
        self.time_remaining = 60 * 60  # 60 seconds at 60 FPS
        self.level = 1
        
        # Collectibles
        self.coins = []
        
        # Manual control variables
        self.manual_control = False
        self.manual_move_cooldown = 0
        
        # Add score tracking to metrics panel
        self.metrics_panel.metrics["score"] = 0
        self.metrics_panel.metrics["time"] = 60
        self.metrics_panel.metrics["level"] = 1
        
    def update(self, keys_pressed):
        """Update game state based on current mode"""
        # Update timer
        if self.mode != MODE_SIMULATION:
            self.time_remaining -= 1
            self.metrics_panel.metrics["time"] = self.time_remaining // 60
            
            # End game if time runs out
            if self.time_remaining <= 0:
                self.game_over()
        
        # Handle different game modes
        if self.mode == MODE_MANUAL:
            self.handle_manual_control(keys_pressed)
        elif self.mode == MODE_RACE:
            self.check_goal_reached()
        elif self.mode == MODE_COLLECT:
            self.check_coin_collection()
            
        # Update metrics
        self.metrics_panel.metrics["score"] = self.score
        self.metrics_panel.metrics["level"] = self.level
        
    def switch_mode(self, mode):
        """Switch to a different game mode"""
        self.mode = mode
        self.metrics_panel.set_mode(mode)

        # Reset game state
        self.score = 0
        self.time_remaining = 60 * 60
        self.level = 1

        # Update metrics
        self.metrics_panel.metrics["score"] = 0
        self.metrics_panel.metrics["level"] = 1
        self.metrics_panel.metrics["time"] = 60

        if mode == MODE_SIMULATION:
            # Clear player car path
            self.player_car.path = []
            self.manual_control = False

        elif mode == MODE_RACE:
            self.setup_race_mode()

        elif mode == MODE_COLLECT:
            self.setup_collect_mode()

        elif mode == MODE_MANUAL:
            self.setup_manual_mode()


    def setup_race_mode(self):
        """Setup for race mode"""
        # Place car at start position
        self.player_car.x = 2
        self.player_car.y = 2
        self.player_car.actual_x = 2 * CELL_SIZE
        self.player_car.actual_y = 2 * CELL_SIZE
        
        # Set random goal position
        goal_x, goal_y = self.get_random_goal()
        self.player_car.goal_x = goal_x
        self.player_car.goal_y = goal_y
        
        # Calculate path
        self.player_car.path = a_star(self.grid, (self.player_car.x, self.player_car.y),
                                     (self.player_car.goal_x, self.player_car.goal_y)) or []
        
        # Make sure path is not empty
        if not self.player_car.path:
            # Try again with a different goal
            self.setup_race_mode()
    


    def setup_collect_mode(self):
        """Setup for collection mode"""
        # Clear existing coins
        self.coins = []
        
        # Spawn coins
        self.spawn_coins(10)
        
        # Set player car to manual control
        self.player_car.path = []
        
    def setup_manual_mode(self):
        """Setup for manual control mode"""
        # Clear path and set manual control
        self.player_car.path = []
        self.manual_control = True
        
    

    def handle_manual_control(self, keys_pressed):
        """Handle manual control with keyboard"""
        if self.manual_move_cooldown > 0:
            self.manual_move_cooldown -= 1
            return

        if self.player_car.is_moving:
            return

        x, y = self.player_car.x, self.player_car.y
        new_x, new_y = x, y

        if keys_pressed[K_UP] or keys_pressed[K_w]:
            new_y = y - 1
            self.player_car.angle = 270
        elif keys_pressed[K_DOWN] or keys_pressed[K_s]:
            new_y = y + 1
            self.player_car.angle = 90
        elif keys_pressed[K_LEFT] or keys_pressed[K_a]:
            new_x = x - 1
            self.player_car.angle = 180
        elif keys_pressed[K_RIGHT] or keys_pressed[K_d]:
            new_x = x + 1
            self.player_car.angle = 0

        if new_x != x or new_y != y:
            if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
                if not self.grid.is_occupied(new_x, new_y):
                    self.player_car.prev_x, self.player_car.prev_y = x, y
                    self.player_car.x, self.player_car.y = new_x, new_y
                    self.player_car.target_x = new_x * CELL_SIZE
                    self.player_car.target_y = new_y * CELL_SIZE
                    self.player_car.is_moving = True

                    self.player_car.car_image = pygame.transform.rotate(
                        self.player_car.original_image, -self.player_car.angle)

                    self.manual_move_cooldown = 5

                    # Clear the path to prevent automatic movement
                    self.player_car.path = []

                    if self.mode == MODE_COLLECT:
                        self.check_coin_collection()


    def spawn_coins(self, num_coins):
        """Spawn coins using rupee.png in random unoccupied positions"""
        for _ in range(num_coins):
            while True:
                x = random.randint(0, self.grid.width - 1)
                y = random.randint(0, self.grid.height - 1)
                
                if not self.grid.is_occupied(x, y):
                    coin = Coin(x, y, image_path='assets/rupee.png')
                    self.coins.append(coin)
                    break
                        
    def check_coin_collection(self):
        """Check if player has collected any coins"""
        player_pos = (self.player_car.x, self.player_car.y)

        for coin in self.coins:
            if not coin.collected and (coin.x, coin.y) == player_pos:
                coin.collected = True
                self.score += POINTS_COIN_COLLECTED
                # Update metrics immediately
                self.metrics_panel.metrics["score"] = self.score

        # Check if all coins are collected
        if all(coin.collected for coin in self.coins):
            self.level += 1
            self.time_remaining += 30 * 60  # Add 30 seconds
            self.metrics_panel.metrics["level"] = self.level
            self.metrics_panel.metrics["time"] = self.time_remaining // 60
            self.spawn_coins(10 + self.level * 2)

    def check_goal_reached(self):
        """Check if player has reached the goal in race mode"""
        if (self.player_car.x, self.player_car.y) == (self.player_car.goal_x, self.player_car.goal_y):
            self.score += POINTS_GOAL_REACHED
            self.level += 1
            self.time_remaining += 30 * 60

            goal_x, goal_y = self.get_random_goal()
            self.player_car.goal_x = goal_x
            self.player_car.goal_y = goal_y

            self.player_car.path = a_star(self.grid, (self.player_car.x, self.player_car.y),
                                         (self.player_car.goal_x, self.player_car.goal_y)) or []

    def get_random_goal(self):
        """Get a random goal position"""
        while True:
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            
            if not self.grid.is_occupied(x, y):
                return x, y
    

    def game_over(self):
        """Handle game over state"""
        # Display game over message
        self.score = 0
        self.time_remaining = 60 * 60  # Reset timer
        self.level = 1
        
        # Switch back to simulation mode
        self.switch_mode(MODE_SIMULATION)

                
    def draw(self, screen):
        """Draw coins in collection mode"""
        if self.mode == MODE_COLLECT:
            for coin in self.coins:
                if not coin.collected:
                    coin.draw(screen)

