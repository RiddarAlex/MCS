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

EMPTY, UP, DOWN, RANDOM,  WALL = 1, 2, 3, 4, 9999
states = [EMPTY, UP, DOWN, RANDOM]

grid = [EMPTY for i in range(N*N)]

grid = np.random.choice(states, (N,N+2), p=[0.79, 0.1, 0.1, 0.01])
for i in range(N):
    grid[i][0], grid[i][-1] = WALL, WALL

# grid[16][16] = RANDOM

newGrid = grid.copy()

t = 0

# PROBABILITIES
PL11, PR11, PW11 = 0.25, 0.5, 0.25
PR12, PW12       = 0.75, 0.25
PL13, PW13       = 0.25, 0.75
PL21, PR21, PW21 = 0.25, 0.5, 0.25
PR22, PW22       = 0.75, 0.25
PL23, PW23       = 0.25, 0.75
PB  , PW3        = 0.5, 0.5

#-------------------------------------------------------------------------------
def update(data):

    # STATES #
    global EMPTY, UP, DOWN, RANDOM
    states = [EMPTY, UP, DOWN, RANDOM]

    # PROBABILITIES #
    global PL11, PR11, PW11, PR12, PW12, PL13, PW13, \
     PL21, PR21, PW21, PR22, PW22, PL23, PW23, PB, PW3

    # FUNCTION INPUT #
    global newGrid, myType, current

    # DOMAIN #
    global grid, t, N
    plt.title(f"t = {t}")
    t += 1
    newGrid = grid.copy()

    monsterMoves = []

    count = 0#N*N
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

            elif grid[current] == RANDOM:
                y_direction = np.random.choice([-1, 0, 1])
                x_direction = np.random.choice([-1, 0, 1])

                randomTarget = ((i + y_direction)%N, j + x_direction)
                if grid[randomTarget] == EMPTY and newGrid[randomTarget] == EMPTY:
                    newGrid[randomTarget] = RANDOM
                    newGrid[current] = EMPTY
                else:
                    newGrid[current] = RANDOM
                continue
            else:
                continue

            count += 1

            if grid[forward] == EMPTY:
                if newGrid[forward] == EMPTY:
                    newGrid[forward] = myType
                    newGrid[current] = EMPTY

            elif (grid[forward] != EMPTY and grid[left] != EMPTY) and (grid[right] != EMPTY):
                move_if_possible([backward, current], [PB, PW3])

            elif grid[forward] == myType or grid[forward] == RANDOM:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL11, PR11, PW11])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR12, PW12])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL13, PW13])


            elif grid[forward] == otherType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL21, PR21, PW21])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR22, PW22])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL23, PW23])

    # update data
    mat.set_data(newGrid)
    grid = newGrid
    if t%25 == 0:
        print(f"t: {t} \tPopulation size: {count}")

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

cmap = colors.ListedColormap(['lightyellow', 'red', 'blue', 'green', 'black'])
bounds = [0.5,1.5,2.5,3.5,4.5,10000]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(grid, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)

plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=states)

ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)

plt.show()
