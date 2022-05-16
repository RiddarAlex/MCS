import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow
from random import randrange
import random
from datetime import datetime
random.seed()


T = 500
N = 1000
p = 0.01 #probability of someone resting finding a meme
q = 0.05 #probablility of a sharer picking a random person
r = 0.01 #probablility of someone bored picking a random person

# STATES #
RESTING = 2
SHARER = 3
BORED = 1

states = [RESTING, SHARER, BORED]
NO = 0
YES = 1

grid = [RESTING for i in range(N)]#np.zeros(N)
grid[0], grid[-1] = SHARER, BORED
# print(grid)


newGrid = grid.copy()
resting_data = [0 for i in range(T)]
sharer_data = [0 for i in range(T)]
bored_data = [0 for i in range(T)]


for t in range(T):

    recovered = 0

    for i in range(N):
        if grid[i]  == RESTING:
            newGrid[i] = np.random.choice(states, p=[1-p, p, 0])
            resting_data[t] += 1

        elif grid[i]  == SHARER:
            will_share = np.random.choice([NO, YES], p=[1-q, q])
            if will_share == YES:
                target = randrange(N)
                if grid[target] == RESTING:
                    newGrid[target] = SHARER
                elif grid[target] == BORED:
                    newGrid[i] = BORED
            sharer_data[t] += 1

        elif grid[i]  == BORED:
            will_browse = np.random.choice([NO, YES], p=[1-r, r])
            if will_browse == YES:
                target = randrange(N)
                if grid[target] == RESTING:
                    newGrid[i] = RESTING
            bored_data[t] += 1
            

    grid = newGrid





    # plt.bar(range(N), grid)
    # plt.title(f't = {t}')

    # plt.pause(0.001)
    # plt.clf()

# results = np.zeros(T)
# for t in range(T):
#     results[t] = np.mean(data[:,t])

# plt.ylabel('Percentage of infected people')


plt.plot(range(T), resting_data, label="resting")
plt.plot(range(T), sharer_data, label="sharer")
plt.plot(range(T), bored_data, label="bored")
plt.xlabel('t')
plt.ylabel('Number of occurences')
plt.legend()
plt.show()
