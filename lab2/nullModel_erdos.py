#! /usr/bin/python3

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# REAL

df = open("airlines/airlines.txt", 'r')
num_vertices = 0

for line in df:
    line_list = line.strip().split()
    if line_list[0] == '*Vertices':
        num_vertices = int(line_list[1])
        break


realNetwork = nx.empty_graph(num_vertices)

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
        realNetwork.add_edge(int(line_list[0]), int(line_list[1]))

realGCC = nx.transitivity(realNetwork)
print(f"realGCC: {realGCC}")
# RANDOM


No_nodes = 333
No_edges = 2126

iterations = 500

GCC_list = [0 for i in range(iterations)]
# GCC_list = np.zeros(iterations)

for iteration in range(iterations):

    G = nx.gnm_random_graph(No_nodes, No_edges)

    n = G.order()
    ne = G.size()
    max_deg = max(dict(G.degree()).values())

    GCC = nx.transitivity(G)
    GCC_list[iteration] = GCC

avg_randomGCC = mean(GCC_list)

print(f"{iterations}-run avgerage randomGCC: {avg_randomGCC}")

# print(GCC_list)
top5 = np.percentile(GCC_list, 95)
print(f"The top5%-border is {top5}")

standard_deviation = np.std(GCC_list)
print(f"Standard deviation = {standard_deviation}")
print(f"=> real network is {(realGCC-avg_randomGCC)/standard_deviation} standard deviations above the erdos mean.")


boxes = [GCC_list, realGCC]

plt.boxplot(boxes, labels=["Erdos Renyi","Airlines"])

plt.title("Box plots of GGC for random and real network")
plt.ylabel("GCC")
plt.show()
