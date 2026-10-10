import math
import csv
import os
from typing import List, Tuple
from datetime import datetime


class Logger:
    """Data logger for robot metrics and sensor readings."""
    def __init__(self, log_dir: str = "data/logs"):
        self.log_dir = log_dir
        self.is_logging = False
        self.log_file = None
        self.writer = None
        self.timestamp = None

        os.makedirs(log_dir, exist_ok=True)

    def start_logging(self) -> None:
        """Start a new logging session."""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"robot_log_{self.timestamp}.csv")
        self.writer = csv.writer(open(self.log_file, 'w', newline=''))
        self.writer.writerow(["time", "x", "y", "heading", "speed", "sensor_front", "sensor_left", "sensor_right", "goal_distance"])
        self.is_logging = True

    def log_reading(self, time: float, robot_pos: Tuple[float, float], heading: float, speed: float, sensor_readings: List[float], goal_distance: float) -> None:
        """Log a single robot state."""
        if self.is_logging and self.writer:
            self.writer.writerow([
                f"{time:.2f}",
                f"{robot_pos[0]:.2f}",
                f"{robot_pos[1]:.2f}",
                f"{heading:.4f}",
                f"{speed:.2f}",
                f"{sensor_readings[0]:.2f}" if len(sensor_readings) > 0 else "0",
                f"{sensor_readings[1]:.2f}" if len(sensor_readings) > 1 else "0",
                f"{sensor_readings[2]:.2f}" if len(sensor_readings) > 2 else "0",
                f"{goal_distance:.2f}"
            ])

    def stop_logging(self) -> str:
        """Stop logging and return log file path."""
        self.is_logging = False
        if self.log_file:
            print(f"Log saved to: {self.log_file}")
        return self.log_file or ""
