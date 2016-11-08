import math


VHIGH = 4.0
HIGH = 3.0
MED = 2.0
LOW = 1.0

FIVEMORE = 5.0
MORE = 6.0

SMALL = 1.0
BIG = 3.0

PARANUM = 6


def getBuyingInt(string):
    return {
        "vhigh" : VHIGH,
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]

def getMaintInt(string):
    return {
        "vhigh" : VHIGH,
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]

def getDoorsInt(string):
    return {
        "2" : 2.0,
        "3": 3.0,
        "4" : 4.0,
        "5more" : FIVEMORE,
    }[string]

def getPersonsInt(string):
    return {
        "2" : 2.0,
        "4" : 4.0,
        "more" : MORE,
    }[string]

def getLugInt(string):
    return {
        "small" : SMALL,
        "med" : MED,
        "big" : BIG,
    }[string]

def getSafetyInt(string):
    return {
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]


def getBuyingString(enumInt):
    return {
        VHIGH: "vhigh",
        HIGH: "high",
        MED: "med",
        LOW: "low",
    }[enumInt]

def getMaintString(enumInt):
    return {
        VHIGH: "vhigh",
        HIGH: "high",
        MED: "med",
        LOW: "low",
    }[enumInt]

def getDoorsString(enumInt):
    return {
        2: "2",
        3: "3",
        4: "4",
        FIVEMORE: "5more",
    }[enumInt]

def getPersonsString(enumInt):
    return {
        2: "2",
        4: "4",
        MORE: "more",
    }[enumInt]

def getLugString(enumInt):
    return {
        SMALL: "small",
        MED: "med",
        BIG: "big",
    }[enumInt]

def getSafetyString(enumInt):
    return {
        HIGH: "high",
        MED: "med",
        LOW: "low",
    }[enumInt]


def parseCar(line):
    elems = line.strip().split(",")
    return (
        getBuyingInt(elems[0]),
        getMaintInt(elems[1]),
        getDoorsInt(elems[2]),
        getPersonsInt(elems[3]),
        getLugInt(elems[4]),
        getSafetyInt(elems[5]),
        elems[6]
    )

def carEnumToListString(car):
    a1

def calDistance(car1, car2):
    sum = 0
    index = 0
    while index < PARANUM:
        sum += ((car1[index] - car2[index]) * (car1[index] - car2[index]))
        index += 1
    return math.sqrt(sum)

def allocateCar(centroids, car):
    min = float("inf")
    minIdx = -1
    index = 0
    for centroid in centroids:
        distance = calDistance(centroid, car)
        if distance < min:
            min = distance
            minIdx = index
        index += 1
    return minIdx

def clustering(centroids, cars):
    clusters = []
    num = len(centroids)
    index = 0
    while index < num:
        clusters.append([])
        index += 1
    for car in cars:
        clusterIdx = allocateCar(centroids, car)
        clusters[clusterIdx].append(car)
    return clusters

def calNewCentroid(cluster):
    base = [0, 0, 0, 0, 0, 0]
    num = len(cluster)
    for car in cluster:
        index = 0
        while index < PARANUM:
            base[index] += car[index]
            index += 1

    index = 0
    while index < 6:
        base[index] /= num
        index += 1

    return (base[0], base[1], base[2], base[3], base[4], base[5], "unknow")

def assignName(cluster):
    count = {
        "unacc": 0,
        "acc": 0,
        "good": 0,
        "vgood": 0,
    }
    for car in cluster:
        count[car[6]] += 1

    if count["unacc"] > count["acc"]:
        max1 = "unacc"
    else:
        max1 = "acc"

    if count["good"] > count["vgood"]:
        max2 = "good"
    else:
        max2 = "vgood"

    if count[max1] > count[max2]:
        return max1
    else:
        return max2

def WrongNumInCluster(cluster, name):
    num = 0
    for car in cluster:
        if car[6] != name:
            num += 1
    return num

def outputCluster(name, cluster, outputFile):
    stream = ""
    stream += "cluster: " + name + "\n"
    for car in cluster:
        stream += str(list(car)) + "\n"
    stream += "\n\n"
    with open(outputFile, "a") as fp:
        fp.write(stream)

def outputWrongs(num, outputFile):
    stream = ""
    stream += "Number of points wrongly assigned:\n"
    stream += str(num) + "\n"
    with open(outputFile, "a") as fp:
        fp.write(stream)

def _main():
    # filename = sys.argv[1]
    # support = int(sys.argv[2])
    # bucket_size = int(sys.argv[3])

    dataFilename = "input_car.txt"
    initialFilename = "initialPoints.txt"
    k = 4
    iter = 10

    outputFile = "output"

    inputLines = []
    initialLines = []
    with open(dataFilename, "r") as fp:
        inputLines = fp.readlines()

    with open(initialFilename, "r") as fp:
        initialLines = fp.readlines()

    cars = []
    for line in inputLines:
        cars.append(parseCar(line))

    centroids = []
    for line in initialLines:
        centroids.append(parseCar(line))

    iterIdx = 0
    clusters = []
    while iterIdx < iter:
        clusters = clustering(centroids, cars)
        centroids = []
        for cluster in clusters:
            centroids.append(calNewCentroid(cluster))
        iterIdx += 1

    names = []
    for cluster in clusters:
        names.append(assignName(cluster))
        outputCluster(names[-1], cluster, outputFile)

    index = 0
    total = 0
    for cluster in clusters:
        total += WrongNumInCluster(cluster, names[index])
        index += 1
    outputWrongs(total, outputFile)

_main()




















