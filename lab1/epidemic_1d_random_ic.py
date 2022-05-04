import matplotlib.pyplot as plt
import numpy as np

time_steps = 100
N = 100
gamma = 0.5
beta = 0.9

n_infected = 0

iterations = 100

data = np.zeros((iterations, time_steps))

has_died = 0


for j in range(iterations):

    grid = np.random.choice([0, 1], N, p=[1-beta, beta])

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

        #sick = np.sum(newGrid)
        data[j,t] = np.sum(grid)

        grid = newGrid





        # plt.bar(x, grid)
        # plt.pause(0.001)
        # plt.clf()

    n_infected += np.sum(grid)

    if np.sum(grid) == 0:
        has_died += 1

results = np.zeros(time_steps)
for t in range(time_steps):
    results[t] = np.mean(data[:,t])

plt.plot(range(time_steps), results)
plt.title('Average percentage of infected people at each timestep')
plt.ylabel('Percentage of infected people')
plt.xlabel('Timesteps')

print(f"{n_infected/iterations} % are infected at final time step")
print(f"The virus died out within 1000 timesteps in {100*has_died/iterations} % of runs")

plt.show()
