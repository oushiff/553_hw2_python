import sys
#from functools import reduce
import itertools
import json



def init_dict(dict, bucket_size):
    i = 0
    while i < bucket_size:
        dict[i] = 0
        i += 1


def elem_std(elem):
    return elem.strip()

def is_validate(elem, res, num):
    if num == 1:
        return True
    for sub_elem in itertools.combinations(elem, num - 1):
        if sub_elem not in res[num - 1]:
            return False
    return True

def freq_set_to_str(freq_set):
    return "[" + ", ".join(map(str, map(list, sorted(list(freq_set))))) + "]"


def find_freq_item_set():
    pass



def output(dict_1, dict_2, freq_set):
    with open("output_multihash.txt", "a") as file:
        json.dump(dict_1, file)
        file.write("\n")
        json.dump(dict_2, file)
        file.write("\n")
        file.write(freq_set_to_str(freq_set))
        file.write("\n\n")
        #print(sorted(list(freq_set)))



def _main():
    # filename = sys.argv[2];
    # support = sys.argv[3];
    # bucket_size = sys.argv[4];

    filename = "input.txt"
    support = 4
    bucket_size = 5

    with open(filename, 'r') as input:
        lines = input.readlines()




_main()