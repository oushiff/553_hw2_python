

def check(lines, start, cycle):
    base = lines[start]
    i = 0
    while (i * cycle + start) < len(lines):
        if not base == lines[i * cycle + start] :
            print(i * cycle + start)
            return False
        i += 1
    return True

def get_max(lines, start, cycle):
    maxNum = -1
    i = 0
    while (i * cycle + start) < len(lines):
        num = int(lines[i * cycle + start])
        if num > maxNum:
            maxNum = num
        i += 1
    return maxNum

def _main():
    filename = "output_toivonen.txt"
    with open(filename, "r") as fp:
        lines = fp.readlines()

    cycle = 12
    
    res = check(lines, 2, cycle)
    print(res)
    res = check(lines, 4, cycle)
    print(res)
    res = check(lines, 6, cycle)
    print(res)
    res = check(lines, 8, cycle)
    print(res)
    res = check(lines, 10, cycle)
    print(res)

    res = get_max(lines, 0, cycle)
    print(res)


_main()

