#MoCS Lab1 3a. A firing brain

import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow

RUNS = 100
T = 1000
N = 40
FIRING = 255
READY = 25
RESTING = 0
vals = [FIRING, READY, RESTING]

cmap = colors.ListedColormap(['orange', 'lightyellow', 'olivedrab'])
bounds=[0,5,30,255]
norm = colors.BoundaryNorm(bounds, cmap.N)

firingData = np.zeros((RUNS, T))


for run in range(RUNS):
    grid = np.random.choice(vals, N*N, p=[0.3, 0.7, 0.0]).reshape(N, N)

    print(f"Run: {run}")

    for t in range(T):

        # if t == 999:
        #     print(f"t = {t}!:)")
        #
        #     mat = plt.imshow(grid, interpolation='nearest', origin='lower',
        #                         cmap=cmap, norm=norm)
        #     plt.show()

        newGrid = grid.copy()
        for i in range(N):

            for j in range(N):

                total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                    grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                    grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                    grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])//255

                if grid[i, j]  == READY:
                    if (total == 2):
                        newGrid[i, j] = FIRING

                elif grid[i, j]  == FIRING:
                    firingData[run, t] += 1
                    newGrid[i, j] = RESTING

                elif grid[i, j]  == RESTING:
                    newGrid[i, j] = READY

                grid = newGrid

results = np.zeros(T)
for t in range(T):
    results[t] = np.mean(firingData[:,t])

plt.plot(range(T), results)
plt.title('Average number of firing cells over time')
plt.ylabel('Number of firing cells')
plt.xlabel('Timesteps')

plt.show()
