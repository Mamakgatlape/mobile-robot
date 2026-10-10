from typing import List, Tuple
import math


class World:
    """World/environment containing obstacles and goals."""
    def __init__(self, width: int = 860, height: int = 520):
        self.width = width
        self.height = height
        self.obstacles: List[Tuple[float, float, float, float]] = []
        self.goals: List[Tuple[float, float]] = []

    def add_obstacle(self, x: float, y: float, width: float, height: float) -> None:
        """Add a static rectangular obstacle."""
        self.obstacles.append((x, y, width, height))

    def add_goal(self, x: float, y: float) -> None:
        """Add a goal location."""
        self.goals.append((x, y))

    def is_collision(self, robot_x: float, robot_y: float, robot_radius: float) -> bool:
        """Check if robot collides with any obstacle."""
        for ox, oy, ow, oh in self.obstacles:
            if (
                robot_x + robot_radius > ox
                and robot_x - robot_radius < ox + ow
                and robot_y + robot_radius > oy
                and robot_y - robot_radius < oy + oh
            ):
                return True
        return False

    def get_nearest_goal(self, x: float, y: float) -> Tuple[float, float]:
        """Get nearest goal to current position."""
        if not self.goals:
            return (self.width // 2, self.height // 2)
        return min(self.goals, key=lambda g: math.hypot(g[0] - x, g[1] - y))

    def clear(self) -> None:
        """Clear all obstacles and goals."""
        self.obstacles.clear()
        self.goals.clear()
