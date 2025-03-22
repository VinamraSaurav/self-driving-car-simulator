import pygame
from utils.config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, WHITE, BLACK
from utils.config import MODE_SIMULATION, MODE_RACE, MODE_COLLECT, MODE_MANUAL, YELLOW

# In metrics_panel.py

class MetricsPanel:
    """Side panel to display simulation metrics and controls"""
    
    def __init__(self, panel_width=200):
        self.panel_width = panel_width
        self.panel_height = GRID_HEIGHT * CELL_SIZE
        self.panel_x = GRID_WIDTH * CELL_SIZE
        self.font = pygame.font.SysFont('Arial', 16)
        self.title_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # Metrics to track
        self.metrics = {
            "player_travel_time": 0,
            "player_recalculations": 0,
            "traffic_recalculations": 0,
            "collisions": 0,
            "fps": 0,
            
            # Game metrics
            "score": 0,
            "level": 1,
            "time": 60
        }
        
        # Current game mode
        self.current_mode = MODE_SIMULATION
        
    def update_metrics(self, player_car, traffic_manager, fps):
        """Update the metrics with current values"""
        self.metrics["player_travel_time"] = player_car.travel_time
        self.metrics["player_recalculations"] = player_car.recalculations
        
        if traffic_manager:
            tm_metrics = traffic_manager.get_metrics()
            self.metrics["collisions"] = tm_metrics["collisions"]
            self.metrics["traffic_recalculations"] = tm_metrics["recalculations"]
        
        self.metrics["fps"] = fps
    
    def draw(self, screen):
        """Draw the metrics panel"""
        # Create panel background
        panel_rect = pygame.Rect(self.panel_x, 0, self.panel_width, self.panel_height)
        pygame.draw.rect(screen, BLACK, panel_rect)
        pygame.draw.rect(screen, WHITE, panel_rect, 2)
        
        # Determine which metrics to show based on game mode
        if self.current_mode == MODE_SIMULATION:
            # Draw simulation metrics title
            title = self.title_font.render("SIMULATION METRICS", True, WHITE)
            screen.blit(title, (self.panel_x + 10, 20))
            
            # Draw simulation metrics
            y_pos = 60
            for key, value in self.metrics.items():
                # Skip game metrics
                if key in ["score", "level", "time"]:
                    continue
                    
                # Format the key name for display
                display_name = key.replace('_', ' ').title()
                
                # Render the metric
                text = self.font.render(f"{display_name}: {value}", True, WHITE)
                screen.blit(text, (self.panel_x + 15, y_pos))
                y_pos += 30
        else:
            # Draw game metrics title
            title = self.title_font.render("GAME METRICS", True, WHITE)
            screen.blit(title, (self.panel_x + 10, 20))
            
            # Draw score
            score_text = self.title_font.render(f"Score: {self.metrics['score']}", True, WHITE)
            screen.blit(score_text, (self.panel_x + 15, 60))
            
            # Draw level
            level_text = self.font.render(f"Level: {self.metrics['level']}", True, WHITE)
            screen.blit(level_text, (self.panel_x + 15, 95))
            
            # Draw time
            time_text = self.font.render(f"Time: {self.metrics['time']}s", True, WHITE)
            screen.blit(time_text, (self.panel_x + 15, 125))
            
            # Draw FPS
            fps_text = self.font.render(f"FPS: {self.metrics['fps']}", True, WHITE)
            screen.blit(fps_text, (self.panel_x + 15, 155))
        
        # Draw divider line
        y_pos = 200 if self.current_mode != MODE_SIMULATION else 260
        pygame.draw.line(screen, WHITE, 
                         (self.panel_x + 10, y_pos), 
                         (self.panel_x + self.panel_width - 10, y_pos), 2)
        
        # Draw game modes section
        modes_title = self.title_font.render("GAME MODES", True, WHITE)
        screen.blit(modes_title, (self.panel_x + 10, y_pos + 20))
        
        # Draw mode options
        mode_texts = [
            "1: Simulation Mode",
            "2: Race Mode",
            "3: Collection Mode",
            "4: Manual Control"
        ]
        
        y_pos += 60
        for i, text in enumerate(mode_texts):
            # Highlight current mode
            color = YELLOW if self.current_mode == i else WHITE
            rendered_text = self.font.render(text, True, color)
            screen.blit(rendered_text, (self.panel_x + 15, y_pos))
            y_pos += 25
        
        # Draw controls section
        controls_title = self.title_font.render("CONTROLS", True, WHITE)
        screen.blit(controls_title, (self.panel_x + 10, y_pos + 20))
        
        # Draw control instructions
        control_texts = [
            "Click: Add/Remove Obstacle",
            "R: Reset Simulation",
            "P: Pause/Resume",
            "WASD/Arrows: Manual Drive",
            "ESC: Quit"
        ]
        
        y_pos += 60
        for text in control_texts:
            rendered_text = self.font.render(text, True, WHITE)
            screen.blit(rendered_text, (self.panel_x + 15, y_pos))
            y_pos += 25
            
    def set_mode(self, mode):
        """Update the current game mode"""
        self.current_mode = mode