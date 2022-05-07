#! /usr/bin/python3

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# ============== read in data from a file ==============
# alpha = 0.1
iterations = 4

alphas = [0.1+0.1*i for i in range(9)]
avg_GCCs = [0 for i in range(len(alphas))]

for a, alpha in enumerate(alphas):

    GCCs = [0 for i in range(iterations)]

    print(f"alpha = {alpha}")
    for iteration in range(iterations):
        df = open("airlines/airlines.txt", 'r')
        num_vertices = 0

        for line in df:
            line_list = line.strip().split()
            if line_list[0] == '*Vertices':
                num_vertices = int(line_list[1])
                break



        # print("num_vertices =", num_vertices)
        G = nx.empty_graph(num_vertices)

        reading_edges = False
        for line in df:
            line_list = line.strip().split()
            if not reading_edges:
                if line_list[0] != "*Edges":
                    continue
                else:
                    reading_edges = True
                    continue
            else:
                G.add_edge(int(line_list[0]), int(line_list[1]))



        n = G.order()
        ne = G.size()
        max_deg = max(dict(G.degree()).values())



        for i in range(int(n*alpha)):
            nodes = list(G.nodes())
            random_node = random.choice(nodes)
            G.remove_node(random_node)

        GCC = nx.transitivity(G)
        GCCs[iteration] = GCC

    # ============== Community Partition of airline network =============

    from networkx.algorithms import community

    G_communities=community.greedy_modularity_communities(G)
    mod=community.modularity(G,G_communities)

    avg_GCCs[a] = mean(GCCs)
    print(f"{iterations}-run avgGCC: {avg_GCCs[a]}")

plt.plot(alphas, avg_GCCs)
plt.title("Average Global Clustering Coefficient as a function of alpha random removal")
plt.xlabel("Alpha")
plt.ylabel("Avg_GCC")
plt.show()
