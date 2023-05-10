import cx_Freeze, sys

base = None 
if sys.platform == 'win32': 
    base = "Win32GUI"

executables = [cx_Freeze.Executable("jai_walking.py", base=base, targetName="jai_walking")]

cx_Freeze.setup(
   name="jai_walking",
   options={"build_exe": {"packages": ["tkinter"], "include_files": ["player2.png", "road.png", "song.mp3", "car1.png", "car_facing_left.png", "car_facing_right.png", "finish_line.png"]}},
   version="1.0",
   description="DESCRIBE YOUR PROGRAM",
   executables=executables
)