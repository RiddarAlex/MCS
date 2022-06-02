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

EMPTY, UP, DOWN, MONSTER, WALL = 1, 2, 3, 4, 9999
states = [EMPTY, UP, DOWN, MONSTER]

# grid = [EMPTY for i in range(N*N)]

T = 200
iterations = 50


flow_arr = []
sortedness_arr = []
bPrefer_arr = []


# rPrefer = 0


populationDensity = 0.35
pM = 0.00
pE = 1 - pM - populationDensity
pUP = populationDensity/2
pDOWN = pUP

rPrefer = 0.7

number_of_bP = 11
for bPrefer in [0.1*i for i in range(number_of_bP)]:
    print(f"bPrefer: {bPrefer}")

    # PROBABILITIES
    L = (0.5 - 0.5*rPrefer)
    R = (0.5 + 0.5*rPrefer)

    neutral = 0.25
    balance = (1-neutral)/2

    PL11, PR11, PW11 = balance*(1 - rPrefer), balance*(1 + rPrefer), neutral
    PR12, PW12       = R, 1 - R
    PL13, PW13       = L, 1 - L
    PL21, PR21, PW21 = balance*(1 - rPrefer), balance*(1 + rPrefer), neutral
    PR22, PW22       = R, 1 - R
    PL23, PW23       = L, 1 - L
    PB  , PW3        = bPrefer, 1 - bPrefer

    # R_preference = 0.8
    # twoOptions = (1 - R_preference)
    # threeOptions = (1 - R_preference)/2
    #
    # PL11, PR11, PW11 = threeOptions, R_preference, threeOptions
    # PR12, PW12       = R_preference, twoOptions
    # PL13, PW13       = twoOptions, R_preference
    # PL21, PR21, PW21 = threeOptions, R_preference, threeOptions
    # PR22, PW22       = R_preference, twoOptions
    # PL23, PW23       = twoOptions, R_preference

    # PL11, PR11, PW11 = 0.25, 0.5, 0.25
    # PR12, PW12       = 0.75, 0.25
    # PL13, PW13       = 0.25, 0.75
    # PL21, PR21, PW21 = 0.25, 0.5, 0.25
    # PR22, PW22       = 0.75, 0.25
    # PL23, PW23       = 0.25, 0.75
    # PB  , PW3        = 0.5, 0.5



    #-------------------------------------------------------------------------------
    def move_if_possible(choices, probabilities):
        indices = [e for e in range(len(choices))]
        index = np.random.choice(indices, p=probabilities)
        target = choices[index]

        if newGrid[target] == EMPTY:
            newGrid[target] = myType
            newGrid[current] = EMPTY

    #-------------------------------------------------------------------------------
    for iteration in range(iterations):
        grid = np.random.choice(states, (N,N+2), p=[pE, pUP, pDOWN, pM])
        # grid = np.random.choice(states, (N,N+2), p=[0.7, 0.15, 0.15])
        for i in range(N):
            grid[i][0], grid[i][-1] = WALL, WALL

        newGrid = grid.copy()

        totalFlow = []
        print(f"iteration: {iteration}")

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

                    elif grid[current] == MONSTER:
                        myType = MONSTER
                        forward  = ((i + 1) % N     , j      )
                        backward = ((N + i - 1) % N , j      )
                        left     = (i               , (j - 1))
                        right    = (i               , (j + 1))

                        move_if_possible([forward, backward, left, right], [0.25, 0.25, 0.25, 0.25])
                        continue
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


                    elif grid[forward] == otherType or grid[forward] == MONSTER:

                        if (grid[left] == EMPTY) and (grid[right] == EMPTY):
                            move_if_possible([left, right, current], [PL21, PR21, PW21])

                        elif (grid[left] != EMPTY) and (grid[right] == EMPTY):
                            move_if_possible([right, current], [PR22, PW22])

                        elif (grid[left] == EMPTY) and (grid[right] != EMPTY):
                            move_if_possible([left, current], [PL23, PW23])


            grid = newGrid
            totalFlow.append(currentFlow)
            # if t%50 == 0:
            #     print(f"t: {t} \tPopulation size: {populationSize}")
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
                # homogeneity.append(0)
                homogeneity.append(1)


        # print(F"Homogeneity: {homogeneity}")
        sortedness = mean([abs(e) for e in homogeneity])
        print(f"Sortedness: {sortedness}")

        flow = N*sum(totalFlow)/(populationSize*T)
        print(f"Flow: {flow}")

        flow_arr.append(flow)
        sortedness_arr.append(sortedness)
        bPrefer_arr.append(bPrefer)



fig_sortedness = plt.subplots(figsize =(11, 7))
plt.hist2d(bPrefer_arr, sortedness_arr, cmap="hot", bins=[11,20])
plt.title(f"Heatmap of sortedness for iterations = {iterations} and t = {T}")
plt.ylabel('Sortedness score')
plt.xlabel('Backward preference parameter')
plt.colorbar()

fig_flow = plt.subplots(figsize =(11, 7))
plt.hist2d(bPrefer_arr, flow_arr, cmap="hot", bins=[11,20])
plt.title(f"Heatmap of flow for iterations = {iterations} and t = {T}")
plt.ylabel('Flow score')
plt.xlabel('Backward preference parameter')
plt.colorbar()

# fig, ax = plt.subplots()
#
# ax.bar(range(N), downCounts, label='DOWN')
# ax.bar(range(N), upCounts, bottom=downCounts,label='UP')
# plt.title(f"Column-wise homogeneity plot for t = {T}")
# plt.ylabel(f"Up+Down")
# plt.xlabel(f"Column index")
# ax.legend()
    # for row in range(N):
    #     if grid[col][row]

# plt.plot(range(N), homogeneity, linestyle='dotted', marker='H')
# plt.title(f"Column-wise homogeneity plot for t = {T}")
# plt.ylabel(f"Up-Down/(Up+Down)")
# plt.xlabel(f"Column index")



plt.show()
