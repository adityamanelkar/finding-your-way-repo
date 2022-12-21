import random
import numpy
from colorama import init
from colorama import deinit
from colorama import Fore
from itertools import product
from collections import deque
from copy import deepcopy
from read_map import read
from drone import Drone

filename = "./reactor.txt"
count = 0

maze = read(filename)
num_rows = len(maze)
num_cols = len(maze[0])

for row in range(num_rows):
    for col in range(num_cols):
        if maze[row][col] == "_":
            count += 1

# Question 1:
# Before you do anything, what is the probability that the drone is in the top left corner?
p_start = 1 / count
print("Probability of the drone being in the top-left at the start is: [{}]".format(p_start))
# Why?
print("Because the drone can be in only one of the white cells as mentioned by Dr. Cowan")

# Question 2:
# What are the locations where the drone is most likely to be? Least likely to be?
# How likely is it to be in all the other locations? Indicate your results visually.

# Note: Dr. Cowan asked us to visualize by considering only one timestep from start after moving "DOWN"

# Display for debugging
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

disp_maze = [[p_start for _ in range(num_cols)] for _ in range(num_rows)]

for row in range(num_rows):
    for col in range(num_cols):
        if maze[row][col] == "X":
            disp_maze[row][col] = -1

for row in range(num_rows - 1, -1, -1):
    for col in range(num_cols -1, -1, -1):
        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
            disp_maze[row + 1][col] += disp_maze[row][col]
            disp_maze[row][col] -= disp_maze[row][col]

init()

display(disp_maze, num_rows, num_cols)

deinit()

# # Go right 5 times
# for r in range(5):
#     for row in range(num_rows):
#         for col in range(num_cols):
#             if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
#                 disp_maze[row][col + 1] += disp_maze[row][col]
#                 disp_maze[row][col] -= disp_maze[row][col]


# # For action down 2 times
# for d in range(2):
#     for row in range(num_rows):
#         for col in range(num_cols):
#             if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
#                 disp_maze[row + 1][col] += disp_maze[row][col]
#                 disp_maze[row][col] -= disp_maze[row][col]


# # Go left 4 times
# for r in range(4):
#     for row in range(num_rows):
#         for col in range(num_cols):
#             if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
#                 disp_maze[row][col - 1] += disp_maze[row][col]
#                 disp_maze[row][col] -= disp_maze[row][col]

f = 0
in_loop = True
moves = 1

