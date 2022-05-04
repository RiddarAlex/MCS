import sys
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import imshow

N = 100
T = 100
gamma = 0.5

HEALTHY = 0
SICK = 1
vals = [HEALTHY, SICK]

grid = np.zeros(100)
grid[N//2] = 1

for t in range(T)
tmp = np.random.choice(vals, 1, p=[gamma, 1-gamma])
grid[i] = tmp[0]


for i in range(N):
    print(f"{grid[i]}", end = '')
