import tkinter as tk
import math
from src.robot import Robot
from src.world import World
from src.pathfinding import AStar


def test_robot_creation():
    """Test robot instantiation."""
    robot = Robot(100.0, 100.0, robot_id=1)
    assert robot.x == 100.0
    assert robot.y == 100.0
    assert robot.robot_id == 1
    print("✓ test_robot_creation passed")


def test_robot_movement():
    """Test robot movement."""
    robot = Robot(0.0, 0.0, heading=0.0)
    robot.set_motion(1.0, 0.0)
    robot.update(1.0)
    assert robot.x > 0
    assert robot.y == 0.0
    print("✓ test_robot_movement passed")


def test_sensor_readings():
    """Test sensor readings."""
    robot = Robot(100.0, 100.0)
    obstacles = [(150, 150, 40, 40)]
    readings = robot.get_sensor_readings(obstacles, 400, 400)
    assert len(readings) == 3
    assert all(r >= 0 for r in readings)
    print("✓ test_sensor_readings passed")


def test_world_collision():
    """Test world collision detection."""
    world = World()
    world.add_obstacle(100, 100, 50, 50)
    assert world.is_collision(120, 120, 15) == True
    assert world.is_collision(10, 10, 15) == False
    print("✓ test_world_collision passed")


def test_pathfinding():
    """Test A* pathfinding."""
    pathfinder = AStar(200, 200, cell_size=20)
    path = pathfinder.find_path((10, 10), (190, 190), [])
    assert len(path) > 0
    assert path[0][0] >= 0 and path[0][1] >= 0
    print("✓ test_pathfinding passed")


if __name__ == "__main__":
    test_robot_creation()
    test_robot_movement()
    test_sensor_readings()
    test_world_collision()
    test_pathfinding()
    print("\nAll tests passed! ✓")
