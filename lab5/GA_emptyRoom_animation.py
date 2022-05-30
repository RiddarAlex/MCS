from cgi import test
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib import colors

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


def painter_play(rules,room):
  #returns score, xpos, ypos

  M, N = room.shape

  #Calculates number of squares t to be painted. / #steps allowed
  t=M*N - room.sum()
  t=int(t)


  # add walls
  # env 0 - empty square, 1 - wall/obstruction, 2 - painted square
  env = np.ones((M+2,N+2))
  for i in range(1, M+1):
    for j in range(1, N+1):
      env[i][j]=room[i-1,j-1]

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

  return score, xpos, ypos, #env

M = 20
N = 40

test_room=np.zeros((M,N))
for i in range(100):
    x = random.randrange(M)
    y = random.randrange(N)
    test_room[x,y] = 1

# print(test_room)

### empty room
# test_rules = [2, 0, 0, 3, 0, 3, 2, 2, 1, 2, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 3, 3, 0, 1, 3, 3, 1, 3, 1, 2, 0, 1, 3, 3, 0, 3, 2, 1, 1, 0, 1, 1, 2, 1, 2, 0, 2, 3, 0, 1, 3, 0]
### obstacles
test_rules = [2, 1, 0, 2, 0, 0, 0, 0, 0, 1, 1, 2, 3, 2, 3, 1, 2, 0, 1, 3, 3, 1, 1, 3, 3, 2, 2, 2, 1, 2, 3, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 3, 2, 2, 2, 1, 0, 2, 1, 2, 0, 0, 1, 0,]

score, xpos, ypos = painter_play(test_rules, test_room)

# print(xpos)
# print(ypos)
# print(len(xpos))
# plt.imshow(test_room)

cmap = colors.ListedColormap(['white', 'black', 'red', 'green'])
# cmap = colors.ListedColormap(['tab:green', 'tab:blue', 'tab:orange'])

bounds = [-0.5,0.5,1.5,2.5,3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)
mat = plt.imshow(test_room, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)

T = int(M*N-test_room.sum())
for i in range(T):
    test_room[xpos[i]-1,ypos[i]-1] = 3
    if i != 0:
        test_room[xpos[i-1]-1,ypos[i-1]-1] = 2
    plt.title(f"Time: {i}")
    mat = plt.imshow(test_room, interpolation='nearest', origin='lower',
                    cmap=cmap, norm=norm)
    plt.pause(0.000000000001)
    plt.clf()
  
plt.show()