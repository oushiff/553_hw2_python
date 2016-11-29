import networkx as nx
import community
import numpy as np
import matplotlib.pyplot as plt
import sys


def get_edge_credit(edge):
    return (edge[2]).get("credit")

def get_bfs_2d_array(G, root_name):
    G.node[root_name]["credit"] = 1.0
    bfs_2d_array = [{root_name: 1}]
    arriveds = set([root_name])
    level_index = 0
    while True:
        new_level = {}
        cur_level = bfs_2d_array[level_index]
        for cur_node_name in cur_level.keys():
            for next_node_name in G.neighbors(cur_node_name):
                if next_node_name not in arriveds:
                    if next_node_name in new_level:
                        new_level[next_node_name] += cur_level[cur_node_name]
                    else:
                        new_level[next_node_name] = cur_level[cur_node_name]
                        G.node[next_node_name]["credit"] = 1.0
        if len(new_level) == 0:
            break
        arriveds |= set(new_level.keys())
        bfs_2d_array.append(new_level)
        level_index += 1
    return bfs_2d_array

def assign_edge_credit(G, bfs_2d_array):
    level_index = len(bfs_2d_array) - 1
    while level_index > 0:
        cur_level = bfs_2d_array[level_index]
        for cur_node_name in cur_level.keys():
            aboves = bfs_2d_array[level_index - 1]
            for neigher_name in G.neighbors(cur_node_name):
                if neigher_name in aboves:
                    increase_credit = (G.node[cur_node_name]["credit"] * aboves[neigher_name] * 1.0) / cur_level[cur_node_name]
                    G.edge[neigher_name][cur_node_name]["credit"] += increase_credit
                    G.node[neigher_name]["credit"] += increase_credit
        level_index -= 1


def get_bet_from_root(G, root_name):
    bfs_2d_array = get_bfs_2d_array(G, root_name)
    assign_edge_credit(G, bfs_2d_array)



def get_betweenness(G):
    for node_name in G.nodes():
        get_bet_from_root(G, node_name)
    for edge in G.edges_iter(data=True):
        edge[2]["credit"] /= 2.0


def find_cluster(G):
    max_mod = -1
    partition_num = 0
    max_partition = {}
    new_G = G.copy()
    while True:
        count = 0
        partition = {}
        for part in nx.connected_components(new_G):
            for node in part:
                partition[node] = count
            count += 1
        if count == len(new_G.nodes()):
            break
        # Use ORIGINAL G  !!!
        mod = community.modularity(partition, G)
        if mod > max_mod:
            max_mod = mod
            partition_num = count
            max_partition = partition
        sorted_edges = sorted(new_G.edges_iter(data=True), key=get_edge_credit, reverse=True)
        edge_index = 0
        max_credit = sorted_edges[edge_index][2]
        while edge_index < len(new_G.edges()) and sorted_edges[edge_index][2] == max_credit:
            new_G.remove_edge(sorted_edges[edge_index][0], sorted_edges[edge_index][1])
            edge_index += 1
        # Compute New Betweenness AGAIN  !!!
        get_betweenness(new_G)
    return max_mod, partition_num, max_partition


def get_colors_list(G, partition, partition_num):
    color_map = {}
    index = 0
    while index < partition_num:
        color_map[index] = (index * 1.0) / partition_num
        index += 1
    return [color_map.get(partition[node], 0.25) for node in G.nodes()]

def output_partitions(partition, partition_num):
    partitions_list = []
    index = 0
    while index < partition_num:
        partitions_list.append([])
        index += 1
    for key, value in partition.items():
        partitions_list[value].append(key)
    sorted_list = []
    for ls in partitions_list:
        int_ls = [int(x) for x in ls]
        sorted_list.append(sorted(int_ls))
    sorted_list = sorted(sorted_list)
    for ls in sorted_list:
        print(list_string(ls))

def list_string(ls):
    str_ls = [str(x) for x in ls]
    return "[" + ",".join(str_ls) + "]"

def print_nodes(G):
    for n, d in G.nodes_iter(data=True):
        print(n)
        print(d)
        print("------------")
    print("\nNodes  End\n\n\n")

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

    G = nx.Graph()
    for line in lines:
        nodes = line.split(" ")
        G.add_edge(nodes[0].strip(), nodes[1].strip(), {"credit": 0.0})

    if len(G.edges()) == 0:
        return

    get_betweenness(G)
    max_mod, partition_num, max_partition = find_cluster(G)

    output_partitions(max_partition, partition_num)
    color_list = get_colors_list(G, max_partition, partition_num)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=color_list)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    #plt.show()
    plt.axis('off')
    plt.savefig(outputImage)


_main()