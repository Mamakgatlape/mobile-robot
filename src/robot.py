import math
from typing import List, Tuple, Optional
from src.sensors import SensorArray, DistanceSensor


class Robot:
    """Advanced mobile robot with multi-sensor support."""
    def __init__(self, x: float, y: float, robot_id: int = 0, radius: float = 18.0, heading: float = 0.0):
        self.robot_id = robot_id
        self.x = x
        self.y = y
        self.radius = radius
        self.heading = heading
        self.speed = 0.0
        self.turn_rate = 0.0
        self.max_speed = 3.0
        self.max_turn_rate = 0.08
        
        # Trajectory history
        self.trajectory: List[Tuple[float, float]] = [(x, y)]
        self.max_trajectory_length = 500
        
        # Sensor array
        self.sensors = SensorArray()
        self.sensors.add_sensor(DistanceSensor(f"front", 0.0))
        self.sensors.add_sensor(DistanceSensor(f"left", 0.75))
        self.sensors.add_sensor(DistanceSensor(f"right", -0.75))
        
        # Performance metrics
        self.total_distance = 0.0
        self.collision_count = 0
        self.goal_reached_count = 0

    def set_motion(self, speed: float, turn_rate: float) -> None:
        """Set motor commands."""
        self.speed = max(-self.max_speed, min(self.max_speed, speed))
        self.turn_rate = max(-self.max_turn_rate, min(self.max_turn_rate, turn_rate))

    def update(self, dt: float) -> None:
        """Update robot pose using kinematic model."""
        prev_x, prev_y = self.x, self.y
        
        self.heading += self.turn_rate * dt * 60.0
        self.x += math.cos(self.heading) * self.speed * dt * 60.0
        self.y += math.sin(self.heading) * self.speed * dt * 60.0
        
        # Update distance traveled
        self.total_distance += math.hypot(self.x - prev_x, self.y - prev_y)
        
        # Add to trajectory
        if len(self.trajectory) > self.max_trajectory_length:
            self.trajectory.pop(0)
        self.trajectory.append((self.x, self.y))

    def get_sensor_readings(self, obstacles: List[Tuple[float, float, float, float]], arena_width: int, arena_height: int) -> List[float]:
        """Get all sensor readings."""
        readings = []
        for sensor in self.sensors.sensors:
            if hasattr(sensor, 'update'):
                reading = sensor.update((self.x, self.y), self.heading, obstacles, arena_width, arena_height)
                readings.append(reading)
        return readings

    def record_collision(self) -> None:
        """Record collision event."""
        self.collision_count += 1

    def record_goal_reached(self) -> None:
        """Record goal reached event."""
        self.goal_reached_count += 1

    def reset(self, x: float, y: float) -> None:
        """Reset robot to initial state."""
        self.x = x
        self.y = y
        self.heading = 0.0
        self.speed = 0.0
        self.turn_rate = 0.0
        self.trajectory = [(x, y)]
        self.total_distance = 0.0
