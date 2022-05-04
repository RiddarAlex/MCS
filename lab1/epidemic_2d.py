#MoCS Lab1 3a. A INFECTED brain

import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow

counter = 0

N = 100
INFECTED = 255
SUSCEPTIBLE = 25
RECOVERED = 0
vals = [INFECTED, SUSCEPTIBLE, RECOVERED]


# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=[0.001, 1-0.001, 0.0]).reshape(N, N)



# np.set_printoptions(threshold=sys.maxsize)
# print(grid)


def update(data):
    global grid
    global counter
    #if counter == 1000: fig.savefig(f'A_INFECTED_Brain_Frame{counter}.png')
    counter += 1
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line

    alpha = 1/20#1/8     # INFECTIOUSNESS
    beta = 0.2#0.95      # EFFECTIVENESS OF ANTIBODIES?
    gamma = 0.1#45     # RECOVERY RATE
    INFECTED = 255
    SUSCEPTIBLE = 25
    RECOVERED = 0
    vals = [INFECTED, SUSCEPTIBLE, RECOVERED]


    newGrid = grid.copy()
    for i in range(N):

        for j in range(N):
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                    grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                    grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                    grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])//255
            # apply Conway's rules
            if grid[i, j]  == SUSCEPTIBLE:
                if (total >= 1 ):
                    newGrid[i, j] = np.random.choice(vals, p=[total*alpha, 1-total*alpha, 0])

            elif grid[i, j]  == INFECTED:
                newGrid[i, j] = np.random.choice(vals, p=[1-gamma, 0, gamma])

            elif grid[i, j]  == RECOVERED:
                newGrid[i, j] = np.random.choice(vals, p=[0, 1-beta, beta])


    # update data
    mat.set_data(newGrid)
    grid = newGrid


    return [mat]

# set up animation
fig, ax = plt.subplots()

# cmap = colors.ListedColormap(['green', 'black', 'yellow'])
# cmap = colors.ListedColormap(['orange', 'lightyellow', 'olivedrab'])
cmap = colors.ListedColormap(['olivedrab', 'lightyellow', 'red'])
bounds=[0,5,30,255]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(grid, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)
# plt.colorbar(mat, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1, 225])
# mat = ax.matshow(grid)
# mat = plt.imshow(grid)
ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)

plt.show()
