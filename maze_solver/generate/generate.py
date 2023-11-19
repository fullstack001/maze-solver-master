import numpy as np
import random
import matplotlib.pyplot as plt

def generate_maze(height, width):
    maze = carve_maze(height, width)
    return np.where(maze == 1, 255, 0)

def carve_maze(width, height):
    maze = np.zeros(shape=(width, height), dtype=int) #[[0 for _ in range(width)] for _ in range(height)]  # Initialize the maze with walls

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and maze[y, x] == 0

    # Recursive backtracking algorithm to traverse the grid to supply a maze.
    # The algorithm will keep visiting unexplored neighbours until it has carved a path. 
    # We are using a slice of 3 to ensure that we are not carving a path into a wall.
    def recursive_backtracking(x, y):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # Right, Down, Left, Up
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + 2 * dx, y + 2 * dy  # Calculate new cell coordinates
            if is_valid(new_x, new_y):
                maze[y + dy, x + dx] = 1  # Carve a path
                maze[new_y, new_x] = 1
                recursive_backtracking(new_x, new_y)

    entry_x, entry_y = 0, np.random.randint(0, height-1), 
    maze[entry_y, entry_x] = 1  # Set the entry point

    exit_x, exit_y = width - 1, np.random.randint(0, height-1)
    maze[exit_y, exit_x] = 1  # Set the exit point

    recursive_backtracking(entry_x, entry_y)
    maze = border(height, width, entry_y, exit_y, maze)
    return maze

#Maze needs a border to show a clearly defined entry and exit point. 
def border(height, width, entry_point, exit_point, maze):
    border_walls = np.zeros(shape=(height+2, width+2), dtype=int)
    border_walls[entry_point+1, 0] = 1;
    border_walls[exit_point+1, width+1] = 1;
    border_walls[1:border_walls.shape[0]-1,1:border_walls.shape[1]-1] = maze
    return border_walls

def print_maze(maze):
    for row in maze:
        print(" ".join("#" if cell == 0 else " " for cell in row))