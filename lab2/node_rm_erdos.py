#! /usr/bin/python3

import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# ============== read in data from a file ==============

gcc_list = np.zeros(9)

alpha_list = [0.1+0.1*i for i in range(9)]

nRuns = 20

for alpha_index, alpha in enumerate(alpha_list):

    gcc = 0

    for j in range(nRuns):

        vertices = 333  # 10 nodes
        edges = 2126  # 20 edges
        seed = 20160  # seed random number generators for reproducibility

        # Use seed for reproducibility
        G = nx.gnm_random_graph(vertices, edges, seed=seed)


        ne = G.size()
                
        n = G.order()
        ne = G.size()
        max_deg = max(dict(G.degree()).values())


        for i in range(int(n*alpha)):
            nodes = list(G.nodes())
            random_node = random.choice(nodes)
            G.remove_node(random_node)

        gcc += nx.transitivity(G)/nRuns

    gcc_list[alpha_index] = gcc

    print(f" avg Global Clustering Coefficient: {gcc} alpha = {alpha}")

    n = G.order()
    ne = G.size()
    max_deg = max(dict(G.degree()).values())
    print("G is of order", n, "and size", ne, "and maximum degree is", max_deg) # just for info

plt.plot(alpha_list, gcc_list,'-o')
plt.title('Average GCC vs alpha with random node removal')
plt.ylabel('Avg GCC')
plt.xlabel('alpha')

# Plot the network:
#nx.draw(G, with_labels=False, node_color='orange', node_size=30, edge_color='black', linewidths=1, font_size=15)

# ============== Community Partition of airline network =============

# from networkx.algorithms import community

# G_communities=community.greedy_modularity_communities(G)
# mod=community.modularity(G,G_communities)
# print("Modularity value of this partition on airline network:",mod)


# G_comm=sorted(map(sorted, G_communities))


# #Plot the graph with node colours showing community membershiop
# node_colors_map = {}
# for i, lg in enumerate(G_comm):
#     for node in lg:
#         node_colors_map[node] = i
# node_colors = [node_colors_map[n] for n in G.nodes]


# #fixes a layout of the nodes (note re-running this will change the layout)
# pos = nx.fruchterman_reingold_layout(G)

# nx.draw(G, pos=pos, with_labels=False, node_color=node_colors, linewidths=1, font_size=15,node_size=30)
plt.show()


