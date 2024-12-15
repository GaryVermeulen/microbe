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
        isPrimeTotal = 0,
        highP = 0.0
        ):

        self.whichFile = whichFile
        self.loopCnt = loopCnt
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal
        self.highP = highP

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
        print('highP: ', self.highP)

    def metabolize(self, loopCnt):

        self.loopCnt = loopCnt

        self.changeFoodSource()

        print("Primary data/food.")
        self.thisFood, self.isPrime = eatFood(self.loopCnt, self.whichFile)
        
        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / self.loopCnt) * 100
        
        return

    def changeFoodSource(self):

        print("Change food source?")

        # Read current log file to see who has the high P%
        whoami = __file__
        files = []
        filesBrief = []
        testChar = "/"
        
        res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
        basePath = whoami[:res[-1]]
        fileList = os.listdir(basePath)

        #print("len fileList: ", len(fileList))

        for f in fileList:
            #print("raw f: ", f)
            if f[-7:] == "Log.txt":
                #print("f log: ", f)
                contents = self.getFile(f)

                #print("len contents: ", len(contents))
           
                listOfLines = []
                reducedLines = []
            
                for l in contents:
                    lineList = l.split(',')                
                    listOfLines.append(lineList)

                files.append((f, listOfLines))

        for f in files:
            filesBrief.append((f[0], f[1][-1]))

        filesBrief.sort()

        #highP = 0

        print("len filesBrief: ", len(filesBrief))
        for f in filesBrief:
            print("f: ", f)
            print("f[1][-1]: ", f[1][-1])
            print("self.highP: ", self.highP)
            self.highP = f[1][-1]

        print("---self.highP: ", self.highP)

        print("Not sure know yet...")

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
