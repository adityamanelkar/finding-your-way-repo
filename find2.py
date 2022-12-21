import random
import numpy
import time
from colorama import init
from colorama import deinit
from colorama import Fore
from itertools import product
from collections import deque
from copy import deepcopy
from read_map import read
from drone import Drone

start_time = time.time()

filename = "./reactor.txt"
count = 0

maze = read(filename)
num_rows = len(maze)
num_cols = len(maze[0])

for row in range(num_rows):
    for col in range(num_cols):
        if maze[row][col] == "_":
            count += 1

# Display for debugging the maze
def display(maze: list, num_rows: int, num_cols: int) -> None:
    for row in range(num_rows):
        for col in range(num_cols):
            if (maze[row][col] == p_start):
                print(Fore.WHITE + str("N"), end=" ")
            elif (maze[row][col] == 0):
                print(Fore.RED + str("L"), end=" ")
            elif (maze[row][col] > p_start):
                print(Fore.YELLOW + str("H"), end=" ")
            elif (maze[row][col] == -1):
                print(Fore.BLACK + str("X"), end=" ")
        print("\n")

init()

#############
# Question 1:
#############

# Before you do anything, what is the probability that the drone is in the top left corner?
print(Fore.GREEN + "\nQUESTION 1\n")
p_start = 1 / count
print(Fore.YELLOW + "Probability of the drone being in the top-left at the start is: [{}].".format(p_start))
# Why?
print(Fore.YELLOW + "WHY? -> Because the drone can be in any one of the white cells at the start.\n")

disp_maze = [[p_start for _ in range(num_cols)] for _ in range(num_rows)]

for row in range(num_rows):
    for col in range(num_cols):
        if maze[row][col] == "X":
            disp_maze[row][col] = -1

print(Fore.WHITE + "Following is a representation of the maze (by probability distribution where N means original distribution and X is used for walls):\n")

display(disp_maze, num_rows, num_cols)

#############
# Question 2:
#############

# What are the locations where the drone is most likely to be? Least likely to be?
# How likely is it to be in all the other locations? Indicate your results visually.

# Note: Dr. Cowan asked us to visualize by considering only one timestep from start after moving "DOWN"

print(Fore.GREEN + "\nQUESTION 2\n")

print(Fore.WHITE + "Following is a representation of the maze (by probability distribution where N and X have the same meanings as from the previous graph, and L indicates the probability falling to 0 and H indicates a higher probability than N in general):\n")

for row in range(num_rows - 1, -1, -1):
    for col in range(num_cols -1, -1, -1):
        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
            disp_maze[row + 1][col] += disp_maze[row][col]
            disp_maze[row][col] -= disp_maze[row][col]

display(disp_maze, num_rows, num_cols)

#############
# Question 3:
#############

print(Fore.GREEN + "\nQUESTION 3\n")

f = 0
in_loop = True
moves = 0

factor = 20 # This determines up until how many clusters do we want to repeat the wasteful approach

actions = []

# MARCH PHASE

