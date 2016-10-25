import sys
import itertools
import math


users_dict = {}
user1_dict = {}
user1_avg = 0
weight_list = []
    # def init_dict(dict, bucket_size):
    #     i = 0
    #     while i < bucket_size:
    #         dict[i] = 0
    #         i += 1
    #



    # def freq_set_to_str(freq_set):
    #     return "[" + ", ".join(map(str, map(list, sorted(list(freq_set))))) + "]"
    #
    # def output(dict_1, dict_2, freq_set):
    #     with open("output_multihash.txt", "a") as file:
    #         json.dump(dict_1, file)
    #         file.write("\n")
    #         json.dump(dict_2, file)
    #         file.write("\n")
    #         file.write(freq_set_to_str(freq_set))
    #         file.write("\n\n\n")

def print_neighbors(neighbors):
    for neighbor in neighbors:
        print(neighbor)

def get_weight(item):
    return item[1]

def pearson_correlation(user1, user2):
    global user1_avg
    global users_dict
    global user1_dict

    user2_list = users_dict[user2]
    user2_avg = user2_list[0]

    numerator = 0
    denominator1 = 0
    denominator2 = 0

    i = 1
    while i < len(user2_list):
        cur_movie = user2_list[i][0]
        if cur_movie in user1_dict:
            u = user1_dict[cur_movie] - user1_avg
            v = user2_list[i][1] - user2_avg
            numerator += u * v
            denominator1 += u * u
            denominator2 += v * v
        i += 1
    return numerator/(math.sqrt(denominator1) * math.sqrt(denominator2))

def K_nearest_neighbors(user1, k):
    global weight_list
    sorted_list = sorted(weight_list, key = get_weight, reverse=True)
    return sorted_list[0:k]

def Predict(user1, item, k_nearest_neighbors):
    global user1_avg
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

    return user1_avg + numerator/denominator

def init_from_input(filename, user_id, movie, k):
    # filename = "ratings-dataset.tsv"
    # user_id = "Kluver"
    # movie = "The Fugitive"
    #k = 10

    global user1_avg
    global users_dict
    global user1_dict
    
    with open(filename, 'r') as input:
        lines = input.readlines()

    for line in lines:
        elems = line.split("\t")
        #print(elems[0] + "  "+ elem[1] +"  " + elem[2] )
        for elem in elems:
            elem = elem.strip()

        #print(elems[0] + "  "+ elems[1] +"  " + elems[2] )
        if elems[0] == user_id:
            user1_dict[elems[2]] = float(elems[1])
            user1_avg += float(elems[1])
            continue

        if elems[0] in users_dict:
            users_dict[elems[0]].append((elems[2], float(elems[1])))
            users_dict[elems[0]][0] += float(elems[1])
        else:
            users_dict[elems[0]] = []
            #users_dict[elems[0]].append(float(elems[1]))
            #users_dict[elems[0]].append((elems[2], float(elems[1])))
            users_dict[elems[0]] = [float(elems[1]), (elems[2], float(elems[1]))]
           # users_dict[elem[0]].append()


    user1_avg /= len(user1_dict)

    for key, value in users_dict.items():
        users_dict[key][0] /= len(users_dict[key]) - 1




def _main():
    # filename = sys.argv[1]
    # support = int(sys.argv[2])
    # bucket_size = int(sys.argv[3])

    filename = "ratings-dataset.tsv"
    user_id = "Kluver"
    movie = "The Fugitive"
    k = 10

    global users_dict
    global weight_list

    init_from_input(filename, user_id, movie, k)
    for key in users_dict:
        cur_weight = pearson_correlation(user_id, key)
        weight_list.append((key, cur_weight))

    k_nearest_neighbors = K_nearest_neighbors(user_id, k)
    print_neighbors(k_nearest_neighbors)

    predictd_rate = Predict(user_id, movie, k_nearest_neighbors)
    print(predictd_rate)

_main()
