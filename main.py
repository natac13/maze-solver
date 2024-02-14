from graphics import Window
from maze import Maze


def main():
    window = Window(800, 600)
    # Draw the maze here

    maze = Maze(10, 10, 10, 10, 20, 20, window)

    window.wait_for_close()


if __name__ == "__main__":
    main()