while in_loop:
    
    if f % 2 == 0:
        for j in range(1):
            # Down
            for c in range(num_rows):
                moves += 1
                actions.append("DOWN")
                for row in range(num_rows - 1, -1, -1):
                    for col in range(num_cols):
                        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                            disp_maze[row + 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Right
            for r in range(num_cols):
                moves += 1
                actions.append("RIGHT")
                for col in range(num_cols - 1, -1, -1):
                    for row in range(num_rows):
                        if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                            disp_maze[row][col + 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Up
            for c in range(num_rows):
                moves += 1
                actions.append("UP")
                for row in range(num_rows):
                    for col in range(num_cols):
                        if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                            disp_maze[row - 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Left
            for r in range(num_cols):
                moves += 1
                actions.append("LEFT")
                for col in range(num_cols):
                    for row in range(num_rows):
                        if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                            disp_maze[row][col - 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

    else:
        for j in range(1):
            # Up
            for c in range(num_rows):
                moves += 1
                actions.append("UP")
                for row in range(num_rows):
                    for col in range(num_cols):
                        if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                            disp_maze[row - 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Right
            for r in range(num_cols):
                moves += 1
                actions.append("RIGHT")
                for col in range(num_cols - 1, -1, -1):
                    for row in range(num_rows):
                        if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                            disp_maze[row][col + 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Down
            for c in range(num_rows):
                moves += 1
                actions.append("DOWN")
                for row in range(num_rows - 1, -1, -1):
                    for col in range(num_cols):
                        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                            disp_maze[row + 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Left
            for r in range(num_cols):
                moves += 1
                actions.append("LEFT")
                for col in range(num_cols):
                    for row in range(num_rows):
                        if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                            disp_maze[row][col - 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

    f += 1

    count = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if disp_maze[i][j] > 0:
                count += 1

    if count < factor:
        in_loop = False

print(Fore.WHITE + "Upon using the slightly wasteful approach, the code reached the following distribution in {} moves:\n".format(moves))

display(disp_maze, num_rows, num_cols)

# print(len(actions))
# print(actions)

# We then want to make sure the clusters in possible positions with non-zero probabilities do converge
# We will do so by simply using shortest path and trying to make one of them "catch" the other

# HUNT PHASE

points = []

for i in range(num_rows):
    for j in range(num_cols):
        if disp_maze[i][j] > 0:
            points.append((i, j))

print(Fore.WHITE + "The cells with the non-zero probabilities are: {}\n".format(points))

drones = [Drone(str(i), points[i]) for i in range(len(points))]

for i in range(1, len(drones)):

    conv_actions = []
    caught = False
    t = 0

    print("Converging Drone 0 and Drone {}".format(i))

    # We use drones[0] as the reference drone that we want to use to calculate heuristics and converge with other drones
    while (drones[0].row, drones[0].col) != (drones[i].row, drones[i].col) and not caught and t < 10000:

        t += 1

        drones[0].calc_heuristics(maze, (drones[i].row, drones[i].col))
        move = list(drones[0].action[(drones[0].row, drones[0].col)])[0]
        # print(move)

        conv_actions.append(move)

        # Move all drones including drones
        for j in range(len(drones)):
            drones[j].move_drone(maze, move)

        # drones[0].move_drone(maze, move)
        # drones[i].move_drone(maze, move)

        # print((drones[0].row, drones[0].col))
        # print((drones[i].row, drones[i].col))

        if move == "UP":
            # Up
            for row in range(num_rows):
                for col in range(num_cols):
                    if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                        disp_maze[row - 1][col] += disp_maze[row][col]
                        disp_maze[row][col] -= disp_maze[row][col]

        elif move == "RIGHT":
            # Right
            for col in range(num_cols - 1, -1, -1):
                for row in range(num_rows):
                    if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                        disp_maze[row][col + 1] += disp_maze[row][col]
                        disp_maze[row][col] -= disp_maze[row][col]

        elif move == "DOWN":
            # Down
            for row in range(num_rows - 1, -1, -1):
                for col in range(num_cols):
                    if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                        disp_maze[row + 1][col] += disp_maze[row][col]
                        disp_maze[row][col] -= disp_maze[row][col]

        elif move == "LEFT":
            # Left
            for col in range(num_cols):
                for row in range(num_rows):
                    if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                        disp_maze[row][col - 1] += disp_maze[row][col]
                        disp_maze[row][col] -= disp_maze[row][col]

        if drones[0].row == drones[i].row and drones[0].col == drones[i].col:
            # print("Here {}".format(t))
            caught = True

    actions.extend(conv_actions)
    moves = len(actions)

    print(conv_actions)
    print(len(conv_actions))

points = []

for i in range(num_rows):
    for j in range(num_cols):
        if disp_maze[i][j] > 0:
            points.append((i, j))

print(Fore.WHITE + "The cells with the non-zero probabilities are: {}\n".format(points))

if len(points) > 1:

    drones = [Drone(str(i), points[i]) for i in range(len(points))]

    for i in range(1, len(drones)):

        conv_actions = []
        caught = False
        t = 0

        print("Converging Drone 0 and Drone {}".format(i))

        # We use drones[0] as the reference drone that we want to use to calculate heuristics and converge with other drones
        while (drones[0].row, drones[0].col) != (drones[i].row, drones[i].col) and not caught and t < 10000:

            t += 1

            drones[0].calc_heuristics(maze, (drones[i].row, drones[i].col))
            move = list(drones[0].action[(drones[0].row, drones[0].col)])[0]
            # print(move)

            conv_actions.append(move)

            # Move all drones including drones
            for j in range(len(drones)):
                drones[j].move_drone(maze, move)

            # drones[0].move_drone(maze, move)
            # drones[i].move_drone(maze, move)

            # print((drones[0].row, drones[0].col))
            # print((drones[i].row, drones[i].col))

            if move == "UP":
                # Up
                for row in range(num_rows):
                    for col in range(num_cols):
                        if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                            disp_maze[row - 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            elif move == "RIGHT":
                # Right
                for col in range(num_cols - 1, -1, -1):
                    for row in range(num_rows):
                        if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                            disp_maze[row][col + 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            elif move == "DOWN":
                # Down
                for row in range(num_rows - 1, -1, -1):
                    for col in range(num_cols):
                        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                            disp_maze[row + 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            elif move == "LEFT":
                # Left
                for col in range(num_cols):
                    for row in range(num_rows):
                        if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                            disp_maze[row][col - 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            if drones[0].row == drones[i].row and drones[0].col == drones[i].col:
                # print("Here {}".format(t))
                caught = True

        actions.extend(conv_actions)
        moves = len(actions)

        print(conv_actions)
        print(len(conv_actions))

print(Fore.WHITE + "Upon using the shortest path approach, the code could converge to one cell with max beleief in {} moves:\n".format(len(conv_actions)))

display(disp_maze, num_rows, num_cols)

max = disp_maze[drones[0].row][drones[0].col]
pos = (drones[0].row, drones[0].col)

for i in range(num_rows):
    for j in range(num_cols):
        if disp_maze[i][j] > 0:
            print("({}, {}) ".format(i, j))

print(Fore.WHITE + "The code could find the following:")
print(Fore.YELLOW + "It took the code {} moves to find the exact position {} of the drone with {} percent certaintly:".format(moves, pos, max * 100))
print(Fore.YELLOW + "\nThe actions the code took to achieve it are:\n{}".format(actions))

#############
# Question 4:
#############

print(Fore.GREEN + "\nQUESTION 4\n")

max_moves = 0
max_moves_maze_num = 0

for num in range(5, 41, 5):

    # filename = "./reactor_aravind" + ".txt"
    filename = "./reactor" + str(num) + ".txt"
    count = 0

    maze = read(filename)
    num_rows = len(maze)
    num_cols = len(maze[0])

    for row in range(num_rows):
        for col in range(num_cols):
            if maze[row][col] == "_":
                count += 1

    p_start = 1 / count

    disp_maze = [[p_start for _ in range(num_cols)] for _ in range(num_rows)]

    for row in range(num_rows):
        for col in range(num_cols):
            if maze[row][col] == "X":
                disp_maze[row][col] = -1

    f = 0
    in_loop = True
    moves = 0

    factor = 20 # This determines up until how many clusters do we want to repeat the wasteful approach

    actions = []

    while in_loop:
        
        if f % 2 == 0:
            for j in range(1):
                # Down
                for c in range(num_rows):
                    moves += 1
                    actions.append("DOWN")
                    for row in range(num_rows - 1, -1, -1):
                        for col in range(num_cols):
                            if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                                disp_maze[row + 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Right
                for r in range(num_cols):
                    moves += 1
                    actions.append("RIGHT")
                    for col in range(num_cols - 1, -1, -1):
                        for row in range(num_rows):
                            if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                                disp_maze[row][col + 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Up
                for c in range(num_rows):
                    moves += 1
                    actions.append("UP")
                    for row in range(num_rows):
                        for col in range(num_cols):
                            if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                                disp_maze[row - 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Left
                for r in range(num_cols):
                    moves += 1
                    actions.append("LEFT")
                    for col in range(num_cols):
                        for row in range(num_rows):
                            if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                                disp_maze[row][col - 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

        else:
            for j in range(1):
                # Up
                for c in range(num_rows):
                    moves += 1
                    actions.append("UP")
                    for row in range(num_rows):
                        for col in range(num_cols):
                            if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                                disp_maze[row - 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Right
                for r in range(num_cols):
                    moves += 1
                    actions.append("RIGHT")
                    for col in range(num_cols - 1, -1, -1):
                        for row in range(num_rows):
                            if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                                disp_maze[row][col + 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Down
                for c in range(num_rows):
                    moves += 1
                    actions.append("DOWN")
                    for row in range(num_rows - 1, -1, -1):
                        for col in range(num_cols):
                            if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                                disp_maze[row + 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                # Left
                for r in range(num_cols):
                    moves += 1
                    actions.append("LEFT")
                    for col in range(num_cols):
                        for row in range(num_rows):
                            if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                                disp_maze[row][col - 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

        f += 1

        count = 0
        for i in range(num_rows):
            for j in range(num_cols):
                if disp_maze[i][j] > 0:
                    count += 1

        if count < factor:
            in_loop = False

    points = []

    for i in range(num_rows):
        for j in range(num_cols):
            if disp_maze[i][j] > 0:
                points.append((i, j))

    if len(points) == 1:
        moves = len(actions)
        max = disp_maze[points[0][0]][points[0][1]]
        pos = (points[0][0], points[0][1])

        if max > max_moves:
            max_moves = moves
            max_moves_maze_num = num

        print(Fore.YELLOW + "\nThe number of moves the code took to find the position {} for maze with {} percent walls are: {}".format(pos, num, moves))

    else:
        drones = [Drone(str(i), points[i]) for i in range(len(points))]

        for i in range(1, len(drones)):

            conv_actions = []
            caught = False
            t = 0

            # print("Converging Drone 0 and Drone {}".format(i))

            while (drones[0].row, drones[0].col) != (drones[i].row, drones[i].col) and not caught and t < 10000:

                t += 1

                drones[0].calc_heuristics(maze, (drones[i].row, drones[i].col))
                move = list(drones[0].action[(drones[0].row, drones[0].col)])[0]
                # print(move)

                conv_actions.append(move)

                # Move all drones including drones
                for j in range(len(drones)):
                    drones[j].move_drone(maze, move)

                # drones[0].move_drone(maze, move)
                # drones[i].move_drone(maze, move)

                # print((drones[0].row, drones[0].col))
                # print((drones[i].row, drones[i].col))

                if move == "UP":
                    # Up
                    for row in range(num_rows):
                        for col in range(num_cols):
                            if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                                disp_maze[row - 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                elif move == "RIGHT":
                    # Right
                    for col in range(num_cols - 1, -1, -1):
                        for row in range(num_rows):
                            if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                                disp_maze[row][col + 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                elif move == "DOWN":
                    # Down
                    for row in range(num_rows - 1, -1, -1):
                        for col in range(num_cols):
                            if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                                disp_maze[row + 1][col] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                elif move == "LEFT":
                    # Left
                    for col in range(num_cols):
                        for row in range(num_rows):
                            if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                                disp_maze[row][col - 1] += disp_maze[row][col]
                                disp_maze[row][col] -= disp_maze[row][col]

                if drones[0].row == drones[i].row and drones[0].col == drones[i].col:
                    # print("Here {}".format(t))
                    caught = True

            actions.extend(conv_actions)
            moves = len(actions)

            # print(conv_actions)
            # print(len(conv_actions))

        points = []

        for i in range(num_rows):
            for j in range(num_cols):
                if disp_maze[i][j] > 0:
                    points.append((i, j))

        # print(Fore.WHITE + "The cells with the non-zero probabilities are: {}\n".format(points))

        if len(points) > 1:

            drones = [Drone(str(i), points[i]) for i in range(len(points))]

            for i in range(1, len(drones)):

                conv_actions = []
                caught = False
                t = 0

                # print("Converging Drone 0 and Drone {}".format(i))

                # We use drones[0] as the reference drone that we want to use to calculate heuristics and converge with other drones
                while (drones[0].row, drones[0].col) != (drones[i].row, drones[i].col) and not caught and t < 10000:

                    t += 1

                    drones[0].calc_heuristics(maze, (drones[i].row, drones[i].col))
                    move = list(drones[0].action[(drones[0].row, drones[0].col)])[0]
                    # print(move)

                    conv_actions.append(move)

                    # Move all drones including drones
                    for j in range(len(drones)):
                        drones[j].move_drone(maze, move)

                    # drones[0].move_drone(maze, move)
                    # drones[i].move_drone(maze, move)

                    # print((drones[0].row, drones[0].col))
                    # print((drones[i].row, drones[i].col))

                    if move == "UP":
                        # Up
                        for row in range(num_rows):
                            for col in range(num_cols):
                                if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                                    disp_maze[row - 1][col] += disp_maze[row][col]
                                    disp_maze[row][col] -= disp_maze[row][col]

                    elif move == "RIGHT":
                        # Right
                        for col in range(num_cols - 1, -1, -1):
                            for row in range(num_rows):
                                if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                                    disp_maze[row][col + 1] += disp_maze[row][col]
                                    disp_maze[row][col] -= disp_maze[row][col]

                    elif move == "DOWN":
                        # Down
                        for row in range(num_rows - 1, -1, -1):
                            for col in range(num_cols):
                                if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                                    disp_maze[row + 1][col] += disp_maze[row][col]
                                    disp_maze[row][col] -= disp_maze[row][col]

                    elif move == "LEFT":
                        # Left
                        for col in range(num_cols):
                            for row in range(num_rows):
                                if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                                    disp_maze[row][col - 1] += disp_maze[row][col]
                                    disp_maze[row][col] -= disp_maze[row][col]

                    if drones[0].row == drones[i].row and drones[0].col == drones[i].col:
                        # print("Here {}".format(t))
                        caught = True

                actions.extend(conv_actions)
                moves = len(actions)

                # print(conv_actions)
                # print(len(conv_actions))

        max = disp_maze[drones[0].row][drones[0].col]
        pos = (drones[0].row, drones[0].col)

        if moves > max_moves:
            max_moves = moves
            max_moves_maze_num = num

        print(Fore.YELLOW + "\nThe number of moves the code took to find the position {} for maze with {} percent walls are: {}".format(pos, num, moves))

print(Fore.RED + "\nreactor{}.txt".format(max_moves_maze_num) + Fore.YELLOW + " is the maze that challenges the algorithm the most with {} moves required to solve!\n".format(max_moves))

deinit()

print("Total time taken by the code to execute was: {} seconds".format(time.time() - start_time))


######################################
## IGNORE THE BELOW COMMENTED CODES ~
######################################

## Trying something for Global Search convergence
## But it does not seem to be working as of now

# class State:
#     def __init__(self, maze: list) -> None:
#         self.start = maze
#         self.cur = maze
#         self.map = {}
#         self.prev = {}
#         self.prev_move = {}
#         self.visited = {}
#         self.num_rows = len(maze)
#         self.num_cols = len(maze[0])
#         self.count = 0

#         self.map[self.count] = self.start

#     def neighbors(self) -> list:
#         nb = []

#         cur = deepcopy(self.count)

#         # DOWN
#         for row in range(self.num_rows):
#             for col in range(self.num_cols):
#                 nb_maze = deepcopy(self.cur)
#                 if row + 1 < num_rows and nb_maze[row][col] > 0 and nb_maze[row][col] != -1 and nb_maze[row + 1][col] > -1:
#                     nb_maze[row + 1][col] += nb_maze[row][col]
#                     nb_maze[row][col] -= nb_maze[row][col]

#         self.count += 1
#         self.map[self.count] = nb_maze
#         self.prev[count] = cur
#         self.prev_move[count] = "DOWN"

#         nb.append(self.count)

#         # RIGHT
#         for row in range(self.num_cols - 1, -1, -1):
#             for col in range(self.num_rows):
#                 nb_maze = deepcopy(self.cur)
#                 if col + 1 < num_cols and nb_maze[row][col] > 0 and nb_maze[row][col] != -1 and nb_maze[row][col + 1] > -1:
#                     nb_maze[row][col + 1] += nb_maze[row][col]
#                     nb_maze[row][col] -= nb_maze[row][col]

#         self.count += 1
#         self.map[self.count] = nb_maze
#         self.prev[count] = cur
#         self.prev_move[count] = "RIGHT"

#         nb.append(self.count)

#         # UP
#         for row in range(self.num_rows):
#             for col in range(self.num_cols):
#                 nb_maze = deepcopy(self.cur)
#                 if row - 1 < num_rows and nb_maze[row][col] > 0 and nb_maze[row][col] != -1 and nb_maze[row - 1][col] > -1:
#                     nb_maze[row - 1][col] += nb_maze[row][col]
#                     nb_maze[row][col] -= nb_maze[row][col]

#         self.count += 1
#         self.map[self.count] = nb_maze
#         self.prev[count] = cur
#         self.prev_move[count] = "UP"

#         nb.append(self.count)

#         # LEFT
#         for row in range(self.num_cols):
#             for col in range(self.num_rows):
#                 nb_maze = deepcopy(self.cur)
#                 if col - 1 < num_cols and nb_maze[row][col] > 0 and nb_maze[row][col] != -1 and nb_maze[row][col - 1] > -1:
#                     nb_maze[row][col - 1] += nb_maze[row][col]
#                     nb_maze[row][col] -= nb_maze[row][col]

#         self.count += 1
#         self.map[self.count] = nb_maze
#         self.prev[count] = cur
#         self.prev_move[count] = "LEFT"

#         nb.append(self.count)

#         return nb

#     def create_actions(self, maze: list) -> list:
#         """
#         Creates the action list to follow a path
#         """
#         for key in self.map:
#             if self.map[key] == maze:
#                 k = key
#                 break

#         actions = []

#         while k in list(self.prev):
#             action = self.prev_move[k]
#             actions.append(action)
#             k = self.prev[k]

#         return actions[::-1]

#     def find(self, goal: list) -> list:
#         """
#         Returns list of actions taken to find goal from start (algo is based on BFS)
#         """
#         queue = []
#         action_list = []

#         self.visited[self.count] = True
#         queue.append(self.start)

#         t = 1

#         while queue and t < 10000:
#             self.cur = queue.pop(0)
#             print("Term {} in ".format(t))

#             if self.cur == goal:
#                 action_list = self.create_actions(goal)
#                 return action_list

#             for key in self.neighbors():
#                 if key not in self.visited:
#                     self.visited[key] = True
#                     queue.append(self.map[key])

#             t += 1

#         if t >= 10000:
#             print("BFS timed out due to large search space")
#             return action_list
#         else:
#             print("Some unknown error occurred")
#             return action_list

# goal_maze = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]

# goal_maze[num_rows - 1][num_cols - 1] = 1.0

# s = State(disp_maze)
# converge_actions = s.find(goal_maze)

# disp_maze = s.cur

# display(disp_maze, num_rows, num_cols)

# print(len(converge_actions))
# print(converge_actions)