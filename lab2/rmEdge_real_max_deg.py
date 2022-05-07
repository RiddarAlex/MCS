#! /usr/bin/python3

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# ============== read in data from a file ==============

iterations = 1

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



        for i in range(int(ne*alpha)):
            vertex_degrees = dict(G.degree())
            max_vertex = max(vertex_degrees, key = lambda x: vertex_degrees[x])
            edges = list(G.edges(max_vertex))
            index_to_rm = random.randrange(len(edges)-1)
            G.remove_edge(edges[index_to_rm][0], edges[index_to_rm][1])

        # print("G is of order", n, "and size", ne, "and maximum degree is", max_deg) # just for info

        GCC = nx.transitivity(G)
        GCCs[iteration] = GCC
        # print(f"The GCC is {GCC}")

        # Plot the network:
        #nx.draw(G, with_labels=False, node_color='orange', node_size=30, edge_color='black', linewidths=1, font_size=15)

    # ============== Community Partition of airline network =============



    from networkx.algorithms import community

    G_communities=community.greedy_modularity_communities(G)
    mod=community.modularity(G,G_communities)
    # print("Modularity value of this partition on airline network:",mod)

    # print("The various Gs are of order", n, "and size", ne, "and their maximum degree is", max_deg)
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
