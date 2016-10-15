import sys
import itertools
import json

def init_dict(dict, bucket_size):
    i = 0
    while i < bucket_size:
        dict[i] = 0
        i += 1

def hash_func_1(x):
    return ord(x.strip()) + 1

def hash_func_2(x):
    return ord(x.strip()) * 9

def elem_std(elem):
    return elem.strip()

def is_validate(elem, freq_set, num):
    if num == 1:
        return True
    for sub_elem in itertools.combinations(elem, num - 1):
        if sub_elem not in freq_set:
            return False
    return True

def freq_set_to_str(freq_set):
    return "[" + ", ".join(map(str, map(list, sorted(list(freq_set))))) + "]"

def output(dict_1, dict_2, freq_set):
    with open("output_multihash.txt", "a") as file:
        json.dump(dict_1, file)
        file.write("\n")
        json.dump(dict_2, file)
        file.write("\n")
        file.write(freq_set_to_str(freq_set))
        file.write("\n\n")

def _main():
    filename = sys.argv[1]
    support = int(sys.argv[2])
    bucket_size = int(sys.argv[3])

    # filename = "input.txt"
    # support = 10
    # bucket_size = 30

    with open(filename, 'r') as input:
        lines = input.readlines()

    former_freq = set()
    num = 1
    while True:
        dict_1 = {}
        dict_2 = {}

        init_dict(dict_1, bucket_size)
        init_dict(dict_2, bucket_size)

        for line in lines:
            elems = sorted(map(elem_std, line.split(",")))
            for elem in itertools.combinations(elems, num):
                if not is_validate(elem, former_freq, num):
                    continue
                key_1 = sum(map(hash_func_1, elem)) % bucket_size
                dict_1[key_1] += 1
                key_2 = sum(map(hash_func_2, elem)) % bucket_size
                dict_2[key_2] += 1

        freq_map = {}

        for line in lines:
            elems = sorted(map(elem_std, line.split(",")))
            for elem in itertools.combinations(elems, num):
                if not is_validate(elem, former_freq, num):
                    continue
                if dict_1[sum(map(hash_func_1, elem)) % bucket_size] < support or dict_2[sum(map(hash_func_2, elem)) % bucket_size] < support:
                    continue
                if elem in freq_map:
                    freq_map[elem] += 1
                else:
                    freq_map[elem] = 1


        former_freq = set()
        for key, value in freq_map.items():
            if value >= support:
                former_freq.add(key)

        if len(former_freq) == 0:
            break

        output(dict_1, dict_2, former_freq)

        num += 1


_main()