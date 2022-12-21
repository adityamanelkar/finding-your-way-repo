import math
import copy

class Drone:
    def __init__(self, name: str, pos: tuple) -> None:
        """
        Class has stuff on the drone object
        """
        self.name = name
        self.row = pos[0]
        self.col = pos[1]
        self.path = {}
        self.action = {}
        self.dist = {}

    def calc_heuristics(self, maze: list, dest: tuple) -> None:
        """
        Calculate shortest paths, action lists for the paths, and shortest distances
        """
        num_rows = len(maze)
        num_cols = len(maze[0])

        row = self.row
        col = self.col

        if maze[row][col] == "_":

            if (row, col) == dest:
                self.path[(row, col)] = [(row, col)]
                self.action[(row, col)] = []
                self.dist[(row, col)] = 0

            else:
                open_set = [(row, col)]
                closed_set = set([])

                # For pos (a, b), prev[(a, b)] is the node immediately preceding it on the path
                prev = {}

                x_delta = [0, 1, 0, -1]
                y_delta = [1, 0, -1, 0]

                while open_set:                            
                    # Pop current off open list, add to closed list
                    current = open_set.pop(0)

                    if not closed_set.intersection({current}):
                        closed_set.add(current)
                    
                    if current == dest:
                        
                        self.path[(row, col)] = self.create_path(prev, current)
                        self.action[(row, col)] = self.create_actions(self.path[(row, col)])
                        self.dist[(row, col)] = len(self.path[(row, col)])
                        break

                    for i in range(4):

                        neighbor = (current[0] + x_delta[i], current[1] + y_delta[i])

                        if self.valid_move(maze, neighbor, closed_set):

                            prev[neighbor] = current

                            if neighbor not in open_set:
                                open_set.append(neighbor)

                            if not closed_set.intersection({neighbor}):
                                closed_set.add(neighbor)

    def valid_move(self, maze: list, pos: tuple, closed_set: set = set([])) -> bool:

        # If we go out of bounds
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(maze) or pos[1] >= len(maze[0]):
            return False
            
        # If cell is blocked
        if maze[pos[0]][pos[1]] == "X":
            return False
        
        # If cell is already added to the closed set
        if closed_set.intersection({pos}):
            return False

        # If not none of the above situations arise, the cell can be added!
        return True

    def create_path(self, prev: dict, current: tuple) -> list:
        """
        Creates the shortest path
        """
        path = [current]

        while current in prev:
            current = prev[current]
            path.append(current)

        return path[::-1]

    def create_actions(self, path: list) -> list:
        """
        Creates the action list to follow a path
        """
        actions = []

        for i in range(1, len(path)):
            if path[i][0] > path[i - 1][0]:
                actions.append("DOWN")
            elif path[i][0] < path[i - 1][0]:
                actions.append("UP")
            elif path[i][1] > path[i - 1][1]:
                actions.append("RIGHT")
            elif path[i][1] < path[i - 1][1]:
                actions.append("LEFT")

        return actions

    def move_drone(self, maze: list, move: str) -> None:
        """
        Function that moves the submarine drone
        """
        moves = ["UP", "DOWN", "LEFT", "RIGHT"]

        x = copy.deepcopy(self.row)
        y = copy.deepcopy(self.col)

        if move == "UP" and self.valid_move(maze, (x - 1, y)):
            if maze[x - 1][y] == "_":
                self.row -= 1
        elif move == "DOWN" and self.valid_move(maze, (x + 1, y)):
            if maze[x + 1][y] == "_":
                self.row += 1
        elif move == "LEFT" and self.valid_move(maze, (x, y - 1)):
            if maze[x][y - 1] == "_":
                self.col -= 1
        elif move == "RIGHT" and self.valid_move(maze, (x, y + 1)):
            if maze[x][y + 1] == "_":
                self.col += 1
        else: # We run into an "X" (i.e a wall) or out of bounds
            # print("here")
            pass

        # print("New pos: {}".format((self.row, self.col)))
