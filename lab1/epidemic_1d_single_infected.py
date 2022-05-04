import matplotlib.pyplot as plt
import numpy as np

time_steps = 100
N = 100
gamma = 0.6

n_infected = 0

iterations = 1

data = np.zeros((iterations, time_steps))


for j in range(iterations):

    grid = np.zeros(N)
    grid[50] = 1

    x = np.zeros(N)

    newGrid = grid.copy()

    

    for t in range(time_steps):

     
        recovered = 0

        for i in range(N):
            if (grid[i] == 1):
                newGrid[i] = np.random.choice([0, 1], p=[gamma, 1-gamma])
                if newGrid[i] == 0:
                    recovered += 1
            elif (grid[i-1] == 1) or (grid[(i+1)%N] == 1):
                newGrid[i] = np.random.choice([0, 1], p=[gamma, 1-gamma])
            x[i] = i+1

        #sick = np.sum(newGrid)
        data[j,t] = np.sum(grid)

        grid = newGrid





        plt.bar(x, grid)
        plt.title(f"gamma = {gamma}")
        plt.pause(0.001)
        plt.clf()

    n_infected += np.sum(grid)

results = np.zeros(time_steps)
for t in range(time_steps):
    results[t] = np.mean(data[:,t])

# plt.plot(range(time_steps), results)
# plt.title(f"Average percentage of infected people at each timestep, gamma = {gamma}")
# plt.ylabel('Percentage of infected people')
# plt.xlabel('Timesteps')

print(f"{n_infected/iterations} % are infected at final time step")

plt.show()