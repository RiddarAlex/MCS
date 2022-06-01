#MCS final project

import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow
import random
from random import randrange
from statistics import mean

N = 32

EMPTY, UP, DOWN, WALL = 1, 2, 3, 9999
states = [EMPTY, UP, DOWN]

grid = [EMPTY for i in range(N*N)]

grid = np.random.choice(states, (N,N+2), p=[0.8, 0.1, 0.1])
# grid = np.random.choice(states, (N,N+2), p=[0.7, 0.15, 0.15])
for i in range(N):
    grid[i][0], grid[i][-1] = WALL, WALL

newGrid = grid.copy()

T = 200
totalFlow = []

# PROBABILITIES
PL11, PR11, PW11 = 0.25, 0.5, 0.25
PR12, PW12       = 0.75, 0.25
PL13, PW13       = 0.25, 0.75
PL21, PR21, PW21 = 0.25, 0.5, 0.25
PR22, PW22       = 0.75, 0.25
PL23, PW23       = 0.25, 0.75
PB  , PW3        = 0.5, 0.5



#-------------------------------------------------------------------------------
def move_if_possible(choices, probabilities):
    indices = [e for e in range(len(choices))]
    index = np.random.choice(indices, p=probabilities)
    target = choices[index]

    if newGrid[target] == EMPTY:
        newGrid[target] = myType
        newGrid[current] = EMPTY

#-------------------------------------------------------------------------------
for t in range(T):
    currentFlow = 0

    # plt.title(f"t = {t}")

    newGrid = grid.copy()


    populationSize = 0#N*N
    for i in range(N):
        for j in range(1,N+1):

            ### APPLY RULES
            current = (i , j)

            if grid[current] == UP:
                myType = UP
                otherType = DOWN
                forward  = ((i + 1) % N     , j      )
                backward = ((N + i - 1) % N , j      )
                left     = (i               , (j - 1))
                right    = (i               , (j + 1))

            elif grid[current] == DOWN:
                myType = DOWN
                otherType = UP
                forward  = ((N + i - 1) % N , j      )
                backward = ((i + 1) % N     , j      )
                left     = (i               , (j + 1))
                right    = (i               , (j - 1))
            else:
                continue

            populationSize += 1

            if grid[forward] == EMPTY:
                if newGrid[forward] == EMPTY:
                    newGrid[forward] = myType
                    newGrid[current] = EMPTY
                    if ( (i == N-1) and (myType == UP) ) or ( (i == 0) and (myType == DOWN) ):
                        currentFlow += 1

            elif (grid[forward] != EMPTY and grid[left] != EMPTY) and (grid[right] != EMPTY):
                move_if_possible([backward, current], [PB, PW3])

            elif grid[forward] == myType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL11, PR11, PW11])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR12, PW12])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL13, PW13])


            elif grid[forward] == otherType:

                if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([left, right, current], [PL21, PR21, PW21])

                elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                    move_if_possible([right, current], [PR22, PW22])

                elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                    move_if_possible([left, current], [PL23, PW23])


    grid = newGrid
    totalFlow.append(currentFlow)
    if t%50 == 0:
        print(f"t: {t} \tPopulation size: {populationSize}")
    # print(f"Flow at t = {t}: {totalFlow[t]}")


#-------------------------------------------------------------------------------
homogeneity = []
upCounts = []
downCounts = []

for col in range(1,N+1):
    upCount, downCount = 0, 0
    for row in range(N):
        if grid[row][col] == UP:
            upCount += 1
        elif grid[row][col] == DOWN:
            downCount += 1

    upCounts.append(upCount)
    downCounts.append(downCount)

    if upCount + downCount > 0:
        homogeneity.append((upCount - downCount)/(upCount + downCount))
    else:
        homogeneity.append(0)


print(F"Homogeneity: {homogeneity}")
sortedness = mean([abs(e) for e in homogeneity])
print(f"Sortedness: {sortedness}")

flow = sum(totalFlow)/(populationSize*T)
print(f"Flow: {flow}")

fig, ax = plt.subplots()

ax.bar(range(N), downCounts, label='DOWN')
ax.bar(range(N), upCounts, bottom=downCounts,label='UP')
plt.title(f"Column-wise homogeneity plot for t = {T}")
plt.ylabel(f"Up+Down")
plt.xlabel(f"Column index")
ax.legend()
    # for row in range(N):
    #     if grid[col][row]

# plt.plot(range(N), homogeneity, linestyle='dotted', marker='H')
# plt.title(f"Column-wise homogeneity plot for t = {T}")
# plt.ylabel(f"Up-Down/(Up+Down)")
# plt.xlabel(f"Column index")



plt.show()
