#! /usr/bin/python3

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

No_nodes = 333
No_edges = 2126
seed = 20160

iterations = 4

alphas = [0.1+0.1*i for i in range(9)]
avg_GCCs = [0 for i in range(len(alphas))]

for a, alpha in enumerate(alphas):

    GCCs = [0 for i in range(iterations)]

    print(f"alpha = {alpha}")
    for iteration in range(iterations):

        G = nx.gnm_random_graph(No_nodes, No_edges, seed=seed)

        n = G.order()
        ne = G.size()
        max_deg = max(dict(G.degree()).values())



        for i in range(int(n*alpha)):
            nodes = list(G.nodes())
            random_node = random.choice(nodes)
            G.remove_node(random_node)

        GCC = nx.transitivity(G)
        GCCs[iteration] = GCC

    avg_GCCs[a] = mean(GCCs)
    print(f"{iterations}-run avgGCC: {avg_GCCs[a]}")

plt.plot(alphas, avg_GCCs)
plt.title("Average Global Clustering Coefficient as a function of alpha random removal")
plt.xlabel("Alpha")
plt.ylabel("Avg_GCC")
plt.show()
