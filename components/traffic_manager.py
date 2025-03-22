class TrafficManager:
    """Manages traffic flow and prevents collisions between cars and obstacles"""
    
    def __init__(self, grid, player_car, traffic_cars, dynamic_obstacles):
        self.grid = grid
        self.player_car = player_car
        self.traffic_cars = traffic_cars.cars if hasattr(traffic_cars, 'cars') else traffic_cars
        self.dynamic_obstacles = dynamic_obstacles
        self.collision_count = 0
        self.recalculations = 0
        
    def update(self):
        """Update traffic conditions and handle collision avoidance"""
        # Get current positions of all dynamic entities
        obstacle_positions = {(obs.x, obs.y) for obs in self.dynamic_obstacles}
        car_positions = {(car.x, car.y) for car in self.traffic_cars}
        
        # Add player car position
        player_pos = (self.player_car.x, self.player_car.y)
        
        # Check player car's next move for potential collisions
        if self.player_car.path:
            next_pos = self.player_car.path[0]
            
            if (next_pos in obstacle_positions) or (next_pos in car_positions and next_pos != player_pos):
                # Collision would occur, recalculate
                self.player_car.path = []  # Clear path to force recalculation
                self.recalculations += 1
        
        # Check and handle emergency stops for traffic cars
        for i, car in enumerate(self.traffic_cars):
            if car.path:
                next_pos = car.path[0]
                
                # Create a set of all positions except this car's current position
                other_car_positions = car_positions.copy()
                other_car_positions.discard((car.x, car.y))
                
                # Check if next position would cause collision
                if (next_pos in obstacle_positions) or (next_pos in other_car_positions) or (next_pos == player_pos):
                    # Potential collision, recalculate or wait
                    car.path = []  # Force recalculation
                    self.recalculations += 1
    
    def check_collisions(self):
        """Check if any collisions occurred and log them"""
        player_pos = (self.player_car.x, self.player_car.y)
        obstacle_positions = {(obs.x, obs.y) for obs in self.dynamic_obstacles}
        car_positions = {(car.x, car.y) for car in self.traffic_cars}
        
        # Check for player collision with obstacles
        if player_pos in obstacle_positions:
            self.collision_count += 1
            return True
            
        # Check for player collision with other cars
        for car in self.traffic_cars:
            if player_pos == (car.x, car.y) and player_pos != (self.player_car.x, self.player_car.y):
                self.collision_count += 1
                return True
                
        return False
    
    def get_metrics(self):
        """Return current traffic metrics"""
        return {
            "collisions": self.collision_count,
            "recalculations": self.recalculations
        }