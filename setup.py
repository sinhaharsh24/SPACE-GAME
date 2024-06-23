from cx_Freeze import setup, Executable

setup(
    name="SpaceGame",
    version="0.1",
    description="It's a game version of space invaders",
    executables=[Executable("SPACEGAME.py")]
)
