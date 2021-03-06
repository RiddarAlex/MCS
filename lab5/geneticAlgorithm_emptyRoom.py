import numpy as np
import random
import math

# %Floor painter algorithm
# %Code translated into python Fiona Skerman from matlab code written by Alex Szorkovszky for UU Modelling Complex Systems

# %INPUTS
# %rules: 54-cell array with one of three actions: 0(no turn) 1(turn left) 2(turn right) 3(random turn left/right)
# %room: MxN matrix defining a rectangular room with each square either 0(empty) or 1(furniture) or 2(painted)


# Chromosome (54-cell rule array) encodes action for each of 54 different scenarios
# no turn, turn left, turn right, turn left/right with 50/50
# let [c, f, l, r] denote the states of current, forward, left and right squares,
# then rule for that position is at position i=2(9f+3l+r)+Indicator[c=2] in chromosone.


#Painter has a position x,y in MxN matrix, and a direction -1 Left, 0 Up, 1 Right, -2 Down.

# Each time step consists of three parts
# a) according to rule on current environment update direction either 0 no turn, 1 turn left, 2 turn right, 3 random turn left/right
# b) if on unpainted square, paint it
# c) go forwards if possible

# OUTPUTS
# score: percentage of empty space painted
# xpos: x positions over time
# ypos: y positions over time

def main():

    No_chromosomes = 50
    genes_per_chromosome = 54

    No_generations = 2
    No_iterations = 5

    fitness = np.zeros((No_chromosomes, No_generations))


    population = np.random.choice([0, 1, 2, 3], No_chromosomes*genes_per_chromosome,
          p=[1/4, 1/4, 1/4, 1/4]).reshape(No_chromosomes, genes_per_chromosome)

    room = np.zeros((20,40))

    for generation in range(No_generations):
        print(f"Generation: {generation}")

        for chromosome in range(No_chromosomes):

            # avg_fitness = [0 for e in range(No_iterations)]
            avg_fitness = np.zeros((No_iterations, 1))

            for iteration in range(No_iterations):

                avg_fitness[iteration] = painter_play(population[chromosome,:], room)

            fitness[chromosome][generation] = np.mean(avg_fitness)
            # print(painter_play(population[chromosome,:], room))

    # print(fitness)

    # print(np.sort(fitness[:,-1]))

    # print(fitness[:,-1])

    # print( type(np.where(fitness[:,-1] > np.sort(fitness[:,-1])[10])) )



        top40indices, = np.where(fitness[:,-1] > np.sort(fitness[:,-1])[10])

        top10indices = np.where(fitness[:,-1] >= np.sort(fitness[:,-1])[40])

        print(np.sort(fitness[top40indices,-1]))

        print(np.sort(fitness[top10indices,-1]))

        # print(top40)


        new_population = population.copy()


        offspring_index = 0

        for parent1 in top40indices:

            parent2 = np.random.choice(top40indices)

            split_index = random.randrange(genes_per_chromosome)

            new_population[offspring_index] = np.append(population[parent1][0:split_index],
            population[parent2][split_index:-1])

            offspring_index += 1

        for parent1 in top10indices:

            parent2 = np.random.choice(top10indices)

            split_index = random.randrange(genes_per_chromosome)

            new_population[offspring_index] = np.append(population[parent1][0:split_index],
            population[parent2][split_index:-1])

            offspring_index += 1


        population = new_population


def painter_play(rules,room):
  #returns score, xpos, ypos

  M, N = room.shape

  #Calculates number of squares t to be painted. / #steps allowed
  t=M*N - room.sum()
  t=int(t)


  # add walls
  # env 0 - empty square, 1 - wall/obstruction, 2 - painted square
  env = np.ones((M+2,N+2));
  for i in range(1, M+1):
    for j in range(1, N+1):
      env[i][j]=0

  #new room size including walls
  M=M+2
  N=N+2

  xpos=[np.nan]*(t+1)
  ypos=[np.nan]*(t+1)

  # %random initial location
  while True:
    xpos[0]=math.floor(M*random.random())
    ypos[0]=math.floor(N*random.random())
    if env[xpos[0], ypos[0]] == 0:
      break


  # random itial orientation (up=0,left=-1,right=+1,down=-2)
  direction = math.floor(4*random.random()) - 2

  # initial score
  score = 0

  for i in range(t):
    # directions -1: Left, 0: Up, 1: Right, 2: Down
    # dx, dy of a forward step (given current direction)
    dx = divmod(direction,2)[1]
    if direction == -1:
      dx = -1 * dx

    dy = divmod(direction+1,2)[1]
    if direction == -2:
      dy = -1*dy




    # dx, dy of a square to right (given currection direction)
    r_direction=direction+1
    if r_direction == 2:
      r_direction = -2

    dxr = divmod(r_direction,2)[1]
    if r_direction == -1:
      dxr = -1 * dxr
    dyr = divmod(r_direction+1,2)[1]
    if r_direction == -2:
      dyr = -1*dyr

    # evaluate surroundings (forward,left,right)
    local = [env[xpos[i] + dx, ypos[i] + dy], env[xpos[i] - dxr, ypos[i] - dyr], env[xpos[i] + dxr, ypos[i] + dyr]]

    #localnum= 2* np.dot([9,3,1], local) if env[xpos[i], ypos[i]] == 2 else 2* np.dot([9,3,1], local) + 1
    localnum= int(2* np.dot([9,3,1], local))
    if env[xpos[i], ypos[i]] == 2:
       localnum += 1

    #use turning rule 1 'turn left', 2 'turn right', 3 'turn left/right 50/50 probabilities'
    if rules[localnum] == 3:
      dirchange = math.floor(random.random()*2)+1
    else:
      dirchange = rules[localnum]

    if dirchange == 1:
      direction = direction - 1
      if direction == -3:
        direction = 1
    elif dirchange == 2:
      direction = direction + 1
      if direction == 2:
        direction = -2

    dx = divmod(direction,2)[1]
    if direction == -1:
      dx = -1 * dx

    dy = divmod(direction+1,2)[1]
    if direction == -2:
      dy = -1*dy

    # paint square
    if env[xpos[i],ypos[i]]==0:
      env[xpos[i],ypos[i]] = 2
      score = score + 1

    # go forward if possible - stay put if wall/obstacle ahead
    if env[xpos[i]+dx, ypos[i]+dy] == 1:
      xpos[i+1] = xpos[i]
      ypos[i+1] = ypos[i]
    else:
      xpos[i+1] = xpos[i]+dx
      ypos[i+1] = ypos[i]+dy


  # %normalise score by time
  score = score/t

  return score #env


if __name__ == '__main__':
    main()
