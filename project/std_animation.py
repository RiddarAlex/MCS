#MCS final project

import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow
import random
from random import randrange

N = 32

EMPTY, UP, DOWN, WALL = 1, 2, 3, 9999
states = [EMPTY, UP, DOWN]

grid = [EMPTY for i in range(N*N)]

grid = np.random.choice(states, (N,N+2), p=[0.80, 0.10, 0.10])
for i in range(N):
    grid[i][0], grid[i][-1] = WALL, WALL

newGrid = grid.copy()

t = 0
totalFlow = []

# PROBABILITIES
rPrefer = 1
L = (0.5 - 0.5*rPrefer)
R = (0.5 + 0.5*rPrefer)

neutral = 0.25
balance = (1-neutral)/2

PL11, PR11, PW11 = balance*(1 - rPrefer), balance*(1 + rPrefer), neutral
PR12, PW12       = R, 1 - R
PL13, PW13       = L, 1 - L
PL21, PR21, PW21 = balance*(1 - rPrefer), balance*(1 + rPrefer), neutral
PR22, PW22       = R, 1 - R
PL23, PW23       = L, 1 - L
PB  , PW3        = 0.5, 0.5

# rightPreference = 0.8
# twoOptions = (1 - rightPreference)
# threeOptions = (1 - rightPreference)/2
#
# PL11, PR11, PW11 = threeOptions, rightPreference, threeOptions
# PR12, PW12       = rightPreference, twoOptions
# PL13, PW13       = twoOptions, rightPreference
# PL21, PR21, PW21 = threeOptions, rightPreference, threeOptions
# PR22, PW22       = rightPreference, twoOptions
# PL23, PW23       = twoOptions, rightPreference
# PB  , PW3        = 0.5, 0.5

# PL11, PR11, PW11 = 0.25, 0.5, 0.25
# PR12, PW12       = 0.75, 0.25
# PL13, PW13       = 0.25, 0.75
# PL21, PR21, PW21 = 0.25, 0.5, 0.25
# PR22, PW22       = 0.75, 0.25
# PL23, PW23       = 0.25, 0.75
# PB  , PW3        = 0.5, 0.5

#-------------------------------------------------------------------------------
def update(data):

    global totalFlow
    currentFlow = 0

    # STATES #
    global EMPTY, UP, DOWN
    states = [EMPTY, UP, DOWN]

    # PROBABILITIES #
    global PL11, PR11, PW11, PR12, PW12, PL13, PW13, \
     PL21, PR21, PW21, PR22, PW22, PL23, PW23, PB, PW3

    # FUNCTION INPUT #
    global newGrid, myType, current

    # DOMAIN #
    global grid, t, N
    plt.title(f"t = {t}")
    newGrid = grid.copy()


    populationSize = 0#N*N
    for i in range(N):
        for j in range(1,N+1):

            ### APPLY RULES
            current = (i , j)

            if grid[current] == UP:
                myType = UP
                otherType = DOWN
                forward  = ((i + 1) % N     , j      )
                backward = ((N + i - 1) % N , j      )
                left     = (i               , (j - 1))
                right    = (i               , (j + 1))

            elif grid[current] == DOWN:
                myType = DOWN
                otherType = UP
                forward  = ((N + i - 1) % N , j      )
                backward = ((i + 1) % N     , j      )
                left     = (i               , (j + 1))
                right    = (i               , (j - 1))

            else:
                continue

            populationSize += 1

            if grid[forward] == EMPTY:
                if newGrid[forward] == EMPTY:
                    newGrid[forward] = myType
                    newGrid[current] = EMPTY
                    if ( (i == N-1) and (myType == UP) ) or ( (i == 0) and (myType == DOWN) ):
                        currentFlow += 1

            elif (grid[forward] != EMPTY and grid[left] != EMPTY) and (grid[right] != EMPTY):
                move_if_possible([backward, current], [PB, PW3])

            elif grid[forward] == myType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL11, PR11, PW11])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR12, PW12])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL13, PW13])


            elif grid[forward] == otherType or grid[forward] == MONSTER:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL21, PR21, PW21])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR22, PW22])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL23, PW23])




    # update data
    mat.set_data(newGrid)
    grid = newGrid

    totalFlow.append(currentFlow)
    if t%N == 0:
        print(f"t: {t} \tPopulation size: {populationSize}")
        if t != 0:
            flow = N*sum(totalFlow[t-31:t+1])/(populationSize*N)
            print(f"Flow: {flow}")
    print(f"Flow at t = {t}: {totalFlow[t]}")

    t += 1
    return [mat]

#-------------------------------------------------------------------------------
def move_if_possible(choices, probabilities):
    indices = [e for e in range(len(choices))]
    index = np.random.choice(indices, p=probabilities)
    target = choices[index]

    if newGrid[target] == EMPTY:
        newGrid[target] = myType
        newGrid[current] = EMPTY

#-------------------------------------------------------------------------------


# set up animation
fig, ax = plt.subplots()

# cmap = colors.ListedColormap(['green', 'black', 'yellow'])
cmap = colors.ListedColormap(['lightyellow', 'red', 'blue', 'black'])
# cmap = colors.ListedColormap(['tab:green', 'tab:blue', 'tab:orange'])
bounds = [0.5,1.5,2.5,3.5,10000]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(grid, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)

plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=states)

ani = animation.FuncAnimation(fig, update, interval=200,
                              save_count=50)

plt.show()


