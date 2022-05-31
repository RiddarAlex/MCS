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

counter = 0

N = 32

EMPTY = 1
UP = 2
DOWN = 3
WALL = 9999

states = [EMPTY, UP, DOWN]
NO = 0
YES = 1

grid = [EMPTY for i in range(N*N)]

grid = np.random.choice(states, (N,N+2), p=[0.9, 0.05, 0.05])
for i in range(N):
    grid[i][0], grid[i][-1] = WALL, WALL
# grid[0][N//2], grid[-1][N//2] = UP, DOWN

newGrid = grid.copy()

t = 0

# PROBABILITIES
PL11, PR11, PW11 = 0.25, 0.25, 0.5
PR12, PW12       = 0.5, 0.5
PL13, PW13       = 0.5, 0.5
PL21, PR21, PW21 = 0.25, 0.25, 0.5
PR22, PW22       = 0.5, 0.5
PL23, PW23       = 0.5, 0.5
PB  , PW3        = 0.5, 0.5





# np.set_printoptions(threshold=sys.maxsize)
# print(grid)


def update(data):

    # STATES #
    global EMPTY, UP, DOWN
    states = [EMPTY, UP, DOWN]

    # PROBABILITIES #
    global PL11, PR11, PW11, PR12, PW12, PL13, PW13, \
     PL21, PR21, PW21, PR22, PW22, PL23, PW23, PB, PW3

    # DOMAIN #
    global grid, t, N
    plt.title(f"t = {t}")
    t += 1
    newGrid = grid.copy()

    count = 0#N*N
    for i in range(N):
        for j in range(1,N+1):



            #CHOOSE A NEIGHBOR
            # target = random.choice(neighbourhood)

            # y_target = (N + (j + target//3 - 1))%N
            # x_target = (N + (i + target%3  - 1))%N

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

            count += 1

            if grid[forward] == EMPTY:
                if newGrid[forward] == EMPTY:
                    newGrid[forward] = myType
                    newGrid[current] = EMPTY

            elif (grid[forward] != EMPTY and grid[left] != EMPTY) and (grid[right] != EMPTY):
                choices = [backward, current]
                index = np.random.choice([0, 1], p=[PB, PW3])
                target = choices[index]

                if newGrid[target] == EMPTY:
                    newGrid[target] = myType
                    newGrid[current] = EMPTY

            elif grid[forward] == myType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    choices = [left, right, current]
                    index = np.random.choice([0, 1, 2], p=[PL11, PR11, PW11])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    choices = [right, current]
                    index = np.random.choice([0, 1], p=[PR12, PW12])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    choices = [left, current]
                    index = np.random.choice([0, 1], p=[PL13, PW13])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY



            elif grid[forward] == otherType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    choices = [left, right, current]
                    index = np.random.choice([0, 1, 2], p=[PL21, PR21, PW21])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    choices = [right, current]
                    index = np.random.choice([0, 1], p=[PR22, PW22])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    choices = [left, current]
                    index = np.random.choice([0, 1], p=[PL23, PW23])
                    target = choices[index]

                    if newGrid[target] == EMPTY:
                        newGrid[target] = myType
                        newGrid[current] = EMPTY

    # update data
    mat.set_data(newGrid)
    grid = newGrid

    print(f"Population size: {count}")
    return [mat]

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
