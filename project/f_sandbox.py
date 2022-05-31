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


EMPTY = 0
UP = 1
DOWN = 2
WALL = 3

states = [EMPTY, UP, DOWN]
NO = 0
YES = 1


grid = np.random.choice(states, (N+2)*N, p=[8/10, 1/10, 1/10]).reshape(N, N+2)

# walls
for i in range(N):
    grid[i][0] = WALL
    grid[i][-1] = WALL

# grid = np.zeros((N,N))
# grid[1][16] = UP
# grid[N-2][16] = DOWN
# print(grid)


newGrid = grid.copy()

t = 0

# print(grid)


def update(data):
    global grid
    global t
    global N

    grid_dimension = N


    # STATES #
    
    EMPTY = 0
    UP = 1
    DOWN = 2

    states = [EMPTY, UP, DOWN]
    NO = 0
    YES = 1

    PL11 = 0.1
    PR11 = 0.7
    PW11 = 0.2

    PR12 = 0.7
    PW12 = 0.3

    PL13 = 0.7
    PW13 = 0.3

    PL21 = 0.1
    PR21 = 0.7
    PW21 = 0.2

    PR22 = 0.9
    PW22 = 0.1

    PL23 = 0.9
    PW23 = 0.1

    PB = 0.6
    PW3 = 0.4


    WAIT = 0
    RIGHT = 1
    LEFT = 2
    BACK = 3
    directions = [WAIT, RIGHT, LEFT, BACK]


    newGrid = grid.copy()
    for i in range(N):
        
        for j in range(1,N+1):
            
            if grid[i][j] == UP:
                if grid[(i+1)%N][j] == EMPTY and newGrid[(i+1)%N][j] == EMPTY:
                    newGrid[(i+1)%N][j] = UP
                    newGrid[i][j] = EMPTY

                elif grid[(i+1)%N][j] == UP:
                    if grid[i][j-1] == EMPTY and grid[i][j+1] == EMPTY and newGrid[i][j-1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW11, PR11, PL11, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        elif direction == RIGHT:
                            newGrid[i][j+1] = UP
                            newGrid[i][j] = EMPTY
                        else: # elif direction == LEFT:
                            newGrid[i][j-1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[i][j+1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW12, PR12, 0, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else: # elif direction == RIGHT:
                            newGrid[i][j+1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[i][j-1] == EMPTY and newGrid[i][j-1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW13, 0, PL13, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else: # elif direction == LEFT:    
                            newGrid[i][j-1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[(i-1)%N][j] == EMPTY and newGrid[(i-1)%N][j] == EMPTY:
                        direction = np.random.choice(directions, p=[PW3, 0, 0, PB])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else:
                            newGrid[(i-1)%N][j] = UP
                            newGrid[i][j] = EMPTY
                    else:
                        newGrid[i][j] = UP


                elif grid[(i+1)%N][j] == DOWN:
                    if grid[i][j-1] == EMPTY and grid[i][j+1] == EMPTY and newGrid[i][j-1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW21, PR21, PL21, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        elif direction == RIGHT:
                            newGrid[i][j+1] = UP
                            newGrid[i][j] = EMPTY
                        else: # elif direction == LEFT:
                            newGrid[i][j-1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[i][j+1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW22, PR22, 0, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else: # elif direction == RIGHT:
                            newGrid[i][j+1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[i][j-1] == EMPTY and newGrid[i][j-1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW23, 0, PL23, 0])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else: # elif direction == LEFT:    
                            newGrid[i][j-1] = UP
                            newGrid[i][j] = EMPTY
                    elif grid[(i-1)%N][j] == EMPTY and newGrid[(i-1)%N][j] == EMPTY:
                        direction = np.random.choice(directions, p=[PW3, 0, 0, PB])
                        if direction == WAIT:
                            newGrid[i][j] = UP
                        else:
                            newGrid[(i-1)%N][j] = UP
                            newGrid[i][j] = EMPTY
                    else:
                        newGrid[i][j] = UP


            if grid[i][j] == DOWN:
                if grid[(i-1)%N][j] == EMPTY and newGrid[(i-1)%N][j] == EMPTY:
                    newGrid[(i-1)%N][j] = DOWN
                    newGrid[i][j] = EMPTY

                elif grid[(i-1)%N][j] == UP:
                    if grid[i][j-1] == EMPTY and grid[i][j+1] == EMPTY and newGrid[i][j-1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW11, PR11, PL11, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        elif direction == RIGHT:
                            newGrid[i][j-1] = DOWN
                            newGrid[i][j] = EMPTY
                        else: # elif direction == LEFT:
                            newGrid[i][j+1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[i][j-1] == EMPTY and newGrid[i][j-1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW12, PR12, 0, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else: # elif direction == RIGHT:
                            newGrid[i][j-1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[i][j+1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW13, 0, PL13, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else: # elif direction == LEFT:    
                            newGrid[i][j+1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[(i-1)%N][j] == EMPTY and newGrid[(i-1)%N][j] == EMPTY:
                        direction = np.random.choice(directions, p=[PW3, 0, 0, PB])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else:
                            newGrid[(i-1)%N][j] = DOWN
                            newGrid[i][j] = EMPTY
                    else:
                        newGrid[i][j] = DOWN


                elif grid[(i-1)%N][j] == DOWN:
                    if grid[i][j-1] == EMPTY and grid[i][j+1] == EMPTY and newGrid[i][j-1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW21, PR21, PL21, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        elif direction == RIGHT:
                            newGrid[i][j-1] = DOWN
                            newGrid[i][j] = EMPTY
                        else: # elif direction == LEFT:
                            newGrid[i][j-1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[i][j-1] == EMPTY and newGrid[i][j-1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW22, PR22, 0, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else: # elif direction == RIGHT:
                            newGrid[i][j-1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[i][j+1] == EMPTY and newGrid[i][j+1] == EMPTY:
                        direction = np.random.choice(directions, p=[PW23, 0, PL23, 0])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else: # elif direction == LEFT:    
                            newGrid[i][j+1] = DOWN
                            newGrid[i][j] = EMPTY
                    elif grid[(i-1)%N][j] == EMPTY and newGrid[(i-1)%N][j] == EMPTY:
                        direction = np.random.choice(directions, p=[PW3, 0, 0, PB])
                        if direction == WAIT:
                            newGrid[i][j] = DOWN
                        else:
                            newGrid[(i-1)%N][j] = DOWN
                            newGrid[i][j] = EMPTY
                    else:
                        newGrid[i][j] = DOWN

  
    # update data
    mat.set_data(newGrid)
    grid = newGrid
    print(grid.sum())
    plt.title(f't = {t}')
    t += 1

    


    return [mat]

# set up animation
fig, ax = plt.subplots()

# cmap = colors.ListedColormap(['green', 'black', 'yellow'])
cmap = colors.ListedColormap(['lightyellow', 'orange', 'olivedrab', 'black'])
# cmap = colors.ListedColormap(['tab:green', 'tab:blue', 'tab:orange'])
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(grid, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)

plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=states)

ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)

plt.show()
