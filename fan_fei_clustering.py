import math
import sys

PARANUM = 6

def getBuyingInt(string):
    return {
        "vhigh" : 3.0,
        "high": 2.0,
        "med" : 1.0,
        "low" : 0.0,
    }[string]

def getMaintInt(string):
    return {
        "vhigh" : 3.0,
        "high": 2.0,
        "med" : 1.0,
        "low" : 0.0,
    }[string]

def getDoorsInt(string):
    return {
        "2" : 0.0,
        "3": 1.0,
        "4" : 2.0,
        "5more" : 3.0,
    }[string]

def getPersonsInt(string):
    return {
        "2" : 0.0,
        "4" : 1.0,
        "more" : 2.0,
    }[string]

def getLugInt(string):
    return {
        "small" : 0.0,
        "med" : 1.0,
        "big" : 2.0,
    }[string]

def getSafetyInt(string):
    return {
        "high": 2.0,
        "med" : 1.0,
        "low" : 0.0,
    }[string]


def getBuyingString(enumInt):
    return {
        3: "vhigh",
        2: "high",
        1: "med",
        0: "low",
    }[enumInt]

def getMaintString(enumInt):
    return {
        3: "vhigh",
        2: "high",
        1: "med",
        0: "low",
    }[enumInt]

def getDoorsString(enumInt):
    return {
        0: "2",
        1: "3",
        2: "4",
        3: "5more",
    }[enumInt]

def getPersonsString(enumInt):
    return {
        0: "2",
        1: "4",
        2: "more",
    }[enumInt]

def getLugString(enumInt):
    return {
        0: "small",
        1: "med",
        2: "big",
    }[enumInt]

def getSafetyString(enumInt):
    return {
        2: "high",
        1: "med",
        0: "low",
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
    elems = []
    elems.append(getBuyingString(car[0]))
    elems.append(getMaintString(car[1]))
    elems.append(getDoorsString(car[2]))
    elems.append(getPersonsString(car[3]))
    elems.append(getLugString(car[4]))
    elems.append(getSafetyString(car[5]))
    elems.append(car[6])
    return str(elems)

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
        stream += carEnumToListString(car) + "\n"
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
    dataFilename = sys.argv[1]
    initialFilename = sys.argv[2]
    k = int(sys.argv[3])
    iter = int(sys.argv[4])

    # dataFilename = "input_car.txt"
    # initialFilename = "initialPoints.txt"
    # k = 4
    # iter = 10

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

