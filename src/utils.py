import math
from typing import List, Tuple, Optional


class Vector2:
    """2D vector math utility."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: 'Vector2') -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def angle_to(self, other: 'Vector2') -> float:
        return math.atan2(other.y - self.y, other.x - self.x)

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))


def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi]."""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def point_to_line_distance(point: Tuple[float, float], line_start: Tuple[float, float], line_end: Tuple[float, float]) -> float:
    """Calculate shortest distance from point to line segment."""
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end

    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D

    if len_sq == 0:
        return math.hypot(A, B)

    param = max(0, min(1, dot / len_sq))
    xx = x1 + param * C
    yy = y1 + param * D

    return math.hypot(x - xx, y - yy)
