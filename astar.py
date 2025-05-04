import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # Cost from start
        self.h = 0  # Heuristic to goal
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    closed_list = set()

    start_node = Node(start)
    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heapq.heappop(open_list)
        closed_list.add(current.position)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse path

        # Check neighbors (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current.position[0] + dx, current.position[1] + dy)

            if (0 <= neighbor_pos[0] < rows and 0 <= neighbor_pos[1] < cols and
                grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and
                neighbor_pos not in closed_list):
                neighbor = Node(neighbor_pos, current)
                neighbor.g = current.g + 1
                neighbor.h = manhattan_distance(neighbor_pos, goal)
                neighbor.f = neighbor.g + neighbor.h

                # Check if neighbor is in open_list with a higher f score
                for _, node in open_list:
                    if node.position == neighbor_pos and node.f <= neighbor.f:
                        break
                else:
                    heapq.heappush(open_list, (neighbor.f, neighbor))

    return []  # No path found