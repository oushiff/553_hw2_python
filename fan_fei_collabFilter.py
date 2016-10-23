import sys
import itertools
import math


class Collaborative_Filter(object):
    def __init__(self):
        self.users_dict = {}
        self.user1_dict = {}
        self.user1_avg = 0
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



    def pearson_correlation(user1, user2):
        user2_list = self.users_dict[user2]
        user2_avg = user2_list[0]

        numerator = 0
        denominator1 = 0
        denominator2 = 0

        i = 1
        while i < len(user2_list):
            cur_movie = user2_list[i][0]
            if cur_movie in self.user1_dict:
                u = self.user1_dict[cur_movie] - self.user1_avg
                v = user2_list[i][1] - user2_avg
                numerator += u * v
                denominator1 += u * u
                denominator2 += v * v
            i += 1
        return numerator/(math.sqrt(denominator1) * math.sqrt(denominator2))

    def K_nearest_neighbors(user1, k):
        pass


    def Predict(user1, item, k_nearest_neighbors):
        pass

    def init_from_input(args):
        filename = "ratings-dataset.tsv"
        user_id = "Kluver"
        movie = "The Fugitive"
        k = 10

        with open(filename, 'r') as input:
            lines = input.readlines()

        for line in lines:
            elems = line.split("\t")
            for elem in elems:
                elem = elem.trip()
            if elem[0] == user_id:
                self.user1_dict[elem[2]] = float(elem[1])
                self.user1_avg += float(elem[1])
                continue

            if elem[0] in self.users_dict:
                self.users_dict[elem[0]].append((elem[2], float(elem[1])))
                self.users_dict[elem[0]][0] += float(elem[1])
            else:
                self.users_dict[elem[0]] = [(float(elem[1]))]
                self.users_dict[elem[0]].append((elem[2], float(elem[1])))

        self.user1_avg /= len(user1_dict)

        for key, value in self.users_dict.items():
            self.users_dict[key][0] /= len(users_dict[key] - 1)




def _main():
    # filename = sys.argv[1]
    # support = int(sys.argv[2])
    # bucket_size = int(sys.argv[3])

    col_filter = Collaborative_Filter()
    col_filter.init_from_input("aaaaa")





_main()
