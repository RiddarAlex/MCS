import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow
from random import randrange


from matplotlib import colors



N = 1000

# STATES #
RESTING = 2
SHARER = 3
BORED = 1

states = [RESTING, SHARER, BORED]
NO = 0
YES = 1

grid = [RESTING for i in range(N)]
grid[0], grid[1] = SHARER, BORED

grid = np.array(grid).reshape(25,40)
#print(grid)


newGrid = grid.copy()

t = 0

def update(data):
    global grid
    global t

    N = 1000
    p = 0.001
    q = 0.01
    r = 0.01

    # p = 0.01
    # q = 0.05
    # r = 0.01

    # STATES #
    RESTING = 2
    SHARER = 3
    BORED = 1

    states = [RESTING, SHARER, BORED]
    NO = 0
    YES = 1

    for i in range(25):
        for j in range(40):
            if grid[i][j]  == RESTING:
                newGrid[i][j] = np.random.choice(states, p=[1-p, p, 0])

            elif grid[i][j]  == SHARER:
                will_share = np.random.choice([NO, YES], p=[1-q, q])
                if will_share == YES:
                    target = randrange(N)
                    target_x = target//40
                    target_y = target%40
                    if grid[target_x][target_y] == RESTING:
                        newGrid[target_x][target_y] = SHARER
                    elif grid[target_x][target_y] == BORED:
                        newGrid[i][j] = BORED

            elif grid[i][j]  == BORED:
                will_browse = np.random.choice([NO, YES], p=[1-r, r])
                if will_browse == YES:
                    target = randrange(N)
                    target_x = target//40
                    target_y = target_x%25
                    if grid[target_x][target_y] == RESTING:
                        newGrid[i][j] = RESTING

     # update data
    mat.set_data(newGrid)
    grid = newGrid
    plt.title(f"Timestep = {t}")
    t = t+1


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
