file1 = "output"
file2 = "outputSample.txt"


class MyCluster(object):
    def __init__(self):
        self.name = ""
        self.num = 0
        self.cars = []

    def setCluster(self, name, cars):
        #print(lines[0])
        self.name = name
        self.num = len(cars)
        self.cars = cars

    def printCluster(self):
        print(self.name.strip())
        print(self.num)
        for car in self.cars:
            print(car.strip())
        print("\n\n")

def initMatches(length):
    matches = []
    index = 0
    while index < length:
        matches.append(False)
        index += 1
    return matches

def splitLines(lines):
    wrongNum = 0
    clusters = []
    index = 0
    while index < len(lines):
        if lines[index] == "\n":
            index += 1
            continue
        if lines[index].strip() == "Number of points wrongly assigned:":
            wrongNum = int(lines[index + 1])
            break
        name = lines[index]
        index += 1
        tmp = []
        while lines[index] != "\n":
            tmp.append(lines[index])
            index += 1
        new_cluster = MyCluster()
        new_cluster.setCluster(name, tmp)
        clusters.append(new_cluster)
    return clusters, wrongNum

def compareCluster(cluster1, cluster2):
    if cluster1.num != cluster2.num:
        return False
    if cluster1.name != cluster2.name:
        return False
    cars1 = copy.deepcopy(cluster1.cars)
    cars2 = copy.deepcopy(cluster2.cars)
    while len(cars1)!= 0 and len(cars2)!= 0:
        index = 0
        doesFind = False
        while index < len(cars2):
            if cars1[-1].strip() == cars2[index].strip():
                doesFind = True
                cars1.pop()
                cars2.pop(index)
                break
            index += 1
        if not doesFind:
            return False
    if len(cars1)==0 and len(cars2)==0:
        return True
    else:
        return False

def compareClusters(clusters1, clusters2):
    matchesIdx1 = initMatches(len(clusters1))
    matchesIdx2 = initMatches(len(clusters2))
    unFind1 = []
    unFind2 = []
    index1 = 0
    while index1 < len(clusters1):
        findMatch = False
        index2 = 0
        while index2 <  len(clusters2):
            if matchesIdx2[index2]:
                index2 += 1
                continue
            findMatch = compareCluster(clusters1[index1], clusters2[index2])
            if findMatch == True:
                matchesIdx1[index1] = True
                matchesIdx2[index2] = True
                break
            index2 += 1
        if not findMatch:
            unFind1.append(clusters1[index1])
        index1 += 1

    index2 = 0
    while index2 < len(matchesIdx2):
        if not matchesIdx2[index2]:
            unFind2.append(clusters2[index2])
        index2 += 1
    return unFind1, unFind2


def _main():
    with open(file1, "r") as fp:
        lines1 = fp.readlines()

    with open(file2, "r") as fp:
        lines2 = fp.readlines()

    clusters1, wrongNum1 = splitLines(lines1)
    clusters2, wrongNum2 = splitLines(lines2)
    
    unFind1, unFind2 = compareClusters(clusters1, clusters2)

    success = True
    if len(unFind1) != 0:
        success = False
        print("UnFindNum in File1:  " + str(len(unFind1)))
        print("Doesn't Match in File1:")
        for cluster in unFind1:
            cluster.printCluster()
        print("\n\n\n\n\n\n")
    if len(unFind2) != 0:
        success = False
        print("UnFindNum in File2:  " + str(len(unFind2)))
        print("Doesn't Match in File2:")
        for cluster in unFind2:
            cluster.printCluster()
        print("\n\n\n\n\n\n")
    if wrongNum1 != wrongNum2:
        success = False
        print("wrongNum doesn't match!:")
        print(str(wrongNum1) + "   " + str(wrongNum2))

    if success:
        print("Success!")

_main()

