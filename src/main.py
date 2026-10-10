import tkinter as tk
from src.robot_sim import RobotSimulation


def main() -> None:
    """Launch the advanced mobile robot simulation."""
    root = tk.Tk()
    root.title("Advanced Mobile Robot Simulation")
    app = RobotSimulation(root)
    root.mainloop()


if __name__ == "__main__":
    main()
