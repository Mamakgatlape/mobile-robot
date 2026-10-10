import math
from typing import List, Tuple, Optional
from heapq import heappush, heappop


class Node:
    """Node in A* pathfinding grid."""
    def __init__(self, x: int, y: int, g: float = 0.0, h: float = 0.0):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent: Optional['Node'] = None

    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f

    def __eq__(self, other: 'Node') -> bool:
        return self.x == other.x and self.y == other.y


class AStar:
    """A* pathfinding algorithm for mobile robots."""
    
    def __init__(self, grid_width: int, grid_height: int, cell_size: int = 20):
        self.grid_width = grid_width // cell_size
        self.grid_height = grid_height // cell_size
        self.cell_size = cell_size

    def heuristic(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """Euclidean distance heuristic."""
        dx = pos[0] - goal[0]
        dy = pos[1] - goal[1]
        return math.sqrt(dx * dx + dy * dy)

    def get_neighbors(self, node: Node) -> List[Node]:
        """Get valid neighboring nodes (8-directional)."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = node.x + dx, node.y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    cost = 1.4 if dx != 0 and dy != 0 else 1.0
                    neighbors.append(Node(nx, ny, node.g + cost))
        return neighbors

    def find_path(self, start: Tuple[float, float], goal: Tuple[float, float], obstacles: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Find optimal path from start to goal avoiding obstacles."""
        start_node = Node(int(start[0] // self.cell_size), int(start[1] // self.cell_size))
        goal_node = Node(int(goal[0] // self.cell_size), int(goal[1] // self.cell_size))

        open_list = [start_node]
        closed_set = set()

        while open_list:
            current = heappop(open_list)

            if current == goal_node:
                path = []
                while current is not None:
                    path.append((current.x * self.cell_size + self.cell_size // 2, current.y * self.cell_size + self.cell_size // 2))
                    current = current.parent
                return list(reversed(path))

            closed_set.add((current.x, current.y))

            for neighbor in self.get_neighbors(current):
                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                if self.is_in_obstacle(neighbor, obstacles):
                    continue

                neighbor.h = self.heuristic((neighbor.x, neighbor.y), (goal_node.x, goal_node.y))
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                heappush(open_list, neighbor)

        return [start]  # No path found

    def is_in_obstacle(self, node: Node, obstacles: List[Tuple[float, float, float, float]]) -> bool:
        """Check if node is inside an obstacle."""
        x = node.x * self.cell_size
        y = node.y * self.cell_size
        for ox, oy, ow, oh in obstacles:
            if x >= ox - self.cell_size and x <= ox + ow and y >= oy - self.cell_size and y <= oy + oh:
                return True
        return False
