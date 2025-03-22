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
        player_pos = (self.player_car.x, self.player_car.y)
        player_next_pos = self.player_car.path[0] if self.player_car.path else player_pos

        for car in self.traffic_cars:
            if car.is_moving:
                continue

            if car.path and (car.path[0] == player_pos or car.path[0] == player_next_pos):
                self.grid.add_dynamic_obstacle(player_pos[0], player_pos[1])
                if player_next_pos != player_pos:
                    self.grid.add_dynamic_obstacle(player_next_pos[0], player_next_pos[1])

                car.path = a_star(self.grid, (car.x, car.y), (car.goal_x, car.goal_y)) or []
                self.recalculations += 1

                self.grid.remove_dynamic_obstacle(player_pos[0], player_pos[1])
                if player_next_pos != player_pos:
                    self.grid.remove_dynamic_obstacle(player_next_pos[0], player_next_pos[1])

        if self.player_car.path:
            for car in self.traffic_cars:
                car_pos = (car.x, car.y)
                car_next_pos = car.path[0] if car.path else car_pos

                if player_next_pos == car_pos or player_next_pos == car_next_pos:
                    self.grid.add_dynamic_obstacle(car_pos[0], car_pos[1])
                    if car_next_pos != car_pos:
                        self.grid.add_dynamic_obstacle(car_next_pos[0], car_next_pos[1])

                    self.player_car.path = a_star(self.grid, 
                                                  (self.player_car.x, self.player_car.y), 
                                                  (self.player_car.goal_x, self.player_car.goal_y)) or []
                    self.player_car.recalculations += 1

                    self.grid.remove_dynamic_obstacle(car_pos[0], car_pos[1])
                    if car_next_pos != car_pos:
                        self.grid.remove_dynamic_obstacle(car_next_pos[0], car_next_pos[1])

    def check_collisions(self):
        """Check for collisions between the player and other cars or obstacles"""
        player_pos = (self.player_car.x, self.player_car.y)
        obstacle_positions = {(obs.x, obs.y) for obs in self.dynamic_obstacles}
        car_positions = {(car.x, car.y) for car in self.traffic_cars}
        
        if player_pos in obstacle_positions or player_pos in car_positions:
            self.collision_count += 1
            return True
        return False

    def get_metrics(self):
        """Return current traffic metrics"""
        return {
            "collisions": self.collision_count,
            "recalculations": self.recalculations
        }
