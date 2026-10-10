windows_path = r"""
Quick Start on Windows:

1. Open PowerShell or Command Prompt

2. Clone the repository:
   git clone https://github.com/Mamakgatlape/mobile-robot.git
   cd mobile-robot

3. Run the simulation:
   python src/main.py

Alternatively, download ZIP:
1. Go to https://github.com/Mamakgatlape/mobile-robot
2. Click "Code" → "Download ZIP"
3. Extract the ZIP
4. Open PowerShell in the folder
5. Run: python src/main.py

Keyboard Controls:
- W/Up: Forward
- S/Down: Backward
- A/Left: Turn left
- D/Right: Turn right
- Space: Toggle autonomous
- P: Toggle path planning
- N: Spawn new robot
- L: Log data
- Esc: Exit
"""

mac_linux_path = r"""
Quick Start on macOS/Linux:

1. Open Terminal

2. Clone the repository:
   git clone https://github.com/Mamakgatlape/mobile-robot.git
   cd mobile-robot

3. Run the simulation:
   python3 src/main.py

Alternatively, download ZIP:
1. Go to https://github.com/Mamakgatlape/mobile-robot
2. Click "Code" → "Download ZIP"
3. Extract: unzip mobile-robot-main.zip && cd mobile-robot-main
4. Run: python3 src/main.py

Keyboard Controls:
- W/Up: Forward
- S/Down: Backward
- A/Left: Turn left
- D/Right: Turn right
- Space: Toggle autonomous
- P: Toggle path planning
- N: Spawn new robot
- L: Log data
- Esc: Exit
"""

if __name__ == "__main__":
    import platform
    if platform.system() == "Windows":
        print(windows_path)
    else:
        print(mac_linux_path)
