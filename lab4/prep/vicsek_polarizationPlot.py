import numpy as np
import scipy as sp
from scipy import sparse
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


L = 32.0
rho = 3.0
N = int(rho*L**2)
print(" N",N)

r0 = 0.5 #1.0        # radius
deltat = 1.0    # timestep
factor = 0.5
v0 = r0/deltat*factor # velocity
iterations = 500
eta = 0.1       #noise term


pos = np.random.uniform(0,L,size=(N,2))
orient = np.random.uniform(-np.pi, np.pi,size=N)

# fig, ax= plt.subplots(figsize=(6,6))

# qv = ax.quiver(pos[:,0], pos[:,1], np.cos(orient[0]), np.sin(orient), orient, clim=[-np.pi, np.pi])
polArr = np.zeros(iterations)

# def animate(i):
#     print(i)
for i in range(iterations):

    # global orient
    # global polArr
    tree = cKDTree(pos,boxsize=[L,L])
    dist = tree.sparse_distance_matrix(tree, max_distance=r0,output_type='coo_matrix')

    #important 3 lines: we evaluate a quantity for every column j
    data = np.exp(orient[dist.col]*1j)
    # construct  a new sparse marix with entries in the same places ij of the dist matrix
    neigh = sparse.coo_matrix((data,(dist.row,dist.col)), shape=dist.get_shape())
    # and sum along the columns (sum over j)
    S = np.squeeze(np.asarray(neigh.tocsr().sum(axis=1)))


    orient = np.angle(S)+eta*np.random.uniform(-np.pi, np.pi, size=N)


    cos, sin= np.cos(orient), np.sin(orient)
    polArr[i] = np.sqrt(sum(cos)**2 + sum(sin)**2)/N

    pos[:,0] += cos*v0
    pos[:,1] += sin*v0

    pos[pos>L] -= L
    pos[pos<0] += L

    # qv.set_offsets(pos)
    # qv.set_UVC(cos, sin,orient)
    # return qv,


# anim = FuncAnimation(fig,animate,np.arange(1, 200),interval=1)
plt.plot(range(iterations), polArr)
plt.show()
