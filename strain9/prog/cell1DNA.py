# cell1DNA.py
#

import os
import pickle
import random


class Food:
    # We'll see if this works better or not...
    def __init__(
        self,
        #/WHICHFILE
        whichFile = '',
        loopCnt = 1,
        thisFood = 0,
        isPrime = False,
        runningP = 0,
        isPrimeTotal = 0
        ):

        self.whichFile = self.setFoodFile(__file__)
        self.loopCnt = loopCnt
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal

    # How instances of the class are serialized and deserialized (pickles)
    def __reduce__(self):
        return (self.__class__, (self.whichFile, self.loopCnt, self.thisFood, self.isPrime, self.runningP, self.isPrimeTotal))

    def setFoodFile(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        basePath = f[:res[-1]]
        foodPath = basePath + "/data"
        print("foodPath: ", foodPath)
        numDataFiles = len(os.listdir(foodPath))
        print("numDataFiles: ",numDataFiles)

        random_int = random.randint(0, int(numDataFiles) - 1)

        foodFile = "dataFile" + str(random_int) + ".txt"

        return foodFile

    def printAll(self):
        print('whichFile: ', self.whichFile)
        print('loopCnt: ', self.loopCnt)
        print('thisFood: ', self.thisFood)
        print('isPrime: ', self.isPrime)
        print('runningP: ', round(self.runningP, 2))
        print('isPrimeTotal: ', self.isPrimeTotal)
        
    def metabolize(self):

        #self.loopCnt = loopCnt

        #print("Curent food source, whichFile: ", self.whichFile)
        #self.changeFoodSource()

        self.thisFood, self.isPrime = eatFood(self.loopCnt, self.whichFile)
        
        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / self.loopCnt) * 100
        
        return

    def changeFoodSource(self):

        print("Change food source?")

        #if (self.loopCnt % 25 == 0) and (self.runningP < 100.0):
        if (self.loopCnt % starvingCheck == 0) and (self.runningP < 100.0):
            if self.whichFile == 6:
                print("Cannot roll whichFood higher than: ", self.whichFile)
            else:
                self.whichFile = self.whichFile + 1
                print("Starving, rolled whichFile to: ", self.whichFile)
        else:
            print("Not yet...")

        return

    def getFile(self, f): # Not used here...~?
        fileLines = []

        #with open('../' + f, 'r') as inFile:
        with open(f, 'r') as inFile:
            for line in inFile:
                fileLines.append(line.strip("\n"))
        inFile.close()
        return fileLines

    

#/TTL
ttl = 120 # Seconds

# Need at least one second due to file opertions
#/SLEEPTIME
sleepTime = 1

# stopReplication:
# 0 allows replcation until MAXPOP (maximum file (cell) population)
# is reached (immediate stop of all cells).
# 1 stops replication, but allows existing cells to complete.
stopReplication = 1

# Typically 30 will not solve
# Typically 90 will solve
MAXPOP = 90 # Maximum file (cell) population

#/STARVINGCHECK
starvingCheck = 25

# Simple function now obsolete
#
def cellFunction(newNum):
    # Principal cell function using: add one
    #/START
    return newNum + 1
    #/END


# Prime number function
#
def isNumPrime(num):
    
    if int(num) > 1:
        for i in range(2, (int(num)//2)+1):
            if (int(num) % i) == 0:
                break
        else:
            return True

    return False


# Load data/food
#
def loadData(whichFile):
    
    """
    if whichFile == 1:
        file = 'pickles/dataFood1.p'
    elif whichFile == 2:
        file = 'pickles/dataFood2.p'
    elif whichFile == 3:
        file = 'pickles/dataFood3.p'
    elif whichFile == 4:
        file = 'pickles/dataFood4.p'
    elif whichFile == 5:
        file = 'pickles/dataFood5.p'
    elif whichFile == 6:
        file = 'pickles/dataFoodP.p'
    else:
        print("Invalid file selection. Defaulting to 1.")
        file = 'pickles/dataFood1.p'
        
    # Get data/food
    with open(file, 'rb') as f:
        dataFood = pickle.load(f)
    f.close()
    """

    dataFood = []

    with open("data/" + whichFile, "r") as f:
        for line in f:
            dataFood.append(line.strip("\n"))

    return dataFood

# Attempt to emulate consumption (eating)
#
def eatFood(loopCnt, whichFile):

    dataFood = loadData(whichFile)
    thisFood = dataFood[loopCnt]
    isPrime = isNumPrime(thisFood)
    
    return thisFood, isPrime
