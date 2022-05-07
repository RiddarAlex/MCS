#! /usr/bin/python3

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

No_nodes = 333
No_edges = 2126
seed = 20160

iterations = 1

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



        for i in range(int(ne*alpha)):
            vertex_degrees = dict(G.degree())
            max_vertex = max(vertex_degrees, key = lambda x: vertex_degrees[x])
            edges = list(G.edges(max_vertex))
            index_to_rm = random.randrange(len(edges)-1)
            G.remove_edge(edges[index_to_rm][0], edges[index_to_rm][1])

        GCC = nx.transitivity(G)
        GCCs[iteration] = GCC

    avg_GCCs[a] = mean(GCCs)
    print(f"{iterations}-run avgGCC: {avg_GCCs[a]}")


    # G_comm=sorted(map(sorted, G_communities))
    #
    #
    # #Plot the graph with node colours showing community membershiop
    # node_colors_map = {}
    # for i, lg in enumerate(G_comm):
    #     for node in lg:
    #         node_colors_map[node] = i
    # node_colors = [node_colors_map[n] for n in G.nodes]
    #
    #
    # #fixes a layout of the nodes (note re-running this will change the layout)
    # pos = nx.fruchterman_reingold_layout(G)
    #
    # nx.draw(G, with_labels=False, node_color=node_colors, linewidths=1, font_size=15,node_size=30)
    #
    # plt.show()

plt.plot(alphas, avg_GCCs)
plt.title("Avg GCC vs alpha for removal of edges incident to max deg. node")
plt.xlabel("Alpha")
plt.ylabel("Avg_GCC")
plt.show()
