import sys
import itertools
import math


users_dict = {}
user1_dict = {}
user1_all_avg = 0
weight_list = []
movie = "unknown"

def print_neighbors(neighbors):
    for neighbor in neighbors:
        print(neighbor)

def get_weight(item):
    return item[1]

def pearson_correlation(user1, user2):
    # global user1_all_avg
    global users_dict
    global user1_dict

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

    numerator = 0
    denominator1 = 0
    denominator2 = 0

    i = 1
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
        #users_dict[elem[0]]
        if movie in [tmp_tuple[0] for tmp_tuple in users_dict[elem[0]]]:
            valide_list.append(elem)
    sorted_list = sorted(valide_list, key = get_weight, reverse=True)
    return sorted_list[0:k]

def Predict(user1, item, k_nearest_neighbors):
    global user1_all_avg
    global users_dict
    global user1_dict

    numerator = 0
    denominator = 0
    for elem in k_nearest_neighbors:
        user2_list = users_dict[elem[0]]
        user2_avg = user2_list[0]
        cur_weight = elem[1]
        i = 1
        while i < len(user2_list):
            cur_movie = user2_list[i][0]
            if cur_movie in user1_dict:
                numerator += (user2_list[i][1] - user2_avg) * cur_weight
                denominator += abs(cur_weight)
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
        for elem in elems:
            elem = elem.strip()

        if elems[0] == user_id:
            user1_dict[elems[2]] = float(elems[1])
            user1_all_avg += float(elems[1])
            continue

        if elems[0] in users_dict:
            users_dict[elems[0]].append((elems[2], float(elems[1])))
            #users_dict[elems[0]][0] += float(elems[1])
        else:
            #users_dict[elems[0]] = []
            #users_dict[elems[0]] = [float(elems[1]), (elems[2], float(elems[1]))]
            users_dict[elems[0]] = [(elems[2], float(elems[1]))]

    user1_all_avg /= len(user1_dict)

    #for key, value in users_dict.items():
    #    users_dict[key][0] /= len(users_dict[key]) - 1




def _main():
    # filename = sys.argv[1]
    # support = int(sys.argv[2])
    # bucket_size = int(sys.argv[3])

    global users_dict
    global weight_list
    global movie

    filename = "ratings-dataset.tsv"
    user_id = "Kluver"
    movie = "The Fugitive"
    k = 10

    

    init_from_input(filename, user_id, movie, k)
    for key in users_dict:
        cur_weight = pearson_correlation(user_id, key)
        weight_list.append((key, cur_weight))

    k_nearest_neighbors = K_nearest_neighbors(user_id, k)
    print_neighbors(k_nearest_neighbors)

    predictd_rate = Predict(user_id, movie, k_nearest_neighbors)
    print(predictd_rate)

_main()
