from components.pathfinding import a_star

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
        """Update traffic management and collision avoidance"""
        # Get current position of player car
        player_pos = (self.player_car.x, self.player_car.y)

        # Get next position of player car from its path
        player_next_pos = self.player_car.path[0] if self.player_car.path else player_pos

        # Update traffic car paths to avoid collision with player
        for car in self.traffic.cars:
            # Skip if car not moving
            if car.is_moving:
                continue

            # Check if car's next move would collide with player's current or next position
            if car.path and (car.path[0] == player_pos or car.path[0] == player_next_pos):
                # Temporarily mark player positions as obstacles for pathfinding
                self.grid.add_dynamic_obstacle(player_pos[0], player_pos[1])
                if player_next_pos != player_pos:
                    self.grid.add_dynamic_obstacle(player_next_pos[0], player_next_pos[1])

                # Recalculate path
                car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
                self.metrics["recalculations"] += 1

                # Remove temporary obstacles
                self.grid.remove_dynamic_obstacle(player_pos[0], player_pos[1])
                if player_next_pos != player_pos:
                    self.grid.remove_dynamic_obstacle(player_next_pos[0], player_next_pos[1])

        # Check if player's next move would collide with any traffic car
        if self.player_car.path:
            for car in self.traffic.cars:
                car_pos = (car.x, car.y)
                car_next_pos = car.path[0] if car.path else car_pos

                if player_next_pos == car_pos or player_next_pos == car_next_pos:
                    # Temporarily mark traffic car positions as obstacles
                    self.grid.add_dynamic_obstacle(car_pos[0], car_pos[1])
                    if car_next_pos != car_pos:
                        self.grid.add_dynamic_obstacle(car_next_pos[0], car_next_pos[1])

                    # Recalculate player path
                    self.player_car.path = a_star(self.grid, 
                                               (self.player_car.x, self.player_car.y), 
                                               (self.player_car.goal_x, self.player_car.goal_y)) or []
                    self.player_car.recalculations += 1

                    # Remove temporary obstacles
                    self.grid.remove_dynamic_obstacle(car_pos[0], car_pos[1])
                    if car_next_pos != car_pos:
                        self.grid.remove_dynamic_obstacle(car_next_pos[0], car_next_pos[1])



        
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