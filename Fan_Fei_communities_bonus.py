import networkx as nx
import community
import numpy as np
import matplotlib.pyplot as plt


def get_edge_credit(edge):
    return (edge[2]).get("credit")

def get_bfs_2d_array(G, root_name):
    G.node[root_name]["credit"] = 1
    bfs_2d_array = [[root_name]]
    arriveds = set([root_name])
    level_index = 0
    while True:
        new_level = []
        for cur_node_name in bfs_2d_array[level_index]:
            for next_node_name in G.neighbors(cur_node_name):
                if next_node_name not in arriveds:
                    G.node[next_node_name]["credit"] = 1
                    new_level.append(next_node_name)
                    arriveds.add(next_node_name)
        #print(new_level)
        if len(new_level) == 0:
            break
        bfs_2d_array.append(new_level)
        level_index += 1
    return bfs_2d_array

def assign_edge_credit(G, bfs_2d_array):
    level_index = len(bfs_2d_array) - 1
    while level_index > 0:
        for cur_node_name in bfs_2d_array[level_index]:
            count = 0
            aboves = set(bfs_2d_array[level_index - 1])
            for neigher_name in G.neighbors(cur_node_name):
                if neigher_name in aboves:
                    count += 1
            increase_credit = G.node[cur_node_name]["credit"] / count
            for neigher_name in G.neighbors(cur_node_name):
                if neigher_name in aboves:
                    G.edge[neigher_name][cur_node_name]["credit"] += increase_credit
                    G.node[neigher_name]["credit"] += increase_credit
        level_index -= 1


def get_bet_from_root(G, root_name):
    bfs_2d_array = get_bfs_2d_array(G, root_name)
    #print(bfs_2d_array)
    assign_edge_credit(G, bfs_2d_array)



def get_betweenness(G):
    for node_name in G.nodes():
        get_bet_from_root(G, node_name)
        print(node_name)
        print_nodes(G)
    for edge in G.edges_iter(data=True):
        edge[2]["credit"] /= 2


# def edges_cmp(x, y):
#     return x[2] - y[2]



def find_cluster(G):
    sorted_edges = sorted(G.edges_iter(data=True), key=get_edge_credit, reverse=True)
    print(sorted_edges)

    nodes_num = len(G.nodes())
    edges_num = len(G.edges())
    edge_index = 0
    max_mod = -1
    partition_num = 0
    max_partition = {}


    while True:
        count = 0
        partition = {}
        for part in nx.connected_components(G):
            for node in part:
                partition[node] = count
            count += 1
        print(partition)
        if count == nodes_num:
            break
        mod = community.modularity(partition, G)
        print(mod)
        if mod > max_mod:
            max_mod = mod
            partition_num = count
            max_partition = partition

        max_credit = sorted_edges[edge_index][2]
        while edge_index < edges_num and sorted_edges[edge_index][2] == max_credit:
            # cur_edge = sorted_edges[edge_index]
            G.remove_edge(sorted_edges[edge_index][0],sorted_edges[edge_index][1])
            edge_index += 1

    return max_mod, partition_num, max_partition


def assign_colors(G, partition):


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
    # dataFilename = sys.argv[1]
    # initialFilename = sys.argv[2]

    inputFilename = "input.txt"
    outputImage = "image.png"


    with open(inputFilename, "r") as fp:
        lines = fp.readlines()

    G = nx.Graph()
    for line in lines:
        nodes = line.split(" ")
        G.add_edge(nodes[0].strip(), nodes[1].strip(), {"credit": 0})

    if len(G.edges()) == 0:
        return


    get_betweenness(G)
    #print_edges(G)


    # for part in nx.connected_components(G):
    #     print(part)
    #     aa = len(part)
    #     print(aa)
    max_mod, partition_num, max_partition = find_cluster(G.copy())

    print(max_mod)
    print(max_partition)

    assign_colors(G, max_partition, partition_num)

    pos = nx.spring_layout(G)


    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    #nx.draw_networkx_edge_labels(G, pos)
    nx.draw_networkx_labels(G, pos)

    # nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color=values)


    plt.show()





_main()