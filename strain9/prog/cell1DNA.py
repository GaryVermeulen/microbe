# cell1DNA.py
#

import os
import pickle
import random


class Food:
    # We'll see if this works better or not...
    def __init__(
        self,
        #/foodFile
        foodFile = '',
        foodFileList = [],
        thisFood = 0,
        isPrime = False,
        runningP = 0,
        isPrimeTotal = 0,
        starvingCheck = 25
        ):

        self.foodFileList = foodFileList
        self.foodFile = self.setFoodFile(__file__)
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal
        self.starvingCheck = starvingCheck

    # How instances of the class are serialized and deserialized (pickles)
    def __reduce__(self):
        return (self.__class__, (self.foodFile, self.foddFileList, self.thisFood, self.isPrime, self.runningP, self.isPrimeTotal))

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
        print("foodFile: ", foodFile)
        print("foodFileList: ", self.foodFileList)

        while foodFile in self.foodFileList:
            random_int = random.randint(0, int(numDataFiles) - 1)
            foodFile = "dataFile" + str(random_int) + ".txt"

        return foodFile

    def printAll(self):
        print('foodFile: ', self.foodFile)
        print('foodFileList: ', self.foodFileList)
        print('thisFood: ', self.thisFood)
        print('isPrime: ', self.isPrime)
        print('runningP: ', round(self.runningP, 2))
        print('isPrimeTotal: ', self.isPrimeTotal)
        print('starvingCheck: ', self.starvingCheck)
        
    def metabolize(self, loopCnt):

        self.thisFood, self.isPrime = eatFood(loopCnt, self.foodFile)
        
        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / loopCnt) * 100
        
        return

    def changeFoodSource(self, loopCnt):

        print("Change food source--assumption that I am not truly fat-n-happy.")
        print("foodFile: ", self.foodFile)
        print("foodFileList: ", self.foodFileList)
        self.foodFileList.append(self.foodFile)
        
        self.foodFile = self.setFoodFile(__file__)

        print("   foodFile: ", self.foodFile)
        print("   foodFileList: ", self.foodFileList)

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

# Moved to class
#/STARVINGCHECK
##starvingCheck = 25

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
def loadData(foodFile):

    dataFood = []

    with open("data/" + foodFile, "r") as f:
        for line in f:
            dataFood.append(line.strip("\n"))

    return dataFood

# Attempt to emulate consumption (eating)
#
def eatFood(loopCnt, foodFile):

    dataFood = loadData(foodFile)
    thisFood = dataFood[loopCnt]
    isPrime = isNumPrime(thisFood)
    
    return thisFood, isPrime
