# cell1DNA.py
#

import os
import pickle


class Food:
    # We'll see if this works better or not...
    def __init__(
        self,
        #/WHICHFILE
        whichFile = 1,
        loopCnt = 0,
        thisFood = 0,
        isPrime = False,
        runningP = 0,
        isPrimeTotal = 0
        ):

        self.whichFile = whichFile
        self.loopCnt = loopCnt
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal

    # How instances of the class are serialized and deserialized (pickles)
    def __reduce__(self):
        return (self.__class__, (self.loopCnt, self.thisFood, self.isPrime, self.runningP, self.isPrimeTotal))

    def printAll(self):
        print('whichFile: ', self.whichFile)
        print('loopCnt: ', self.loopCnt)
        print('thisFood: ', self.thisFood)
        print('isPrime: ', self.isPrime)
        print('runningP: ', self.runningP)
        print('isPrimeTotal: ', self.isPrimeTotal)

    def metabolize(self, loopCnt):

        self.loopCnt = loopCnt

        self.changeFoodSource()

        print("whichFile: ", self.whichFile)
        self.thisFood, self.isPrime = eatFood(self.loopCnt, self.whichFile)
        
        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / self.loopCnt) * 100
        
        return

    def changeFoodSource(self):

        print("Change food source?")
        
        #if self.loopCnt >= 10:
        #    if self.runningP < 100:
        #        self.whichFile = self.whichFile + 1
        #        print("Updated whichFile to: ", self.whichFile)

        print("Not yet...")

        return

    def getFile(self, f):
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

# Simple function now obsolete
#
def cellFunction(newNum):
    # Principal cell function using: add one
    #/START
    return newNum + 1
    #/END


# Prime number function
#
def isNumPrime1(num):
    
    retValue = False
    
    if num > 1:
        for i in range(2, (num//2)+1):
            if (num % i) == 0:
                break
        else:
            retValue = True

    return retValue


# Load data/food
#
def loadData(whichFile):

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

    return dataFood

# Attempt to emulate consumption (eating)
#
def eatFood(loopCnt, whichFile):

    dataFood = loadData(whichFile)
    thisFood = dataFood[loopCnt]
    isPrime = isNumPrime1(thisFood)
    
    return thisFood, isPrime
