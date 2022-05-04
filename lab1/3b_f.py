import matplotlib.pyplot as plt
import numpy as np

time_steps = 30
N = 100
gamma = 0.3

n_infected = 0

iterations = 1000

data = np.zeros((iterations, time_steps))
sick = 0
recovered = 0

for j in range(iterations):

    grid = np.zeros(N)
    grid[50] = 1

    x = np.zeros(N)

    newGrid = grid.copy()

    for t in range(time_steps):


        for i in range(N):
            if (grid[i] == 1):
                newGrid[i] = np.random.choice([0, 1], p=[gamma, 1-gamma])
                if newGrid[i] == 0:
                    recovered += 1
            elif (grid[i-1] == 1) or (grid[(i+1)%N] == 1):
                newGrid[i] = np.random.choice([0, 1], p=[gamma, 1-gamma])
            x[i] = i+1

        sick = np.sum(newGrid)
        data[j,t] = sick - np.sum(grid)

        grid = newGrid





        # plt.bar(x, grid)
        # plt.pause(0.001)
        # plt.clf()

    n_infected += np.sum(grid)

print(n_infected/iterations)
