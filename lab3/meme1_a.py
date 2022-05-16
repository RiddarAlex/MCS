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

grid = [RESTING for i in range(N)]
grid[0], grid[-1] = SHARER, BORED

# print(grid)


newGrid = grid.copy()
resting_data = [0 for i in range(T)]
sharer_data = [0 for i in range(T)]
bored_data = [0 for i in range(T)]


grid = np.array(grid).reshape(25,40)
#print(grid)


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
           

t = 0

def update(data):
    global grid
    global t

    N = 1000
    p = 0.01
    q = 0.05
    r = 0.01

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
                    target_y = target_x%25
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
