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

# Function to place static obstacles without blocking critical paths
def place_static_obstacles():
    global static_obstacles
    static_obstacles = []
    
    # Clear all static obstacles from grid
    grid.static_obstacles.clear()
    
    # Important positions to avoid (player start/goal)
    important_positions = {
        (start_x, start_y), 
        (goal_x, goal_y),
        (start_x+1, start_y), (start_x-1, start_y),
        (start_x, start_y+1), (start_x, start_y-1),
        (goal_x+1, goal_y), (goal_x-1, goal_y),
        (goal_x, goal_y+1), (goal_x, goal_y-1)
    }
    
    for _ in range(num_static_obstacles):
        attempts = 0
        while attempts < 20:  # Limit attempts to prevent infinite loop
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Skip if position is important or already occupied
            if (x, y) in important_positions or grid.is_occupied(x, y):
                attempts += 1
                continue
                
            # Create and place the obstacle
            obstacle = StaticObstacle(x, y)
            static_obstacles.append(obstacle)
            grid.add_static_obstacle(x, y)
            break

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

# Add dynamic obstacles to grid
for obstacle in dynamic_obstacles:
    grid.add_dynamic_obstacle(obstacle.x, obstacle.y)

# Create traffic cars
traffic = MultiCar(grid, 5, TRAFFIC_CAR_IMAGE)

# Create traffic manager
traffic_manager = TrafficManager(grid, player_car, traffic, dynamic_obstacles)

# Create metrics panel
metrics_panel = MetricsPanel(PANEL_WIDTH)

# Simulation loop
clock = pygame.time.Clock()
running = True
paused = False

# Timers for delays
obstacle_timer = 0
path_timer = 0
OBSTACLE_MOVE_INTERVAL = 90
PATH_RECALC_INTERVAL = 60

# Draw path function
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
            elif event.key == pygame.K_p:  # Pause/Resume
                paused = not paused
            elif event.key == pygame.K_r:  # Reset
                # Reset player car
                player_car = Car(start_x, start_y, goal_x, goal_y, PLAYER_CAR_IMAGE)
                player_car.path = a_star(grid, (start_x, start_y), (goal_x, goal_y)) or []
                
                # Reset traffic
                traffic = MultiCar(grid, 5, TRAFFIC_CAR_IMAGE)
                
                # Reset traffic manager
                traffic_manager = TrafficManager(grid, player_car, traffic, dynamic_obstacles)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is within the grid (not on panel)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < GRID_WIDTH * CELL_SIZE:
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                
                # Toggle obstacle at click location
                if grid.is_obstacle(grid_x, grid_y):
                    grid.remove_dynamic_obstacle(grid_x, grid_y)
                    grid.remove_static_obstacle(grid_x, grid_y)
                    
                    # Remove from obstacle lists if present
                    for obs in dynamic_obstacles[:]:
                        if obs.x == grid_x and obs.y == grid_y:
                            dynamic_obstacles.remove(obs)
                            
                    for obs in static_obstacles[:]:
                        if obs.x == grid_x and obs.y == grid_y:
                            static_obstacles.remove(obs)
                else:
                    # Add new obstacle at click location
                    new_obs = StaticObstacle(grid_x, grid_y)
                    static_obstacles.append(new_obs)
                    grid.add_static_obstacle(grid_x, grid_y)
                
                # Recalculate paths after obstacle change
                player_car.path = a_star(grid, (player_car.x, player_car.y), 
                                        (player_car.goal_x, player_car.goal_y)) or []
                player_car.recalculations += 1

    if not paused:
        # Handle obstacle movement delay
        obstacle_timer += 1
        if obstacle_timer >= OBSTACLE_MOVE_INTERVAL:
            for obstacle in dynamic_obstacles:
                grid.remove_dynamic_obstacle(obstacle.x, obstacle.y)
                obstacle.move(grid)
                grid.add_dynamic_obstacle(obstacle.x, obstacle.y)
            obstacle_timer = 0

        # Handle path recalculation delay
        path_timer += 1
        if path_timer >= PATH_RECALC_INTERVAL:
            if not player_car.path:
                player_car.path = a_star(grid, (player_car.x, player_car.y), 
                                        (player_car.goal_x, player_car.goal_y)) or []
                player_car.recalculations += 1
            path_timer = 0

        # Update traffic manager
        traffic_manager.update()
        
        # Check for collisions
        has_collision = traffic_manager.check_collisions()
        
        # Update player car animation
        player_car.update_animation()
        
        # Move player car if animation complete
        if not player_car.is_moving:
            player_car.move()
            
        # Update traffic cars
        traffic.update()
        for car in traffic.cars:
            car.update_animation()

    # Draw everything
    grid.draw(screen, goal_x, goal_y)

    # Draw static obstacles
    for obstacle in static_obstacles:
        obstacle.draw(screen)

    # Draw dynamic obstacles
    for obstacle in dynamic_obstacles:
        obstacle.draw(screen)

    # Draw the path for player car
    if player_car.path:
        draw_path(screen, player_car.path)

    # Draw traffic cars
    traffic.draw(screen)
    
    # Draw player car (on top)
    player_car.draw(screen)
    
    # Update and draw metrics panel
    metrics_panel.update_metrics(player_car, traffic_manager, int(current_fps))
    metrics_panel.draw(screen)
    
    # Display pause indicator if paused
    if paused:
        font = pygame.font.SysFont('Arial', 36, bold=True)
        pause_text = font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2))
        screen.blit(pause_text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()