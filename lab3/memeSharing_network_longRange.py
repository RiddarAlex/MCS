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

grid_dimension = 32

T = 500

N = grid_dimension**2
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

neighbourhood = list(range(9))
neighbourhood.pop(4)
# print(neighbourhood)
remote_frequency = 10
remote_distance = 10

grid = RESTING*np.ones((grid_dimension, grid_dimension))#[RESTING for i in range(N)]#np.zeros(N)
grid[0][0], grid[-1][-1] = SHARER, BORED
print(grid)


newGrid = grid.copy()
resting_data = [0 for i in range(T)]
sharer_data = [0 for i in range(T)]
bored_data = [0 for i in range(T)]


for t in range(T):

    for i in range(N):

        row = i // grid_dimension
        col = i % grid_dimension

        target = random.choice(neighbourhood)
        target_row = ( grid_dimension + (row + target // 3 - 1) ) % grid_dimension
        target_col = ( grid_dimension + (col + target % 3 - 1) ) % grid_dimension

        if i % remote_frequency == 0:
            long_range_comm = np.random.choice([NO, YES], p=[0.5, 0.5])
            if long_range_comm:
                target_row = ( target_row + remote_distance ) % grid_dimension


        if grid[row][col]  == RESTING:
            newGrid[row][col] = np.random.choice(states, p=[1-p, p, 0])
            resting_data[t] += 1

        elif grid[row][col]  == SHARER:
            will_share = np.random.choice([NO, YES], p=[1-q, q])
            if will_share == YES:
                if grid[target_row][target_col] == RESTING:
                    newGrid[target_row][target_col] = SHARER
                elif grid[target_row][target_col] == BORED:
                    newGrid[row][col] = BORED
            sharer_data[t] += 1

        elif grid[row][col]  == BORED:
            will_browse = np.random.choice([NO, YES], p=[1-r, r])
            if will_browse == YES:
                if grid[target_row][target_col] == RESTING:
                    newGrid[row][col] = RESTING
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