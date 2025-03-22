import pygame
from utils.config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, WHITE, BLACK

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
            "fps": 0
        }
    
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
        
        # Draw title
        title = self.title_font.render("SIMULATION METRICS", True, WHITE)
        screen.blit(title, (self.panel_x + 10, 20))
        
        # Draw metrics
        y_pos = 60
        for key, value in self.metrics.items():
            # Format the key name for display
            display_name = key.replace('_', ' ').title()
            
            # Render the metric
            text = self.font.render(f"{display_name}: {value}", True, WHITE)
            screen.blit(text, (self.panel_x + 15, y_pos))
            y_pos += 30
        
        # Draw divider line
        pygame.draw.line(screen, WHITE, 
                         (self.panel_x + 10, y_pos + 10), 
                         (self.panel_x + self.panel_width - 10, y_pos + 10), 2)
        
        # Draw controls section
        controls_title = self.title_font.render("CONTROLS", True, WHITE)
        screen.blit(controls_title, (self.panel_x + 10, y_pos + 30))
        
        # Draw control instructions
        control_texts = [
            "Click: Add/Remove Obstacle",
            "R: Reset Simulation",
            "P: Pause/Resume",
            "ESC: Quit"
        ]
        
        y_pos += 70
        for text in control_texts:
            rendered_text = self.font.render(text, True, WHITE)
            screen.blit(rendered_text, (self.panel_x + 15, y_pos))
            y_pos += 25