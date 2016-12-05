import networkx as nx
import community
import numpy as np
import matplotlib.pyplot as plt
import sys

# key of sorting edge. using "credit" of edge as key
def get_edge_credit(edge):
    return (edge[2]).get("credit")

# Top -> Bottom: build bfs array
def get_bfs_2d_array(G, root_name):
    # initialize root node credit
    G.node[root_name]["credit"] = 1.0
    # each level in bfs is one level of array
    # each level is a dict
    # key: node_name, value: num of shortest pathes through the node
    bfs_2d_array = [{root_name: 1}]
    # save the nodes in above levels
    arriveds = set([root_name])
    level_index = 0
    # loop until no node in new level
    while True:
        # dict for new level
        new_level = {}
        # dict for current level
        cur_level = bfs_2d_array[level_index]
        for cur_node_name in cur_level.keys():
            for next_node_name in G.neighbors(cur_node_name):
                # filtering the nodes in the same level and upper levels
                if next_node_name not in arriveds:
                    # exists, add num of cur_node to new node's value
                    if next_node_name in new_level:
                        new_level[next_node_name] += cur_level[cur_node_name]
                    # Not exists, set num of cur_node as new node's value
                    else:
                        new_level[next_node_name] = cur_level[cur_node_name]
                        # initialize node credit
                        G.node[next_node_name]["credit"] = 1.0
        # no node in new level, break
        if len(new_level) == 0:
            break
        # add nodes in new level to arriveds
        arriveds |= set(new_level.keys())
        # add new level to array
        bfs_2d_array.append(new_level)
        level_index += 1
    # return bfs array
    return bfs_2d_array

# Bottom ->Top: compute credits
def assign_edge_credit(G, bfs_2d_array):
    # Bottom ->Top
    level_index = len(bfs_2d_array) - 1
    while level_index > 0:
        # dict for current level
        cur_level = bfs_2d_array[level_index]
        for cur_node_name in cur_level.keys():
            # dict for above level
            aboves = bfs_2d_array[level_index - 1]
            for neigher_name in G.neighbors(cur_node_name):
                # filter nodes in current level and lower level
                if neigher_name in aboves:
                    # increase value = (credit of cur_node) * rate
                    # rate = (num of shortest paths through above node) / (num of shortest paths through cur node)
                    increase_credit = (G.node[cur_node_name]["credit"] * aboves[neigher_name] * 1.0) / cur_level[cur_node_name]
                    # increase edge credit
                    G.edge[neigher_name][cur_node_name]["credit"] += increase_credit
                    # increase node credit
                    G.node[neigher_name]["credit"] += increase_credit
        level_index -= 1

# Compute Betweenness with specific root
def get_bet_from_root(G, root_name):
    # Top -> Bottom: build bfs array
    bfs_2d_array = get_bfs_2d_array(G, root_name)
    # Bottom ->Top: compute credits
    assign_edge_credit(G, bfs_2d_array)

# Compute Betweenness
def get_betweenness(G):
    # compute credit for each node as root
    for node_name in G.nodes():
        # get betweenness when node as root
        get_bet_from_root(G, node_name)
    # credit of edges divided by 2, because each edge compute twice
    for edge in G.edges_iter(data=True):
        edge[2]["credit"] /= 2.0

# find cluster
def find_cluster(G):
    max_mod = -1
    partition_num = 0
    max_partition = {}
    new_G = G.copy()
    # loop util there is no edge
    while True:
        count = 0
        partition = {}
        # compute the num of parts
        for part in nx.connected_components(new_G):
            for node in part:
                partition[node] = count
            count += 1
        # No edge, Break
        if count == len(new_G.nodes()):
            break
        # Compute modularity
        # Use ORIGINAL G  !!!
        mod = community.modularity(partition, G)
        # check whether the modularity is the max
        if mod > max_mod:
            max_mod = mod
            partition_num = count
            max_partition = partition
        # sort edges based on credit
        sorted_edges = sorted(new_G.edges_iter(data=True), key=get_edge_credit, reverse=True)
        # remove one or more edges with max credit
        edge_index = 0
        max_credit = sorted_edges[edge_index][2]
        while edge_index < len(new_G.edges()) and sorted_edges[edge_index][2] == max_credit:
            new_G.remove_edge(sorted_edges[edge_index][0], sorted_edges[edge_index][1])
            edge_index += 1
        # Compute New Betweenness AGAIN  !!!
        get_betweenness(new_G)
    # return max modularity, modularity num, and the parition
    return max_mod, partition_num, max_partition

# compute color list
def get_colors_list(G, partition, partition_num):
    color_map = {}
    index = 0
    # compute color map
    while index < partition_num:
        color_map[index] = (index * 1.0) / partition_num
        index += 1
    # compute and return color list
    return [color_map.get(partition[node], 0.25) for node in G.nodes()]

# output partitions
def output_partitions(partition, partition_num):
    # initialize list
    partitions_list = []
    index = 0
    while index < partition_num:
        partitions_list.append([])
        index += 1
    # assign nodes to list
    for key, value in partition.items():
        partitions_list[value].append(key)
    # sort list
    sorted_list = []
    for ls in partitions_list:
        # transfer elem from string to int
        int_ls = [int(x) for x in ls]
        sorted_list.append(sorted(int_ls))
    sorted_list = sorted(sorted_list)
    for ls in sorted_list:
        print(list_string(ls))

# transfer int list to string
def list_string(ls):
    str_ls = [str(x) for x in ls]
    return "[" + ",".join(str_ls) + "]"

# print nodes of graph G
def print_nodes(G):
    for n, d in G.nodes_iter(data=True):
        print(n)
        print(d)
        print("------------")
    print("\nNodes  End\n\n\n")

# print edges of graph G
def print_edges(G):
    for edge in G.edges_iter(data=True):
        print(edge)
    print("\nEdges  End\n\n\n")


def _main():
    inputFilename = sys.argv[1]
    outputImage = sys.argv[2]

    # inputFilename = "input.txt"
    # outputImage = "image.png"

    with open(inputFilename, "r") as fp:
        lines = fp.readlines()

    # build graph from input
    G = nx.Graph()
    for line in lines:
        nodes = line.split(" ")
        G.add_edge(nodes[0].strip(), nodes[1].strip(), {"credit": 0.0})

    if len(G.edges()) == 0:
        return

    # compute betweenness
    get_betweenness(G)
    print_edges(G)
    # find cluster, and return the partition which can get max modularity and the num of partition
    max_mod, partition_num, max_partition = find_cluster(G)
    # output partition
    output_partitions(max_partition, partition_num)
    # compute the list of color of nodes
    color_list = get_colors_list(G, max_partition, partition_num)
    # drawing
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=color_list)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    #plt.show()
    plt.axis('off')
    # output image
    plt.savefig(outputImage)


_main()