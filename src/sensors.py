from typing import List, Tuple
import math


class BaseSensor:
    """Base class for robot sensors."""
    def __init__(self, name: str):
        self.name = name
        self.reading = 0.0

    def update(self, robot_pos: Tuple[float, float], robot_heading: float, obstacles: List[Tuple[float, float, float, float]]) -> float:
        raise NotImplementedError


class DistanceSensor(BaseSensor):
    """Simulated LIDAR/ultrasonic distance sensor."""
    def __init__(self, name: str, angle_offset: float, max_range: float = 200.0):
        super().__init__(name)
        self.angle_offset = angle_offset
        self.max_range = max_range

    def update(self, robot_pos: Tuple[float, float], robot_heading: float, obstacles: List[Tuple[float, float, float, float]], arena_width: int, arena_height: int) -> float:
        """Calculate distance to nearest obstacle."""
        sensor_angle = robot_heading + self.angle_offset
        sensor_x = robot_pos[0] + math.cos(sensor_angle) * (15 + 10)
        sensor_y = robot_pos[1] + math.sin(sensor_angle) * (15 + 10)
        closest_distance = self.max_range

        for ox, oy, ow, oh in obstacles:
            nearest_x = max(ox, min(sensor_x, ox + ow))
            nearest_y = max(oy, min(sensor_y, oy + oh))
            distance = math.hypot(sensor_x - nearest_x, sensor_y - nearest_y)
            if distance < closest_distance:
                closest_distance = distance

        if sensor_x < 0 or sensor_x > arena_width or sensor_y < 0 or sensor_y > arena_height:
            closest_distance = min(closest_distance, 40.0)

        self.reading = closest_distance
        return closest_distance


class IMUSensor(BaseSensor):
    """Inertial Measurement Unit - tracks acceleration and heading."""
    def __init__(self, name: str):
        super().__init__(name)
        self.heading = 0.0
        self.angular_velocity = 0.0
        self.linear_velocity = 0.0

    def update(self, robot_heading: float, angular_velocity: float, linear_velocity: float) -> Tuple[float, float, float]:
        self.heading = robot_heading
        self.angular_velocity = angular_velocity
        self.linear_velocity = linear_velocity
        return (self.heading, self.angular_velocity, self.linear_velocity)


class SensorArray:
    """Array of sensors on the robot."""
    def __init__(self):
        self.sensors: List[BaseSensor] = []

    def add_sensor(self, sensor: BaseSensor) -> None:
        self.sensors.append(sensor)

    def get_reading(self, name: str) -> float:
        for sensor in self.sensors:
            if sensor.name == name:
                return sensor.reading
        return 0.0
