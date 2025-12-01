import heapq

def manhattan_distance(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def solve_ucs(maze, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor in maze.get_valid_neighbors(current):
            new_cost = cost_so_far[current] + maze.get_cost(neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))

    path = []
    node = goal
    if node not in came_from:
        return [], visited
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path, visited

def solve_a_star(maze, start, goal):
    frontier = []
    h = manhattan_distance(start, goal)
    heapq.heappush(frontier, (h, start))
    came_from = {start: None}
    g_score = {start: 0}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor in maze.get_valid_neighbors(current):
            tentative_g = g_score[current] + maze.get_cost(neighbor)
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan_distance(neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(frontier, (f, neighbor))

    path = []
    node = goal
    if node not in came_from:
        return [], visited
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path, visited
