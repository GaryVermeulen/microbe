# cell1DNA.py
#

import os
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
        starvingCheck = 25,
        avalonFound = False
        ):

        self.foodFileList = foodFileList
        self.avalonFound = avalonFound
        self.foodFile = foodFile
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal
        self.starvingCheck = starvingCheck
        
    # How instances of the class are serialized and deserialized (pickles)
    def __reduce__(self):
        return (self.__class__, (self.foodFile, self.foddFileList, self.thisFood,
                                 self.isPrime, self.runningP, self.isPrimeTotal,
                                 self.starvingCheck, self.avalonFound))

    def setFoodFile(self, f):  
        if self.avalonFound:
            print("Food: setFoodFile: avalonFound: {}, foodFile: {}".formatt(self.avalonFound, self.foodFile))
        else:
            print("Food: setFoodFile: avalonFound (not found): ", self.avalonFound)
            testChar = "/"
            res = [i for i in range(len(f)) if f.startswith(testChar, i)]
            basePath = f[:res[-1]]
            foodPath = basePath + "/data"
            print("Food: setFoodFile: foodPath: ", foodPath)
            numDataFiles = len(os.listdir(foodPath))
            print("Food: setFoodFile: numDataFiles: ", numDataFiles)

            random_int = random.randint(0, int(numDataFiles) - 1)
            foodFile = "dataFile" + str(random_int) + ".txt"
            
            while foodFile in self.foodFileList:
                random_int = random.randint(0, int(numDataFiles) - 1)
                foodFile = "dataFile" + str(random_int) + ".txt"

            print("Food: setFoodFile: foodFile: ", foodFile)
            print("Food: setFoodFileList: foodFileList: ", self.foodFileList)
        return foodFile

    def printAll(self):
        print('Food: foodFile: ', self.foodFile)
        print('Food: foodFileList: ', self.foodFileList)
        print('Food: thisFood: ', self.thisFood)
        print('Food: isPrime: ', self.isPrime)
        print('Food: runningP: ', round(self.runningP, 2))
        print('Food: isPrimeTotal: ', self.isPrimeTotal)
        print('Food: starvingCheck: ', self.starvingCheck)
        print('Food: avalonFound: ', self.avalonFound)
        
    def metabolize(self, loopCnt):
        if self.foodFile == '':
            self.foodFile = self.setFoodFile(__file__)
        self.thisFood, self.isPrime = eatFood(loopCnt, self.foodFile)
        
        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / loopCnt) * 100
        return

    def changeFoodSource(self, loopCnt):
        print("Change food source--assumption that I am not truly fat-n-happy.")
        print(" was   foodFile: ", self.foodFile)
        print(" was   foodFileList: ", self.foodFileList)
        self.foodFileList.append(self.foodFile)
        self.foodFile = self.setFoodFile(__file__)
        print(" is  foodFile: ", self.foodFile)
        print(" is  foodFileList: ", self.foodFileList)
        return
    

# Globals from first cell construct
#
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
#MAXPOP = 20 # Maximum file (cell) population

# Moved to class
#/STARVINGCHECK
##starvingCheck = 25

# Based on fatAndHappy (True) and runningP = 100
# Retain info on where is Avalon:
#/AVALON
AVALON = '?'

# Pheromone used as a shortcut to Avalon. Once a cell
# finds Avalon it will create a file as a marker for the
# other cells.
Pheromone = False

# 1st Simple function now obsolete
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


def isReadable(testFile):
    readableCount = 0
    nonreadableCount = 0

    with open(testFile, 'rb') as fp:
        data = fp.read(8)
    fp.close()
    
    decodedData = data.decode()

    for c in decodedData:
        if ord(c) >= 32 and ord(c) <= 126:
            readableCount += 1
        else:
            if ord(c) == 10:
                readableCount += 1
            else:
                nonreadableCount += 1
                
    if readableCount > nonreadableCount:
        return True

    return False    
    
# Load data/food
#
def loadData(foodFile):

    dataFood = []

    if isReadable("data/" + foodFile):

        with open("data/" + foodFile, "r") as f:
            for line in f:
                dataFood.append(line.strip("\n"))
    else:
        print("!!!! Unreadable data file: ", foodFile)

    return dataFood

# Attempt to emulate consumption (eating)
#
def eatFood(loopCnt, foodFile):

    dataFood = loadData(foodFile)

    print("eatFood: loopCnt: ", loopCnt)
    print("eatFood: len-dataFood: ", len(dataFood))

    if len(dataFood) == 0:
        print(" ********************* Food/data len is zero! *********************")
        isPrime = False
        thisFood = -10
        return thisFood, isPrime

    if loopCnt < len(dataFood):
        thisFood = dataFood[loopCnt]

        derivedNumber = classifier(thisFood)
        
        if derivedNumber == None:
            isPrime = False # Something other than a real number
            thisFood = 0
        else:
            isPrime = isNumPrime(thisFood)
            thisFood = derivedNumber
    else:
        print(" ********************* Food/data len is less than loopCnt! *********************")
        isPrime = False
        thisFood = -1
        
    return thisFood, isPrime

# Search avalon file
#
def search4Avalon(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Set Avalon file
#
def setAvalonFile(avalonFile):
    global AVALON

    print("setAvalonFile: avalonFile: ", avalonFile)

    file_path = search4Avalon("avalon.txt", "txt")
    
    if file_path:
        print("Avalon file already set:", file_path)
        print("   AVALON: ", AVALON)
    else:
        f = open("txt/avalon.txt", "w")
        f.write(str(avalonFile))
        f.close()
        AVALON = avalonFile
        print("Avalon file set to: ", avalonFile)
        print("   AVALON: ", AVALON)
    return

# Has Avalon been found, and if so set AVALON
def hasAvalonBeenFound():
    global AVALON

    file_path = search4Avalon("avalon.txt", "txt")

    print("hasAvalonBeenFound: file_path: ", file_path)
    
    if file_path:
        print("Avalon file already set:", file_path)
        if AVALON == "?":
            f = open("txt/avalon.txt", "r")
            AVALON = f.read()
            f.close()
            print("Did we set AVALON: ", AVALON)
        else:
            print("AVALON already set: ", AVALON)
        return True
    else:
        print("Avalon file not found: ", AVALON)
        
    return False

def classifier(inputNumber):

    if inputNumber.isdigit():
        return int(inputNumber)
    else:
        return None



