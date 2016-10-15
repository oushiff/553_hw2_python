import sys
#from functools import reduce
import itertools
import json
import random


def init_dict(dict, bucket_size):
    i = 0
    while i < bucket_size:
        dict[i] = 0
        i += 1

def hash_func_1(x):
    return ord(x.strip()) + 1

def hash_func_2(x):
    return ord(x.strip()) * 9


def former_freq_check(elem, freq_set, num):
    if num == 1:
        return True
    for sub_elem in itertools.combinations(elem, num - 1):
        if sub_elem not in freq_set:
            return False
    return True

def freq_set_to_str(freq_set):
    return "[" + ", ".join(map(str, map(list, sorted(list(freq_set))))) + "]"

def elem_std(elem):
    return elem.strip()

def input_to_std(lines):
    std_lines = []
    for line in lines:
        line = sorted(map(elem_std, line.split(",")))
        std_lines.append(line)
    return std_lines

def sample_lines(lines, rate):
    size = len(lines)
    sample_index = random.sample(range(size), int(rate * size))
    sampled_std_lines = []
    for index in sample_index:
        sampled_std_lines.append(lines[index])
    return  sampled_std_lines

def output(time, fraction, res):
    with open("output_toivonen.txt", "a") as file:
        file.write(str(time) + "\n")
        file.write(str(fraction) + "\n")
        for freq_set in res:
            file.write(freq_set_to_str(freq_set))
            file.write("\n\n")

def find_freq_candidate(sampled_std_lines, num, former_freq, bucket_size, new_support):
    dict_1 = {}
    dict_2 = {}

    init_dict(dict_1, bucket_size)
    init_dict(dict_2, bucket_size)

    for line in sampled_std_lines:
        for elem in itertools.combinations(line, num):
            if not former_freq_check(elem, former_freq, num):
                continue
            key_1 = sum(map(hash_func_1, elem)) % bucket_size
            dict_1[key_1] += 1
            key_2 = sum(map(hash_func_2, elem)) % bucket_size
            dict_2[key_2] += 1

    freq_map = {}

    for line in sampled_std_lines:
        for elem in itertools.combinations(line, num):
            if not former_freq_check(elem, former_freq, num):
                continue
            if dict_1[sum(map(hash_func_1, elem)) % bucket_size] < new_support or dict_2[
                        sum(map(hash_func_2, elem)) % bucket_size] < new_support:
                continue
            if elem in freq_map:
                freq_map[elem] += 1
            else:
                freq_map[elem] = 1

    freq_candidate = {}
    for key, value in freq_map.items():
        if value >= new_support:
            freq_candidate[key] = 0

    return freq_candidate

def _main():
    filename = sys.argv[1]
    support = int(sys.argv[2])

    # filename = "input.txt"
    # support = 10

    fraction = 0.5
    lower_rate = 0.35
    max_try = 50000
    does_finished = False

    with open(filename, 'r') as input:
        lines = input.readlines()
    std_lines = input_to_std(lines)

    res = []

    time = 1
    while time < max_try:

        sampled_std_lines = sample_lines(std_lines, fraction)
        bucket_size = len(sampled_std_lines) * 5

        former_freq = set()
        res = []
        is_fail = False

        num = 1
        while True:

            freq_candidate = find_freq_candidate(sampled_std_lines, num, former_freq, bucket_size, support * lower_rate)

            negative_border = {}

            for line in std_lines:
                for elem in itertools.combinations(line, num):
                    if not former_freq_check(elem, former_freq, num):
                        continue
                    if elem in freq_candidate:
                        freq_candidate[elem] += 1
                    else:
                        if elem in negative_border:
                            negative_border[elem] += 1
                        else:
                            negative_border[elem] = 1

            former_freq = set()
            for key, value in freq_candidate.items():
                if value >= support:
                    former_freq.add(key)
                # the reason of commenting out the two lines below
                # is the value < support cannot make is_fail = True
                # else:
                #     negative_border[key] = value

            for key, value in negative_border.items():
                if value >= support:
                    is_fail = True

            if is_fail == True:
                break

            if len(former_freq) == 0:
                does_finished = True
                break

            res.append(former_freq)
            num += 1

        if does_finished == True:
            break
        time += 1

    if does_finished == True:
        output(time , fraction, res)


_main()