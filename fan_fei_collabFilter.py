import sys
import itertools
import math
import re

users_dict = {}
user1_dict = {}
user1_all_avg = 0
tmp_users_avg_dict = {}
weight_list = []
movie = "unknown"

def print_neighbors(neighbors):
    for neighbor in neighbors:
        print(neighbor[0]+" %.5f" % neighbor[1])

def get_weight(item):
    return item[1]

def pearson_correlation(user1, user2):
    global users_dict
    global user1_dict
    global tmp_users_avg_dict

    user2_list = users_dict[user2]
    user1_avg = 0
    user2_avg = 0
    user1_co_list = []
    user2_co_list = []
    for elem in user2_list:
        if elem[0] in user1_dict:
            user1_co_list.append(user1_dict[elem[0]])
            user2_co_list.append(elem[1])
            user1_avg += user1_dict[elem[0]]
            user2_avg += elem[1]
    length = len(user1_co_list)
    user1_avg /= length
    user2_avg /= length
    tmp_users_avg_dict[user2] = user2_avg

    numerator = 0
    denominator1 = 0
    denominator2 = 0
    i = 0
    while i < length:
        u = user1_co_list[i] - user1_avg
        v = user2_co_list[i] - user2_avg
        numerator += u * v
        denominator1 += u * u
        denominator2 += v * v
        i += 1
    return numerator/(math.sqrt(denominator1) * math.sqrt(denominator2))

def K_nearest_neighbors(user1, k):
    global weight_list
    global movie
    valide_list = []
    for elem in weight_list:
        if movie in [tmp_tuple[0] for tmp_tuple in users_dict[elem[0]]]:
            valide_list.append(elem)
    sorted_list = sorted(valide_list, key = get_weight, reverse=True)
    return sorted_list[0:k]

def Predict(user1, item, k_nearest_neighbors):
    global user1_all_avg
    global users_dict
    global user1_dict
    global tmp_users_avg_dict
    global movie

    numerator = 0
    denominator = 0
    for elem in k_nearest_neighbors:
        user2_list = users_dict[elem[0]]
        user2_avg = user2_list[0]
        cur_weight = elem[1]
        i = 0
        while i < len(user2_list):
            if user2_list[i][0] == movie:
                numerator += (user2_list[i][1] - tmp_users_avg_dict[elem[0]]) * cur_weight
                denominator += abs(cur_weight)
                break
            i += 1
    return user1_all_avg + numerator/denominator

def init_from_input(filename, user_id, movie, k):
    global user1_all_avg
    global users_dict
    global user1_dict
    
    with open(filename, 'r') as input:
        lines = input.readlines()

    for line in lines:
        elems = line.split("\t")
        if elems[0].strip() == user_id:
            user1_dict[elems[2].strip()] = float(elems[1])
            user1_all_avg += float(elems[1])
            continue
        if elems[0].strip() in users_dict:
            users_dict[elems[0].strip()].append((elems[2].strip(), float(elems[1])))
        else:
            users_dict[elems[0].strip()] = [(elems[2].strip(), float(elems[1]))]
    user1_all_avg /= len(user1_dict)


def _main():
    global users_dict
    global weight_list
    global movie

    filename = sys.argv[1]
    user_id = sys.argv[2]
    movie = sys.argv[3]
    k = int(sys.argv[4])

    init_from_input(filename, user_id, movie, k)
    for key in users_dict:
        cur_weight = pearson_correlation(user_id, key)
        weight_list.append((key, cur_weight))

    k_nearest_neighbors = K_nearest_neighbors(user_id, k)
    print_neighbors(k_nearest_neighbors)

    predictd_rate = Predict(user_id, movie, k_nearest_neighbors)
    print("%.5f" % predictd_rate)

_main()
