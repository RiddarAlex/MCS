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


T = 1000
N = 1000
p = 0.001 #probability of someone resting finding a meme
# q = 0.05 #probablility of a sharer picking a random person
r = 0.01 #probablility of someone bored picking a random person

# STATES #
RESTING = 2
SHARER = 3
BORED = 1

states = [RESTING, SHARER, BORED]
NO = 0
YES = 1


# print(grid)

iterations = 25
number_of_qs = 10
q_list = [0.01*i for i in range(number_of_qs)]


resting_data = np.zeros((number_of_qs, iterations))#[0 for i in range(T)]
sharer_data = np.zeros((number_of_qs, iterations))#[0 for i in range(T)]
bored_data = np.zeros((number_of_qs, iterations))#[0 for i in range(T)]
resting_arr = []
sharer_arr = []
bored_arr = []
q_arr = []



for q_index, q in enumerate(q_list):
    print(f"q: {q}")
    for iteration in range(iterations):
        print(f"iteration: {iteration}")

        grid = [RESTING for i in range(N)]#np.zeros(N)
        grid[0], grid[-1] = SHARER, BORED
        newGrid = grid.copy()

        for t in range(T):

            recovered = 0

            for i in range(N):
                if grid[i]  == RESTING:
                    newGrid[i] = np.random.choice(states, p=[1-p, p, 0])
                    # resting_data[t] += 1

                elif grid[i]  == SHARER:
                    will_share = np.random.choice([NO, YES], p=[1-q, q])
                    if will_share == YES:
                        target = randrange(N)
                        if grid[target] == RESTING:
                            newGrid[target] = SHARER
                        elif grid[target] == BORED:
                            newGrid[i] = BORED
                    # sharer_data[t] += 1

                elif grid[i]  == BORED:
                    will_browse = np.random.choice([NO, YES], p=[1-r, r])
                    if will_browse == YES:
                        target = randrange(N)
                        if grid[target] == RESTING:
                            newGrid[i] = RESTING
                    # bored_data[t] += 1
                    

            grid = newGrid
    

        # resting_data[q_index][iteration] = grid.count(RESTING)
        # sharer_data[q_index][iteration] = grid.count(SHARER)
        # bored_data[q_index][iteration] = grid.count(BORED)


        resting_arr.append(grid.count(RESTING))
        sharer_arr.append(grid.count(SHARER))
        bored_arr.append(grid.count(BORED))
        q_arr.append(q)



            # plt.bar(range(N), grid)
            # plt.title(f't = {t}')

            # plt.pause(0.001)
            # plt.clf()

        # results = np.zeros(T)
        # for t in range(T):
        #     results[t] = np.mean(data[:,t])
   
    

        # plt.ylabel('Percentage of infected people')
# print("resting")
# print(resting_data)
# print("sharer")
# print(sharer_data)
# print("bored")
# print(bored_data)

# fig = plt.subplots(figsize =(10, 7))
# Creating plot
fig_resting = plt.subplots(figsize =(10, 7))
plt.hist2d(q_arr, resting_arr, cmap="hot")
plt.title(f"Heatmap of No. resting vs q for iterations = {iterations} and t = {T}")
plt.ylabel('No. resting')
plt.xlabel('q')
plt.colorbar()

fig_sharer = plt.subplots(figsize =(10, 7))
plt.hist2d(q_arr, sharer_arr, cmap="hot")
plt.title(f"Heatmap of No. sharer vs q for iterations = {iterations} and t = {T}")
plt.ylabel('No. sharer')
plt.xlabel('q')
plt.colorbar()

fig_bored = plt.subplots(figsize =(10, 7))
plt.hist2d(q_arr, bored_arr, cmap="hot")
plt.title(f"Heatmap of No. bored vs q for iterations = {iterations}  and t = {T}")
plt.ylabel('No. bored')
plt.xlabel('q')
plt.colorbar()
  
# show plot
plt.show()

# plt.plot(range(T), resting_data, label="resting")
# plt.plot(range(T), sharer_data, label="sharer")
# plt.plot(range(T), bored_data, label="bored")
# plt.xlabel('t')
# plt.ylabel('Number of occurences')
# plt.legend()
# plt.show()
