import pygame
import random
import sys
from components.grid import Grid
from components.car import Car
from components.obstacle import Obstacle
from components.static_obstacle import StaticObstacle
from components.multi_car import MultiCar
from components.traffic_manager import TrafficManager
from components.metrics_panel import MetricsPanel
from components.pathfinding import a_star
from utils.config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, FPS, GREY, WHITE
from components.game_controller import GameController
from utils.config import MODE_COLLECT, MODE_MANUAL, MODE_RACE, MODE_SIMULATION

# Pygame initialization
pygame.init()

# Panel width for metrics display
PANEL_WIDTH = 250

# Screen setup with side panel
screen = pygame.display.set_mode(
    (GRID_WIDTH * CELL_SIZE + PANEL_WIDTH, GRID_HEIGHT * CELL_SIZE)
)
pygame.display.set_caption("Advanced Self-Driving Car Simulator")

# File paths
PLAYER_CAR_IMAGE = "assets/sport-car.png"
TRAFFIC_CAR_IMAGE = "assets/racing-car.png"
OBSTACLE_IMAGE = "assets/safety-cone.png"
COIN_IMAGE = "assets/rupee.png"

# Grid initialization
grid = Grid()

# Car's start and goal positions
start_x, start_y = 2, 2
goal_x, goal_y = GRID_WIDTH - 3, GRID_HEIGHT - 3

# Load player car
player_car = Car(start_x, start_y, goal_x, goal_y, PLAYER_CAR_IMAGE)

# Create static obstacles (trees, buildings)
num_static_obstacles = 15
static_obstacles = []

def place_static_obstacles():
    """Place static obstacles while avoiding blocking critical paths"""
    global static_obstacles
    static_obstacles = []
    grid.static_obstacles.clear()
    
    important_positions = {
        (start_x, start_y), 
        (goal_x, goal_y)
    }
    
    for _ in range(num_static_obstacles):
        attempts = 0
        while attempts < 20:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if (x, y) not in important_positions and not grid.is_occupied(x, y):
                obstacle = StaticObstacle(x, y)
                static_obstacles.append(obstacle)
                grid.add_static_obstacle(x, y)
                break
            attempts += 1

# Place initial static obstacles
place_static_obstacles()

# Dynamic obstacles
num_dynamic_obstacles = 8
dynamic_obstacles = [
    Obstacle(
        random.randint(0, GRID_WIDTH - 1),
        random.randint(0, GRID_HEIGHT - 1),
        OBSTACLE_IMAGE
    ) for _ in range(num_dynamic_obstacles)
]

for obstacle in dynamic_obstacles:
    grid.add_dynamic_obstacle(obstacle.x, obstacle.y)

# Create traffic cars
traffic_cars = MultiCar(grid, 5, TRAFFIC_CAR_IMAGE)

# Create traffic manager
traffic_manager = TrafficManager(grid, player_car, traffic_cars, dynamic_obstacles)

# Create metrics panel
metrics_panel = MetricsPanel(PANEL_WIDTH)

# Create game controller
game_controller = GameController(grid, player_car, metrics_panel)

# Simulation loop
clock = pygame.time.Clock()
running = True
paused = False

# Timers
obstacle_timer = 0
path_timer = 0
OBSTACLE_MOVE_INTERVAL = 90
PATH_RECALC_INTERVAL = 60

def draw_path(screen, path):
    """Draw the path in grey"""
    for x, y in path:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREY, rect)

# Main game loop
while running:
    current_fps = clock.get_fps()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                game_controller.switch_mode(MODE_SIMULATION)
                paused = False
            elif event.key == pygame.K_2:
                game_controller.switch_mode(MODE_RACE)
                paused = False
            elif event.key == pygame.K_3:
                game_controller.switch_mode(MODE_COLLECT)
                paused = False
            elif event.key == pygame.K_4:
                game_controller.switch_mode(MODE_MANUAL)
                paused = False
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r:
                player_car = Car(start_x, start_y, goal_x, goal_y, PLAYER_CAR_IMAGE)
                player_car.path = a_star(grid, (start_x, start_y), (goal_x, goal_y)) or []
                traffic_cars = MultiCar(grid, 5, TRAFFIC_CAR_IMAGE)
                traffic_manager = TrafficManager(grid, player_car, traffic_cars, dynamic_obstacles)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < GRID_WIDTH * CELL_SIZE:
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                
                if grid.is_obstacle(grid_x, grid_y):
                    grid.remove_dynamic_obstacle(grid_x, grid_y)
                    grid.remove_static_obstacle(grid_x, grid_y)
                else:
                    new_obs = StaticObstacle(grid_x, grid_y)
                    static_obstacles.append(new_obs)
                    grid.add_static_obstacle(grid_x, grid_y)
                
                player_car.path = a_star(grid, (player_car.x, player_car.y), 
                                        (player_car.goal_x, player_car.goal_y)) or []
                player_car.recalculations += 1

    keys_pressed = pygame.key.get_pressed()
    game_controller.update(keys_pressed)

    if not paused:
        obstacle_timer += 1
        if obstacle_timer >= OBSTACLE_MOVE_INTERVAL:
            for obstacle in dynamic_obstacles:
                grid.remove_dynamic_obstacle(obstacle.x, obstacle.y)
                obstacle.move(grid)
                grid.add_dynamic_obstacle(obstacle.x, obstacle.y)
            obstacle_timer = 0

        path_timer += 1
        if path_timer >= PATH_RECALC_INTERVAL:
            if not player_car.path:
                player_car.path = a_star(grid, (player_car.x, player_car.y), 
                                        (player_car.goal_x, player_car.goal_y)) or []
                player_car.recalculations += 1
            path_timer = 0

        traffic_manager.update()
        has_collision = traffic_manager.check_collisions()
        player_car.update_animation()

        if not player_car.is_moving:
            player_car.move()

        traffic_cars.update()
        for car in traffic_cars.cars:
            car.update_animation()

    # Draw everything
    grid.draw(screen, player_car.goal_x, player_car.goal_y)


    for obstacle in static_obstacles:
        obstacle.draw(screen)

    for obstacle in dynamic_obstacles:
        obstacle.draw(screen)

    if player_car.path:
        draw_path(screen, player_car.path)

    traffic_cars.draw(screen)
    player_car.draw(screen)
    metrics_panel.update_metrics(player_car, traffic_manager, int(current_fps))
    metrics_panel.draw(screen)
    game_controller.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
