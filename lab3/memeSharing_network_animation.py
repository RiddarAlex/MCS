#MoCS Lab1 3a. A INFECTED brain

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
SHARER = 3
RESTING = 2
BORED = 1
states = [RESTING, SHARER, BORED]
NO = 0
YES = 1

grid = [RESTING for i in range(N*N)]
grid[0], grid[1] = SHARER, BORED

grid = np.array(grid).reshape(N,N)
#print(grid)


newGrid = grid.copy()

t = 0


# np.set_printoptions(threshold=sys.maxsize)
# print(grid)


def update(data):
    global grid
    global t
    global N

    grid_dimension = N

    p = 0.1
    q = 0.5
    r = 0.1

    # p = 0.01
    # q = 0.05
    # r = 0.01

    # STATES #
    
    SHARER = 3
    RESTING = 2
    BORED = 1

    states = [RESTING, SHARER, BORED]
    NO = 0
    YES = 1

    neighbourhood = [0, 1, 2, 3, 5, 6, 7, 8]

    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
          
            #CHOOSE A NEIGHBOR
            target = random.choice(neighbourhood)

            y_target = (N + (j + target//3 - 1))%N
            x_target = (N + (i + target%3  - 1))%N

            ### APPLY RULES       
            if grid[i][j]  == RESTING:
                newGrid[i][j] = np.random.choice(states, p=[1-p, p, 0])

            elif grid[i][j]  == SHARER:
                will_share = np.random.choice([NO, YES], p=[1-q, q])
                if will_share == YES:
                    if grid[x_target][y_target] == RESTING:
                        newGrid[x_target][y_target] = SHARER
                    elif grid[x_target][y_target] == BORED:
                        newGrid[i][j] = BORED

            elif grid[i][j] == BORED:
                will_browse = np.random.choice([NO, YES], p=[1-r, r])
                if will_browse == YES:
                    if grid[x_target][y_target] == RESTING:
                        newGrid[i][j] = RESTING


    # update data
    mat.set_data(newGrid)
    grid = newGrid


    return [mat]

# set up animation
fig, ax = plt.subplots()

# cmap = colors.ListedColormap(['green', 'black', 'yellow'])
cmap = colors.ListedColormap(['orange', 'lightyellow', 'olivedrab'])
# cmap = colors.ListedColormap(['tab:green', 'tab:blue', 'tab:orange'])
bounds = [0.5,1.5,2.5,3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(grid, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)

plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=[BORED, RESTING, SHARER])

ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)

plt.show()
