
VHIGH = 4
HIGH = 3
MED = 2
LOW = 1

FIVEMORE = 5
MORE = 6

SMALL = 1
BIG = 3


def getBuying(string):
    return {
        "vhigh" : VHIGH,
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]

def getMaint(string):
    return {
        "vhigh" : VHIGH,
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]

def getDoors(string):
    return {
        "2" : 2,
        "3": 3,
        "4" : 4,
        "5more" : FIVEMORE,
    }[string]

def getPersons(string):
    return {
        "2" : 2,
        "4" : 4,
        "more" : MORE,
    }[string]

def getLug(string):
    return {
        "small" : SMALL,
        "med" : MED,
        "big" : BIG,
    }[string]

def getSafety(string):
    return {
        "high": HIGH,
        "med" : MED,
        "low" : LOW,
    }[string]

def parseCar(line):
    elems = line.strip().split(",")
    return (
        getBuying(elems[0]),
        getMaint(elems[1]),
        getDoors(elems[2]),
        getPersons(elems[3]),
        getLug(elems[4]),
        getSafety(elems[5]),
        elems[6]
    )


def _main():
    # filename = sys.argv[1]
    # support = int(sys.argv[2])
    # bucket_size = int(sys.argv[3])

    dataFilename = "input_car.txt"
    initialFilename = "initialPoints.txt"
    k = 4
    iter = 10


    inputLines = []
    initialLines = []
    with open(dataFilename, "r") as fp:
        inputLines = fp.readlines()

    with open(initialFilename, "r") as fp:
        initialLines = fp.readlines()

    inputCars = []
    for line in inputLines:
        inputCars.append(parseCar(line))

    initialPoints = []
    for line in initialLines:
        initialPoints.append(parseCar(line))



_main()




















