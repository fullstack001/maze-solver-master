import numpy as np

#When given an image of a maze this script and functions will attempt to solve it. 

def solve_maze(maze, repaint_callback):
    explorer = Explorer(maze, repaint_callback)
    
    explorer.visited = explorer.explore_maze(explorer.entry_point, explorer.exit_point, {})
    explorer.paint_paths()
    explorer.solvable = explorer.determine_solvability()
    repaint_callback(explorer.maze_for_image_update)
    explorer.show_solutions()

    return explorer

class Explorer:
    entry_point = 0
    exit_point = 0
    maze = None
    maze_for_image_update = None
    visited = {}
    solvable = False
    repaint_callback = None

    def __init__(self, maze, repaint_callback):
        self.maze = maze
        self.maze_for_image_update = maze.copy()
        self.repaint_callback = repaint_callback
        self.find_entry_point(maze)
        self.last_path_pos = self.entry_point
        self.find_exit_point(maze)
        
    def show_solutions(self):
        for path in self.solvable:
            for point in path:
                self.repaint_callback(self.paint_point(point, 75))

    def unpack(self):
        unpacked_children = []
        def flatten(node):
            nonlocal unpacked_children
            unpacked_children.append(node)
            for child in node["children"]:
                flatten(child)
        flatten(self.visited)
        return unpacked_children

    def paint_paths(self):
        node = self.visited
        flattened_tree = self.unpack()
        for node in flattened_tree:
            for point in node["current_path"]:
                curr_maze = self.paint_point(np.array(point), 200)
        return curr_maze

    def explore_maze(self, current_position, end_position, visited, node=None, intersects=None):
        row, col = current_position

        # Check if the current position is out of bounds or an obstacle
        if (
            row < 0
            or col < 0
            or row >= self.maze.shape[0]
            or col >= self.maze.shape[1]
            or self.maze[row, col] == 0  # Check for walls
        ):
            return {}
        
        #If the length of visisted is falsy, assume we're at the start of the maze
        if (node == None):
            node = {
                "start": (row, col),
                "end": None,
                "dir_x": True,
                "dir_y": False,
                "direction": 1,
                "dead_end": False,
                "children": [], 
                "current_path": []
            }

        # We need to see if this is a complete path.
        current_path = [current_position] 
        direction = None
        if (node["dir_x"]):
            direction = (row, col+node["direction"])
        if (node["dir_y"]):
            direction = (row+node["direction"], col)

        d_row, d_col = direction
        while (self.maze[row, col] == self.maze[min(d_row, self.maze.shape[0]-1), min(d_col, self.maze.shape[1]-1)]):
            if (d_row > self.maze.shape[0]-1 or d_col > self.maze.shape[1]-1): #We've exceeded the bounds of the maze
                break
            current_path.append(direction)
            node["end"] = [direction[0], direction[1]]
            direction = (d_row, d_col + node["direction"]) if node["dir_x"] else (d_row + node["direction"], d_col)
            d_row, d_col = direction

        current_path = np.array(current_path)
        node["current_path"] = current_path

        if intersects == None:
            intersects = []

        intersects.append(current_path)

        # Split into separate arrays for x and y axes
        x_values = current_path[:, 0]  # Extract the x
        y_values = current_path[:, 1]  # Extract the y
        dir_x = np.all(x_values == x_values[0])
        dir_y = np.all(y_values == y_values[0])
        node["dir_x"] = dir_x
        node["dir_y"] = dir_y

        def exists_in_intersect(step):
            for intersect in intersects:
                intersect = intersect.tolist()
                if step in intersect:
                    return True
            return False

        children = []
        for step in current_path:
            if dir_x:
                if (self.maze[step[0]-1, step[1]] == 255 and not exists_in_intersect([step[0]-1, step[1]])):
                    children.append({ "start": step, "end": None, "dir_x": False, "dir_y": True, "direction": -1, "dead_end": False, "children": []})
                if (self.maze[step[0]+1, step[1]] == 255 and not exists_in_intersect([step[0]+1, step[1]])):
                    children.append({ "start": step, "end": None, "dir_x": False, "dir_y": True, "direction": 1, "dead_end": False, "children": []})
            if dir_y:
                if (self.maze[step[0], step[1]-1] == 255 and not exists_in_intersect([step[0], step[1]-1])):
                    children.append({ "start": step, "end": None, "dir_x": True, "dir_y": False, "direction": -1, "dead_end": False, "children": []})
                if (self.maze[step[0], step[1]+1] == 255 and not exists_in_intersect([step[0], step[1]+1])):
                    children.append({ "start": step, "end": None, "dir_x": True, "dir_y": False, "direction": 1, "dead_end": False, "children": []})
        node["children"] = children
    

        if not len(children):
            node["dead_end"] = not np.any(np.all(np.array(node["end"]) == np.array(self.exit_point)))

        for child in children:
            child = self.explore_maze(child["start"], child["end"], visited, child, intersects)

        return node
    
    def determine_solvability(self):
        solvable_paths = []
        curr_path = []
        def solvable(node):
            curr_path.append(np.array(node["start"]))
            if len(node["children"]) == 0:
                if not node["dead_end"]:
                    solvable_paths.append(curr_path.copy())
                    curr_path.clear() #reset the curr path array incase theres more than one road paved with gold
            else:
                for child in node["children"]:
                    solvable(child)
        solvable(self.visited)
        return solvable_paths     
    
    def paint_point(self, point, colour):
        point_colour = self.maze_for_image_update[point[0], point[1]]
        self.maze_for_image_update[point[0], point[1]] = colour if point_colour == 255 or point_colour == 200 else point_colour
        return self.maze_for_image_update.copy()
    
    def find_entry_point(self, maze):
        height, width = maze.shape
        for h in range(height):
            if self.maze[h, 0] == 255:
                entry_point = h
        self.entry_point = [entry_point, 0]
        self.repaint_callback(self.paint_point(self.entry_point, 100))

    def find_exit_point(self, maze):
        height, width = maze.shape
        for h in range(height):
            if self.maze[h, -1] == 255:
                exit_point = h
        self.exit_point = [exit_point, width-1]
        self.repaint_callback(self.paint_point(self.exit_point, 100))