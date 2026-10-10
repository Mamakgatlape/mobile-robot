import math
import tkinter as tk
from typing import List, Dict, Tuple, Optional
from src.robot import Robot
from src.world import World
from src.controllers import ManualController, AutonomousController
from src.pathfinding import AStar
from src.logger import Logger
from src.utils import normalize_angle


class RobotSimulation:
    """Advanced robot simulation with multi-robot support and path planning."""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Canvas setup
        self.canvas = tk.Canvas(root, width=960, height=540, bg="#0f172a")
        self.canvas.pack(padx=20, pady=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Mode: Manual | FPS: 0 | Robots: 1")
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 11), fg="#e2e8f0", bg="#1e293b")
        self.status_label.pack(fill=tk.X, padx=20, pady=8)
        
        # World setup
        self.world = World(width=960, height=540)
        self.world.add_obstacle(170, 120, 180, 22)
        self.world.add_obstacle(300, 300, 160, 22)
        self.world.add_obstacle(500, 150, 22, 180)
        self.world.add_obstacle(610, 350, 170, 22)
        self.world.add_goal(800, 420)
        
        # Robot management
        self.robots: Dict[int, Robot] = {}
        self.selected_robot_id = 0
        self.robot_counter = 1
        self.spawn_robot(120, 170)
        
        # Controllers
        self.manual_controller = ManualController()
        self.autonomous_controller = AutonomousController()
        self.autonomous_mode = False
        
        # Path planning
        self.pathfinder = AStar(960, 540, cell_size=20)
        self.show_path = False
        self.planned_paths: Dict[int, List[Tuple[float, float]]] = {}
        
        # Data logging
        self.logger = Logger()
        self.frame_count = 0
        self.fps = 0
        
        # Visualization flags
        self.show_trajectories = True
        self.show_sensors = True
        self.show_obstacles = True
        
        # Key binding
        self.setup_key_bindings()
        
        # Animation loop
        self.root.after(16, self.animate)

    def setup_key_bindings(self) -> None:
        """Setup keyboard controls."""
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_key_press(self, event) -> None:
        """Handle key press events."""
        key = event.keysym.lower()
        
        # Movement controls
        if key in ["w", "up"]:
            self.manual_controller.set_control("forward", True)
        elif key in ["s", "down"]:
            self.manual_controller.set_control("backward", True)
        elif key in ["a", "left"]:
            self.manual_controller.set_control("left", True)
        elif key in ["d", "right"]:
            self.manual_controller.set_control("right", True)
        
        # Mode switches
        elif key == "space":
            self.autonomous_mode = not self.autonomous_mode
        elif key == "r":
            self.reset_selected_robot()
        elif key == "p":
            self.show_path = not self.show_path
        elif key == "l":
            if self.logger.is_logging:
                self.logger.stop_logging()
            else:
                self.logger.start_logging()
        elif key == "n":
            self.spawn_robot(120, 170)
        elif key == "c":
            for robot in self.robots.values():
                robot.trajectory.clear()
        elif key == "t":
            self.show_trajectories = not self.show_trajectories
        elif key == "o":
            self.show_obstacles = not self.show_obstacles

    def on_key_release(self, event) -> None:
        """Handle key release events."""
        key = event.keysym.lower()
        if key in ["w", "up"]:
            self.manual_controller.set_control("forward", False)
        elif key in ["s", "down"]:
            self.manual_controller.set_control("backward", False)
        elif key in ["a", "left"]:
            self.manual_controller.set_control("left", False)
        elif key in ["d", "right"]:
            self.manual_controller.set_control("right", False)

    def spawn_robot(self, x: float, y: float) -> None:
        """Add a new robot to the simulation."""
        robot = Robot(x, y, robot_id=self.robot_counter)
        self.robots[self.robot_counter] = robot
        self.selected_robot_id = self.robot_counter
        self.robot_counter += 1

    def reset_selected_robot(self) -> None:
        """Reset the selected robot."""
        if self.selected_robot_id in self.robots:
            self.robots[self.selected_robot_id].reset(120, 170)

    def update_robots(self, dt: float) -> None:
        """Update all robots."""
        for robot_id, robot in self.robots.items():
            if robot_id == self.selected_robot_id and not self.autonomous_mode:
                speed, turn = self.manual_controller.get_motion()
                robot.set_motion(speed, turn)
            elif self.autonomous_mode:
                sensor_readings = robot.get_sensor_readings(self.world.obstacles, self.world.width, self.world.height)
                goal = self.world.get_nearest_goal(robot.x, robot.y)
                speed, turn = self.autonomous_controller.compute_motion((robot.x, robot.y), robot.heading, goal, sensor_readings)
                robot.set_motion(speed, turn)
            
            robot.update(dt)
            self.constrain_robot(robot)
            self.handle_collisions(robot)
            
            if self.logger.is_logging:
                sensor_readings = robot.get_sensor_readings(self.world.obstacles, self.world.width, self.world.height)
                goal = self.world.get_nearest_goal(robot.x, robot.y)
                goal_dist = math.hypot(goal[0] - robot.x, goal[1] - robot.y)
                self.logger.log_reading(self.frame_count / 60.0, (robot.x, robot.y), robot.heading, robot.speed, sensor_readings, goal_dist)

    def constrain_robot(self, robot: Robot) -> None:
        """Keep robot within arena bounds."""
        robot.x = max(robot.radius, min(robot.x, self.world.width - robot.radius))
        robot.y = max(robot.radius, min(robot.y, self.world.height - robot.radius))

    def handle_collisions(self, robot: Robot) -> None:
        """Handle robot-obstacle collisions."""
        for ox, oy, ow, oh in self.world.obstacles:
            if (
                robot.x + robot.radius > ox
                and robot.x - robot.radius < ox + ow
                and robot.y + robot.radius > oy
                and robot.y - robot.radius < oy + oh
            ):
                robot.x -= math.cos(robot.heading) * 3.0
                robot.y -= math.sin(robot.heading) * 3.0
                robot.speed *= -0.5
                robot.turn_rate *= -0.8
                robot.record_collision()

    def draw_world(self) -> None:
        """Draw the simulation environment."""
        self.canvas.delete("all")
        
        # Arena border
        self.canvas.create_rectangle(10, 10, 950, 530, outline="#334155", width=2)
        
        # Obstacles
        if self.show_obstacles:
            for ox, oy, ow, oh in self.world.obstacles:
                self.canvas.create_rectangle(ox, oy, ox + ow, oy + oh, fill="#f59e0b", outline="#b45309", width=2)
        
        # Goals
        for gx, gy in self.world.goals:
            self.canvas.create_oval(gx - 12, gy - 12, gx + 12, gy + 12, fill="#22c55e", outline="#15803d", width=2)
        
        # Draw robots
        for robot in self.robots.values():
            self.draw_robot(robot)
        
        # Draw trajectories
        if self.show_trajectories:
            for robot in self.robots.values():
                if len(robot.trajectory) > 1:
                    self.canvas.create_line(*[coord for point in robot.trajectory for coord in point], fill="#60a5fa", dash=(2, 2), width=1)
        
        # Draw paths if enabled
        if self.show_path and self.selected_robot_id in self.robots:
            robot = self.robots[self.selected_robot_id]
            goal = self.world.get_nearest_goal(robot.x, robot.y)
            path = self.pathfinder.find_path((robot.x, robot.y), goal, self.world.obstacles)
            if len(path) > 1:
                for i in range(len(path) - 1):
                    x1, y1 = path[i]
                    x2, y2 = path[i + 1]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#a78bfa", width=2)
        
        # Status text
        status_text = f"Robots: {len(self.robots)} | Mode: {'Autonomous' if self.autonomous_mode else 'Manual'} | Path: {'ON' if self.show_path else 'OFF'}"
        self.canvas.create_text(480, 30, text=status_text, fill="#e2e8f0", font=("Arial", 11, "bold"))

    def draw_robot(self, robot: Robot) -> None:
        """Draw a single robot."""
        x1 = robot.x
        y1 = robot.y
        x2 = robot.x + math.cos(robot.heading) * (robot.radius + 18)
        y2 = robot.y + math.sin(robot.heading) * (robot.radius + 18)
        
        color = "#3b82f6" if robot.robot_id == self.selected_robot_id else "#6366f1"
        self.canvas.create_oval(
            x1 - robot.radius, y1 - robot.radius,
            x1 + robot.radius, y1 + robot.radius,
            fill=color, outline="#1e3a8a", width=2
        )
        self.canvas.create_line(x1, y1, x2, y2, fill="#dbeafe", width=3)
        
        # Robot ID label
        self.canvas.create_text(x1, y1 - 25, text=f"R{robot.robot_id}", fill="#e2e8f0", font=("Arial", 9, "bold"))

    def animate(self) -> None:
        """Main animation loop."""
        dt = 1.0 / 60.0
        self.update_robots(dt)
        self.draw_world()
        
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.fps = 60
        
        self.status_var.set(f"Mode: {'Autonomous' if self.autonomous_mode else 'Manual'} | FPS: {self.fps} | Robots: {len(self.robots)}")
        self.root.after(16, self.animate)


__all__ = ["RobotSimulation"]
