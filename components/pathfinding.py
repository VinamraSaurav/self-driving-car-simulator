import heapq

def manhattan(a, b):
    """Calculate Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def manhattan_distance(a, b):
    """Calculate Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    """A* pathfinding algorithm"""
    open_list = [(0, start)]
    g_cost = {start: 0}
    f_cost = {start: manhattan(start, goal)}
    parent = {start: None}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

        for neighbor in neighbors:
            nx, ny = neighbor

            if 0 <= nx < grid.width and 0 <= ny < grid.height and not grid.is_occupied(nx, ny):
                new_g_cost = g_cost[current] + 1

                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost[neighbor] = new_g_cost + manhattan(neighbor, goal)
                    parent[neighbor] = current
                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))

    return None  # No path found
