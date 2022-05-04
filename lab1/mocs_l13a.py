#MoCS Lab1 3a. A firing brain

import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow

counter = 0

N = 40
FIRING = 255
READY = 25
RESTING = 0
vals = [FIRING, READY, RESTING]

# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=[0.3, 0.7, 0.0]).reshape(N, N)


# np.set_printoptions(threshold=sys.maxsize)
# print(grid)


def update(data):
  global grid
  global counter
  if counter == 10: fig.savefig(f'A_Firing_Brain_Frame{counter}.png')
  counter += 1
  # copy grid since we require 8 neighbors for calculation
  # and we go line by line
  newGrid = grid.copy()
  for i in range(N):

    for j in range(N):
      # compute 8-neghbor sum
      # using toroidal boundary conditions - x and y wrap around
      # so that the simulaton takes place on a toroidal surface.
      total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] +
               grid[(i-1)%N, j] + grid[(i+1)%N, j] +
               grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
               grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])//255
      # apply Conway's rules
      if grid[i, j]  == READY:
        if (total == 2):
          newGrid[i, j] = FIRING

      elif grid[i, j]  == FIRING:
          newGrid[i, j] = RESTING

      elif grid[i, j]  == RESTING:
          newGrid[i, j] = READY

  # update data
  mat.set_data(newGrid)
  grid = newGrid

  return [mat]

# set up animation
fig, ax = plt.subplots()

# cmap = colors.ListedColormap(['green', 'black', 'yellow'])
cmap = colors.ListedColormap(['orange', 'lightyellow', 'olivedrab'])
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
