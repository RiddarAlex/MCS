from random import randrange
import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow


import matplotlib.pyplot as plt
import numpy as np

time_steps = 1000
N = 1000


p = 0.01
q = 0.05
r = 0.01

# STATES
RESTING = 2
SHARER = 3
BORED = 1

states = [RESTING, SHARER, BORED]

iterations = 1

data = np.zeros((iterations, time_steps))



for j in range(iterations):

    grid = RESTING*np.ones(N)

    grid[0] = SHARER
    grid[1] = BORED
    

    x = np.zeros(N)

    newGrid = grid.copy()

    for t in range(time_steps):

    

        for i in range(N):


            if (grid[i] == RESTING):
                newGrid[i] = np.random.choice(states, p=[1-p, p, 0])

            elif (grid[i] == SHARER):
                pick = np.random.choice([0, 1], p=[1-q, q])
                if (pick == 1):
                    random_body = randrange(N)
                    if (grid[random_body] == RESTING):
                        newGrid[random_body] = SHARER
                    elif (grid[random_body] == BORED):
                        newGrid[i] = BORED

            elif (grid[i] == BORED):
                pick = np.random.choice([0, 1], p=[1-r, r])
                if (pick == 1):
                    random_body = randrange(N)
                    if (grid[random_body] == RESTING):
                        newGrid[i] = RESTING


            x[i] = i+1

        #sick = np.sum(newGrid)
        data[j,t] = np.sum(grid)

        grid = newGrid





        plt.bar(x, grid)
        plt.title(f"t = {t} out of {time_steps}")
        plt.pause(0.001)
        plt.clf()


# results = np.zeros(time_steps)
# for t in range(time_steps):
#     results[t] = np.mean(data[:,t])

# plt.plot(range(time_steps), results)
# plt.title('Average percentage of infected people at each timestep')
# plt.ylabel('Percentage of infected people')
# plt.xlabel('Timesteps')

# plt.show()