
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = grid.width, grid.height
    pq = []
    heapq.heappush(pq, (0 + heuristic(start, goal), 0, start, []))
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    goal_surroundings = [
        (goal[0] - 1, goal[1]),
        (goal[0] + 1, goal[1]),
        (goal[0], goal[1] - 1),
        (goal[0], goal[1] + 1)
    ]

    valid_goal_surroundings = [
        (x, y) for (x, y) in goal_surroundings if 0 <= x < rows and 0 <= y < cols and not grid.get(x, y)
    ]

    while pq:
        _, cost, (x, y), action_list = heapq.heappop(pq)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) in valid_goal_surroundings:
            return action_list  # return action list

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                cell = grid.get(nx, ny)

                if cell is not None:
                    if cell.type=="wall":
                        continue
                    if cell.type=="door" and cell.is_open == False:
                        continue

                new_actions = action_list + [(dx, dy)]
                heapq.heappush(pq, (cost + 1 + heuristic((nx, ny), goal), cost + 1, (nx, ny), new_actions))

    return None



def is_near(source_pos,target_pos):
    # Check if two positions are near each other based on a specified threshold.
    x_diff = abs(source_pos[0] - target_pos[0])
    y_diff = abs(source_pos[1] - target_pos[1])
    return (x_diff + y_diff) <= 1



