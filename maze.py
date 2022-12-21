import random
from colorama import init
from colorama import deinit
from colorama import Fore

# Display for debugging the maze
def display(maze: list, num_rows: int, num_cols: int) -> None:
    for row in range(num_rows):
        for col in range(num_cols):
            if (maze[row][col] == "_"):
                print(Fore.WHITE + str(maze[row][col]), end=" ")
            elif (maze[row][col] == "X"):
                print(Fore.BLACK + str(maze[row][col]), end=" ")
        print("\n")

# Module to save a reactor maze map in reactor<num>.txt
def save_txt(filename: str, maze: list) -> list:
    """
    Writes the reactor maze to a text file
    """
    with open(filename, "w") as f:
        for row in maze:
            f.write("".join([str(cell) for cell in row]))
            f.write("\n")

# Block maze by x percent
def create_walls(maze: list, x: int, num_rows: int, num_cols: int) -> None:
    """
    Create walls (X) with an x% probability in a maze
    """
    per = float(x / 100)
    for i in range(num_rows):
        for j in range(num_cols):
            if random.random() < per: # Block the cell with a x% chance
                maze[i][j] = "X"

def valid_neighbor(neighbor: tuple, maze: list, visited: list, num_rows: int, num_cols: int) -> bool:
    """
    Check for out of bounds and walls
    """
    # If we go out of bounds
    if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= num_rows or neighbor[1] >= num_cols:
        return False
        
    # If cell is blocked
    if maze[neighbor[0]][neighbor[1]] == "X":
        return False
    
    # If cell is already visited
    if visited[neighbor[0]][neighbor[1]]:
        return False

    # If not none of the above situations arise, the cell can be added!
    return True

def explore(cell: tuple, maze: list, visited: list, num_rows: int, num_cols: int) -> None:

    visited[cell[0]][cell[1]] = True

    x_delta = [1, 0, -1, 0]
    y_delta = [0, 1, 0, -1]

    for i in range(4):
        nb = (cell[0] + x_delta[i], cell[1] + y_delta[i])
        if valid_neighbor(nb, maze, visited, num_rows, num_cols):
            explore(nb, maze, visited, num_rows, num_cols)

init()

num_rows = 19
num_cols = 19

for x in range(5, 61, 5):
    maze = [["_" for _ in range(num_cols)] for _ in range(num_rows)] # We initialize the maze to be unblocked
    bad = True

    tries = 0

    while bad:

        tries += 1
        print("Try {} for {} percent case".format(tries, x))

        # Generate the blocked spaces in the maze
        create_walls(maze, x, num_rows, num_cols)

        first_cell = (0, 0) # by default
        found_blank = False

        for i in range(num_rows):
            for j in range(num_cols):
                if maze[i][j] == "_":
                    first_cell = (i, j)
                    found_blank = True
                    break
            if found_blank:
                break

        visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]

        # Check if the maze is legit using DFS
        explore(first_cell, maze, visited, num_rows, num_cols)

        bad = False

        for i in range(num_rows):
            for j in range(num_cols):
                if not visited[i][j] and maze[i][j] == "_":
                    bad = True
                    break
            if bad:
                # Re-initialize the maze to be unblocked
                for i in range(num_rows):
                    for j in range(num_cols):
                        maze[i][j] = "_"
                break

    display(maze, num_rows, num_cols)

    # Print the legit maze to a txt file
    save_txt("./reactor" + str(x) + ".txt", maze)

deinit()

# Finish!
