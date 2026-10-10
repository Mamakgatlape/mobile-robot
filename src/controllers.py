import math
from typing import List, Tuple, Dict, Optional


class PIDController:
    """PID controller for motion control."""
    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, error: float, dt: float) -> float:
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def reset(self) -> None:
        self.integral = 0.0
        self.prev_error = 0.0


class ManualController:
    """Manual control handler."""
    def __init__(self):
        self.controls = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
        }

    def set_control(self, control: str, active: bool) -> None:
        if control in self.controls:
            self.controls[control] = active

    def get_motion(self) -> Tuple[float, float]:
        speed = 0.0
        turn = 0.0

        if self.controls["forward"]:
            speed += 2.2
        if self.controls["backward"]:
            speed -= 1.8
        if self.controls["left"]:
            turn -= 0.08
        if self.controls["right"]:
            turn += 0.08

        return speed, turn


class AutonomousController:
    """Autonomous navigation controller."""
    def __init__(self):
        self.angle_pid = PIDController(kp=0.35, ki=0.0, kd=0.1)
        self.target_position: Optional[Tuple[float, float]] = None

    def compute_motion(self, robot_pos: Tuple[float, float], robot_heading: float, target: Tuple[float, float], sensor_readings: List[float]) -> Tuple[float, float]:
        """Compute autonomous motion commands."""
        front_distance = sensor_readings[1] if len(sensor_readings) > 1 else 100.0
        left_distance = sensor_readings[0] if len(sensor_readings) > 0 else 100.0
        right_distance = sensor_readings[2] if len(sensor_readings) > 2 else 100.0

        target_angle = math.atan2(target[1] - robot_pos[1], target[0] - robot_pos[0])
        angle_error = target_angle - robot_heading

        while angle_error > math.pi:
            angle_error -= 2 * math.pi
        while angle_error < -math.pi:
            angle_error += 2 * math.pi

        if front_distance < 50 or left_distance < 35 or right_distance < 35:
            if left_distance < right_distance:
                return 0.5, 0.12
            else:
                return 0.5, -0.12

        turn = self.angle_pid.update(angle_error, 1.0 / 60.0)
        return 1.8, turn

    def reset(self) -> None:
        self.angle_pid.reset()