# #MCS final project
#
# import sys
# from matplotlib import colors
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib.colors import ListedColormap
# from matplotlib.pyplot import imshow
# import random
# from random import randrange
#
# counter = 0
#
# N = 32
#
# EMPTY = 1
# UP = 2
# DOWN = 3
# WALL = 9999
#
# states = [EMPTY, UP, DOWN]
# NO = 0
# YES = 1
#
# grid = [EMPTY for i in range(N*N)]
#
# grid = np.random.choice(states, (N,N+2), p=[0.8, 0.1, 0.1])
# for i in range(N):
#     grid[i][0], grid[i][-1] = WALL, WALL
# # grid[0][N//2], grid[-1][N//2] = UP, DOWN
#
# newGrid = grid.copy()
#
# t = 0
#
# # PROBABILITIES
# PL11, PR11, PW11 = 0.25, 0.5, 0.25
# PR12, PW12       = 0.75, 0.25
# PL13, PW13       = 0.25, 0.75
# PL21, PR21, PW21 = 0.25, 0.5, 0.25
# PR22, PW22       = 0.75, 0.25
# PL23, PW23       = 0.25, 0.75
# PB  , PW3        = 0.5, 0.5
#
#
#
#
#
# # np.set_printoptions(threshold=sys.maxsize)
# # print(grid)
#
#
# def update(data):
#
#     # STATES #
#     global EMPTY, UP, DOWN
#     states = [EMPTY, UP, DOWN]
#
#     # PROBABILITIES #
#     global PL11, PR11, PW11, PR12, PW12, PL13, PW13, \
#      PL21, PR21, PW21, PR22, PW22, PL23, PW23, PB, PW3
#
#     # DOMAIN #
#     global grid, t, N
#     plt.title(f"t = {t}")
#     t += 1
#     newGrid = grid.copy()
#
#     count = 0#N*N
#     for i in range(N):
#         for j in range(1,N+1):
#
#
#
#             #CHOOSE A NEIGHBOR
#             # target = random.choice(neighbourhood)
#
#             # y_target = (N + (j + target//3 - 1))%N
#             # x_target = (N + (i + target%3  - 1))%N
#
#             ### APPLY RULES
#             current = (i , j)
#
#             if grid[current] == UP:
#                 myType = UP
#                 otherType = DOWN
#                 forward  = ((i + 1) % N     , j      )
#                 backward = ((N + i - 1) % N , j      )
#                 left     = (i               , (j - 1))
#                 right    = (i               , (j + 1))
#
#             elif grid[current] == DOWN:
#                 myType = DOWN
#                 otherType = UP
#                 forward  = ((N + i - 1) % N , j      )
#                 backward = ((i + 1) % N     , j      )
#                 left     = (i               , (j + 1))
#                 right    = (i               , (j - 1))
#             else:
#                 continue
#
#             count += 1
#
#             if grid[forward] == EMPTY:
#                 if newGrid[forward] == EMPTY:
#                     newGrid[forward] = myType
#                     newGrid[current] = EMPTY
#
#             elif (grid[forward] != EMPTY and grid[left] != EMPTY) and (grid[right] != EMPTY):
#                 choices = [backward, current]
#                 index = np.random.choice([0, 1], p=[PB, PW3])
#                 target = choices[index]
#
#                 if newGrid[target] == EMPTY:
#                     newGrid[target] = myType
#                     newGrid[current] = EMPTY
#
#             elif grid[forward] == myType:
#
#                 if (grid[left] == EMPTY) and (grid[right] == EMPTY):
#                     choices = [left, right, current]
#                     index = np.random.choice([0, 1, 2], p=[PL11, PR11, PW11])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#                 elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
#                     choices = [right, current]
#                     index = np.random.choice([0, 1], p=[PR12, PW12])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#                 elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
#                     choices = [left, current]
#                     index = np.random.choice([0, 1], p=[PL13, PW13])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#
#
#             elif grid[forward] == otherType:
#
#                 if (grid[left] == EMPTY) and (grid[right] == EMPTY):
#                     choices = [left, right, current]
#                     index = np.random.choice([0, 1, 2], p=[PL21, PR21, PW21])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#                 elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
#                     choices = [right, current]
#                     index = np.random.choice([0, 1], p=[PR22, PW22])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#                 elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
#                     choices = [left, current]
#                     index = np.random.choice([0, 1], p=[PL23, PW23])
#                     target = choices[index]
#
#                     if newGrid[target] == EMPTY:
#                         newGrid[target] = myType
#                         newGrid[current] = EMPTY
#
#     # update data
#     mat.set_data(newGrid)
#     grid = newGrid
#     if t%25 == 0:
#         print(f"t: {t} \tPopulation size: {count}")
#     return [mat]
#
# # set up animation
# fig, ax = plt.subplots()
#
# # cmap = colors.ListedColormap(['green', 'black', 'yellow'])
# cmap = colors.ListedColormap(['lightyellow', 'red', 'blue', 'black'])
# # cmap = colors.ListedColormap(['tab:green', 'tab:blue', 'tab:orange'])
# bounds = [0.5,1.5,2.5,3.5,10000]
# norm = colors.BoundaryNorm(bounds, cmap.N)
# mat = plt.imshow(grid, interpolation='nearest', origin='lower',
#                     cmap=cmap, norm=norm)
#
# plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=states)
#
# ani = animation.FuncAnimation(fig, update, interval=200,
#                               save_count=50)
#
# plt.show()