while in_loop:
    
    if f % 2 == 0:
        for j in range(f + 1):
            # Down
            for c in range(num_cols):
                moves += 1
                for row in range(num_rows):
                    for col in range(num_cols):
                        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                            disp_maze[row + 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Right
            for r in range(num_rows):
                moves += 1
                for col in range(num_cols):
                    for row in range(num_rows):
                        if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                            disp_maze[row][col + 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Up
            for c in range(num_cols):
                moves += 1
                for row in range(num_rows - 1, -1, -1):
                    for col in range(num_cols):
                        if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                            disp_maze[row - 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Left
            for r in range(num_rows):
                moves += 1
                for col in range(num_cols - 1, -1, -1):
                    for row in range(num_rows):
                        if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                            disp_maze[row][col - 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

    else:
        for j in range(f + 1):
            # Up
            for c in range(num_cols):
                moves += 1
                for row in range(num_rows - 1, -1, -1):
                    for col in range(num_cols):
                        if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
                            disp_maze[row - 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Right
            for r in range(num_rows):
                moves += 1
                for col in range(num_cols):
                    for row in range(num_rows):
                        if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
                            disp_maze[row][col + 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Down
            for c in range(num_cols):
                moves += 1
                for row in range(num_rows):
                    for col in range(num_cols):
                        if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
                            disp_maze[row + 1][col] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

            # Left
            for r in range(num_rows):
                moves += 1
                for col in range(num_cols - 1, -1, -1):
                    for row in range(num_rows):
                        if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
                            disp_maze[row][col - 1] += disp_maze[row][col]
                            disp_maze[row][col] -= disp_maze[row][col]

    f += 1

    # count = 0
    # for i in range(num_rows):
    #     for j in range(num_cols):
    #         if disp_maze[i][j] > 0:
    #             count += 1

    if numpy.amax(disp_maze) > 0.90:
        in_loop = False

print(f)
print(numpy.amax(disp_maze))
print(moves)

moves = ["UP", "DOWN", "LEFT", "RIGHT"]
steps = [i for i in range(1, 4)]

total = 0

# for i in range(300):
#     move = random.choice(moves)
#     num_steps = random.choice(steps)

#     if move == "UP":
#         # Up
#         for c in range(num_steps):
#             for row in range(num_rows - 1, -1, -1):
#                 for col in range(num_cols):
#                     if row - 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row - 1][col] > -1:
#                         disp_maze[row - 1][col] += disp_maze[row][col]
#                         disp_maze[row][col] -= disp_maze[row][col]

#     elif move == "RIGHT":
#         # Right
#         for r in range(num_steps):
#             for col in range(num_cols):
#                 for row in range(num_rows):
#                     if col + 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col + 1] > -1:
#                         disp_maze[row][col + 1] += disp_maze[row][col]
#                         disp_maze[row][col] -= disp_maze[row][col]

#     elif move == "DOWN":
#         # Down
#         for c in range(num_steps):
#             for row in range(num_rows):
#                 for col in range(num_cols):
#                     if row + 1 < num_rows and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row + 1][col] > -1:
#                         disp_maze[row + 1][col] += disp_maze[row][col]
#                         disp_maze[row][col] -= disp_maze[row][col]

#     elif move == "LEFT":
#         # Left
#         for r in range(num_steps):
#             for col in range(num_cols - 1, -1, -1):
#                 for row in range(num_rows):
#                     if col - 1 < num_cols and disp_maze[row][col] > 0 and disp_maze[row][col] != -1 and disp_maze[row][col - 1] > -1:
#                         disp_maze[row][col - 1] += disp_maze[row][col]
#                         disp_maze[row][col] -= disp_maze[row][col]

points = []

for i in range(num_rows):
    for j in range(num_cols):
        if disp_maze[i][j] > 0:
            points.append((i, j))

print(points)

init()

display(disp_maze, num_rows, num_cols)

deinit()

print("The cells in yellow indicate the most likely cells and those in red represent least likely cells!")

# # Question 3:

# def match_list(l1: list, l2: list) -> list:
#     """
#     Find some kind of alignment/matching between 2 lists
#     """
#     a = deepcopy(l1)
#     b = deepcopy(l2)

#     a = a[::-1]
#     b = b[::-1]

#     if len(a) == 0:
#         return b[::-1]
#     elif len(b) == 0:
#         return a[::-1]
#     else:
#         idx_a = len(a) - 1
#         idx_b = len(b) - 1

#         final = []

#         while idx_a > 0 or idx_b > 0:
#             if idx_a > 0 or idx_b > 0 and a[idx_a] == b[idx_b]:
#                 final.append(a[idx_a])
#                 idx_a -= 1
#                 idx_b -= 1
#             elif idx_a > 0:
#                 final.append(a[idx_a])
#                 idx_a -= 1
#             elif idx_b > 0:
#                 final.append(b[idx_b])
#                 idx_b -= 1
        
#         return final[::-1]

# def needleman_wunsch(x, y):
#     """
#     Run the Needleman-Wunsch algorithm on two sequences.

#     x, y -- sequences.

#     Code based on pseudocode in Section 3 of:

#     Naveed, Tahir; Siddiqui, Imitaz Saeed; Ahmed, Shaftab.
#     "Parallel Needleman-Wunsch Algorithm for Grid." n.d.
#     https://upload.wikimedia.org/wikipedia/en/c/c4/ParallelNeedlemanAlgorithm.pdf
#     """
#     N, M = len(x), len(y)
#     s = lambda a, b: int(a == b)

#     DIAG = -1, -1
#     LEFT = -1, 0
#     UP = 0, -1

#     # Create tables F and Ptr
#     F = {}
#     Ptr = {}

#     F[-1, -1] = 0
#     for i in range(N):
#         F[i, -1] = -i
#     for j in range(M):
#         F[-1, j] = -j

#     option_Ptr = DIAG, LEFT, UP
#     for i, j in product(range(N), range(M)):
#         option_F = (
#             F[i - 1, j - 1] + s(x[i], y[j]),
#             F[i - 1, j] - 1,
#             F[i, j - 1] - 1,
#         )
#         F[i, j], Ptr[i, j] = max(zip(option_F, option_Ptr))

#     # Work backwards from (N - 1, M - 1) to (0, 0)
#     # to find the best alignment.
#     alignment = deque()
#     i, j = N - 1, M - 1
#     while i >= 0 and j >= 0:
#         direction = Ptr[i, j]
#         if direction == DIAG:
#             element = i, j
#         elif direction == LEFT:
#             element = i, None
#         elif direction == UP:
#             element = None, j
#         alignment.appendleft(element)
#         di, dj = direction
#         i, j = i + di, j + dj
#     while i >= 0:
#         alignment.appendleft((i, None))
#         i -= 1
#     while j >= 0:
#         alignment.appendleft((None, j))
#         j -= 1

#     return list(alignment)

# def align_fast(x, y):
#     """
#     Align two sequences, maximizing the
#     alignment score, using the Needleman-Wunsch
#     algorithm.

#     x, y -- sequences.
#     """
#     return needleman_wunsch(x, y)

# def str_align(x, y, alignment):
#     l1 = ["-" if i is None else x[i] for i, _ in alignment]
#     l2 = ["-" if j is None else y[j] for _, j in alignment]

#     return l1, l2

# def merge_lists(x, y):
#     len_list = len(x)

#     merged = []

#     for idx in range(len_list):
#         if x[idx] == "-":
#             merged.append(y[idx])
#         elif y[idx] == "-":
#             merged.append(x[idx])
#         elif x[idx] == y[idx]:
#             merged.append(x[idx])
#         else:
#             merged.append(x[idx])

#     return merged

# # l1, l2 = str_align(["UP", "UP", "LEFT"], ["UP", "LEFT", "DOWN"], align_fast(["UP", "UP", "LEFT"], ["UP", "LEFT", "DOWN"]))

# # print("l1 = {}".format(l1))
# # print("l2 = {}".format(l2))

# rand_pos = (random.randint(0, num_rows - 1), random.randint(0, num_cols - 1))

# while maze[rand_pos[0]][rand_pos[0]] != "_":
#     rand_pos = (random.randint(0, num_rows - 1), random.randint(0, num_cols - 1))

# print("Random spawn for drone: {}".format(rand_pos))

# count = 0

# for row in range(num_rows - 1, -1, -1):
#     for col in range(num_cols - 1, -1, -1):
#         if maze[row][col] == "_":
#             dest = (row, col)
#             count += 1
#             break
#     if count > 0:
#         break

# print("White cell closest to top-left corner: {}".format(dest))

# d = Drone(rand_pos)
# d.calc_heuristics(maze, dest)

# # print(d.path)
# # print(d.action)
# # print(d.dist)

# actions = []

# for pos in d.action:
#     if pos in points:
#         actions.append(d.action[pos])

# print(actions)

# len_actions = len(actions)

# counter_moves = ["DOWN", "RIGHT", "UP", "LEFT"]
# clock_moves = ["UP", "RIGHT", "DOWN", "LEFT"]

# init_actions = []
# for f in range(7):
#     if f % 2 == 0:
#         for move in counter_moves:
#             for i in range(num_cols + 1):
#                 init_actions.append(move)
#     else:
#         for move in counter_moves:
#             for i in range(num_cols + 1):
#                 init_actions.append(move)

# common_actions = []
# cur_actions = []

# # print(merge_lists(l1, l2))
# print(common_actions)

# print("New common actions")

# for i in range(len_actions - 1, -1, -1):
#     cur_actions = actions[i]
#     l1, l2 = str_align(common_actions, cur_actions, align_fast(common_actions[::-1], cur_actions[::-1]))
#     common_actions = merge_lists(l1, l2)[::-1]
#     print(common_actions)

# init_actions.extend(common_actions)


# # print("init_actions = {}".format(init_actions))

# for action in init_actions:
#     d.move_drone(maze, action)

# print("Spawn point was: {}".format(rand_pos))
# print("Final point after set of actions was: {}".format((d.row, d.col)))
# print("Number of actions required were: {}".format(len(init_actions)))
# # print("List of actions required were: {}".format(init_actions))