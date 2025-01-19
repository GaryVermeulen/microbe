# cell1Body.py
#
# "Evolved" from cellAdd.py
#

import os
import sys
import time
import shutil
import random
import importlib
import fcntl
from subprocess import call


fList = "/home/gary/src/strain9/txt/fileList.txt"


class Cell:

    def __init__(
        self,
        population = 0,
        basePath = '',
        baseFile = '',
        parent = '',
        dnaFile = '',
        dnaModule = '',
        mTimeStart = '',
        loopCnt = 1,
        myChildren = [],
        foodList = [],
        windowSize = 5,
        windowList = [],
        fatAndHappy = False 
        ):
        
        self.population = population
        self.basePath = self.setBasePath(__file__)
        self.baseFile = self.setBaseFile(__file__)
        self.parent = parent
        self.dnaFile = dnaFile
        self.dnaModule = dnaModule
        self.mTimeStart = mTimeStart
        self.loopCnt = loopCnt
        self.myChildren = myChildren
        self.foodList = foodList
        self.windowSize = windowSize
        self.windowList = windowList
        self.fatAndHappy = fatAndHappy

    def setBasePath(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        basePath = f[:res[-1]]
        return basePath

    def setBaseFile(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        baseFile = f[res[-1]:]
        baseFile = baseFile[1:]
        return baseFile

    def __reduce__(self):
        return (self.__class__, (self.population, self.basePath, self.baseFile,
                                 self.parent, self.dnaFile, self.dnaModule, self.mTimeStart,
                                 self.loopCnt, self.myChildren, self.foodList,
                                 self.windowSize, self.windowList, self.fatAndHappy))

    def printAll(self):
        print("population: ", self.population)
        print("basePath: ", self.basePath)
        print("baseFile: ", self.baseFile)
        print("parent: ", self.parent)
        print("dnaFile: ", self.dnaFile)
        print("dnaModule: ", self.dnaModule)
        print("mTimeStart: ", self.mTimeStart)
        print("loopCnt: ", self.loopCnt)
        if len(self.myChildren) > 0:
            print("myChildren:")
            for c in self.myChildren:
                print(c)
        else:
            print("No Children.")
        print("foodList len: ", len(self.foodList))
        print("windowSize: ", self.windowSize)
        print("windowList: ", self.windowList)
        print("fatAndHappy: ", self.fatAndHappy)

    def setPopulation(self, stopReplication):
        if dna.stopReplication == 0:
            self.population = 0
        else:
            self.population = len([f for f in os.listdir(self.basePath) if os.path.isfile(os.path.join(self.basePath, f))])

    def toReplicate(self, MAXPOP, foodObj):
        if self.population < (MAXPOP - 5):        
            
            random_int = random.randint(1, 120)
            
            if (random_int == self.loopCnt) or (self.loopCnt % 25 == 0): #(loopCnt == 100): # One free pass at 100
                if (self.loopCnt % 25 == 0): #(loopCnt == 100): # Reduce odds with "coin flip"
                    random_coin = random.randint(0, 1)
                    if random_coin == 1:
                        print("Won multiple of 25 - 50/50 coin toss, Replicate. ", random_coin)
                        replicate(self, foodObj)
                    else:
                        print("Lost multiple of 25 - 50/50 coin toss, no replication. ", random_coin)
                else:
                    print("Replicating randomly at: ", random_int)
                    replicate(self, foodObj)
        else:
            print("Max Population (-5) Exceeded, no further replications: " + str(self.population))


    def loopBody(self, dna, foodObj):

        print("Top of loopBody, foodObj.printAll(): ")
        foodObj.printAll()
        print('---------')
        self.setPopulation(dna.stopReplication)
        self.toReplicate(dna.MAXPOP, foodObj)

        # What to do if fat-and-happy...?
        # Extend ttl, sleep more, starvingCheck less?
        self.prosperityCheck(dna, foodObj)

        if not self.fatAndHappy:
            print("NOT self.fatAndHappy: ", self.fatAndHappy)
            foodObj.changeFoodSource(thisCell.loopCnt)
                   
        foodObj.metabolize(thisCell.loopCnt)

        self.foodList.append(foodObj.thisFood)
       
        print('--- foodObj.printAll():')
        foodObj.printAll()
        print('--- thisCell.printAll():')
        self.printAll()
        print('Running: parent: {}, ttl: {}, baseFile: {}, sleepTime: {}, DNA: {}, loopCnt: {}, thisFood: {}, isPrime: {}, runningP: {}'.format(
            self.parent, dna.ttl, self.baseFile, dna.sleepTime, self.dnaFile, self.loopCnt, foodObj.thisFood, foodObj.isPrime, round(foodObj.runningP, 2)))

        # Write to log file
        #  parent, TTL, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime
        writeLog(str(self.parent) + ',' + str(dna.ttl) + ',' + self.baseFile + ',' + str(dna.sleepTime) + ',' + str(self.dnaFile) + ',' +
                 str(self.loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) + ',' + str(round(foodObj.runningP, 2)) + '\n')

        time.sleep(dna.sleepTime) # Small delay to reduce excessive CPU usage

        self.loopCnt += 1

        self.checkOverpopulation(dna.MAXPOP)

    def prosperityCheck(self, dna, foodObj):

        self.fatAndHappy = True
        
        if (self.loopCnt % foodObj.starvingCheck == 0) and (foodObj.runningP < 100.0):
            self.windowList = self.foodList[-5:]
            #print("windowLst: ", self.windowList)
            for n in self.windowList:
                if not dna.isNumPrime(n):
                    self.fatAndHappy = False
                    break             
        return

    def checkOverpopulation(self, MAXPOP):
        
        self.population = len([f for f in os.listdir(self.basePath) if os.path.isfile(os.path.join(self.basePath, f))])
        if self.population > MAXPOP:
            for c in self.myChildren:
                print(c)
                writeLog("#" + c[0] + "," + c[1])

            sys.exit("Max Population Exceeded: " + str(self.population))

    def setDNA(self):
        if self.baseFile == "cell1Body.py": # First cell -- rewrite list file
            self.parent = "cell1Body.py"
            self.dnaFile = "cell1DNA.py"
            self.dnaModule = "cell1DNA"

            fileEntry = "1" + ",cell1Body.py" + ",cell1Body.py," + self.dnaFile + "\n"

            filer = open(fList, "w")
            filer.writelines(str(fileEntry))
            filer.close()
        else:
            self.parent, lastFile, lastDNAFile = getLastFile(self.baseFile)
        
            fileNum = getFileNumber(self.baseFile)
            self.dnaFile = "cell" + str(fileNum) + "DNA.py"
            self.dnaModule = "cell" + str(fileNum) + "DNA"
            

def getFileNumber(file):

    bx = [i for i in range(len(file)) if file.startswith("B", i)]
    bIdx = bx[0]
    cIdx = 0
    fileNumber = file[cIdx + 4:bIdx]

    return fileNumber


def isFileLocked(file_path):
    try:
        with open(file_path, "r") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return False
    except BlockingIOError:
        return True


def writeLog(fInput):

    whoami = __file__
    baseStr = whoami[:-7] # remove the Base.py
    newStr = baseStr + "Log.txt"
    outFile = open(newStr, "a")
    outFile.writelines(str(fInput))
    outFile.close()

    return


def readDNAFile(fName):

    fileLines = []

    with open(fName, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


def getLastFile(baseFile):

    fLst = []

    while isFileLocked(fList):
        time.sleep(1)        
        if not isFileLocked(fList):
            break

    with open(fList, "r") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        fileContent = file.read()
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    file.close()

    fileLines = fileContent.split("\n")

    for line in fileLines:
        #print("line: ", line)
        #line = line.replace("\n", "")
        lineLst = line.split(',')
        if len(lineLst) == 4:
            #print(">{}<".format(lineLst))
            fLst.append(lineLst)

    # Get last entry
    indxNum = fLst[-1][0]
    parent = fLst[-1][1]
    lastFile = fLst[-1][2]
    lastDNA = fLst[-1][3]

    # Ensure a newer process didn't already beat us to the punch 
    baseFileNum = getFileNumber(baseFile)
    lastFileNum = getFileNumber(lastFile)

    if baseFileNum != lastFileNum:
        print("baseFileNum and lastFileNum do not match, so baseFileNum overrides lastFileNum if baseFileNum less than lastFileNum: ")
        print("baseFile: {}; baseFileNum: {}".format(baseFile, baseFileNum))
        print("lastFile: {}; lastFileNum: {}".format(fLst[-1], lastFileNum))
        #print("getting correct file entery...")
        #for i in fLst:
        #    if i[0] == baseFileNum:
        #        print("Found correct file enter: ", i)
        #        # Setting correct entry
        #        indxNum = i[0]
        #        parent = i[1]
        #        lastFile = i[2]
        #        lastDNA = i[3]
    else:
        print("Numbers match; baseNum: {}; lastNum: {}".format(baseFileNum, lastFileNum))
    
    return parent, lastFile, lastDNA


def setNextFile(baseFile, lastFile, lastDNA):
    
    # Extract the number from the file name
    bx = [i for i in range(len(lastFile)) if lastFile.startswith("B", i)]
    bIdx = bx[0]
    cIdx = 0

    head = lastFile[:4] # pick off cell
    tail = lastFile[-7:] # pick off Body.py
        
    num = lastFile[cIdx + 4:bIdx]
    nextNum = int(num) + 1

    # Next file names
    newFile = head + str(nextNum) + tail
    newDNA = head + str(nextNum) + "DNA.py"

    # Append to file
    fileEntry = str(nextNum) + "," + baseFile + "," + newFile + "," + newDNA + "\n"

    while isFileLocked(fList):
        sleep(1)
        if not isFileLocked(fList):
            break

    with open(fList, "a") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        file.write(fileEntry)
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    file.close()

    return newFile, newDNA


def mutateDNAFile(newDNA, newValue, dnaPart):
    # Input: (foodObj, dna.starvingCheck, direction) 
    """
    file = readDNAFile(newDNA)
    found = False
    newFile = []

    if dnaPart == "foodFile":
        for i in range(len(file)):
            if file[i].strip() == "#/foodFile":
                #print("FOUND: ", file[i])
                newFile.append(file[i])
                newFile.append("        foodFile = " + str(newValue) + ",")
                found = True
            else:
                #print("NF: ", file[i])
                if found:
                    found = False
                    continue
                newFile.append(file[i])
    elif dnaPart == "STARVINGCHECK":
        for i in range(len(file)):
            if file[i].strip() == "#/STARVINGCHECK":
                #print("FOUND: ", file[i])
                newFile.append(file[i])
                newFile.append("starvingCheck = " + str(newValue))
                found = True
            else:
                #print("NF: ", file[i])
                if found:
                    found = False
                    continue
                newFile.append(file[i])
    else:
        print("Invalid dnaPart: {}; No mutation available.".format(dnaPart))
        return

    with open(newDNA, "w") as outFile:
        for l in newFile:
            outFile.write(l + "\n")
    outFile.close()
    """

    foodObj.foodFile = foodObj.setFoodFile(__file__)

    print("Reset foodObj.foodFile: ", foodObj.foodFile)
    
    return 


def replicate(thisCell, foodObj):
    
    print("-----")
    print("replicate:")

    thisCell.parent, lastFile, lastDNA = getLastFile(thisCell.baseFile)
    newFile, newDNA = setNextFile(thisCell.baseFile, lastFile, lastDNA)

    print("thisCell:")
    thisCell.printAll()
    print("foodObj: ")
    foodObj.printAll()

    print("B4COPY newFile: ", newFile)
    print("B4COPY newDNA: ", newDNA)

    thisCell.myChildren.append((newFile, newDNA))
        
    # Create file (replicant)
    shutil.copyfile(lastFile, newFile)

    # Create matching DNA file
    shutil.copyfile(lastDNA, newDNA)
    
    # Mutate child DNA?
    #
    """
    New mutation to be based on the % of primes found...
    """
    #if foodObj.runningP < 100.0:
        #if foodObj.foodFile == 6:
        #    print("Attempted mutation failed: Cannot roll whichFood higher than: ", foodObj.foodFile)
        #else:
        #    newFileNum = int(foodObj.foodFile) + 1
        #    mutateDNAFile(newDNA, newFileNum, "foodFile")
        #    print("Mutated: ", newFileNum)
     
    print("Starting replicated file: ", newFile)
    print("Replicated DNA file: ", newDNA)

    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newFile + "; bash"
    call(callStr)
        
    return


if __name__ == "__main__":

    print("--- START __main__ CELL INSTANCE ---")
    start_time = time.time()
    thisCell = Cell()
    thisCell.setDNA()

    dna = importlib.import_module(thisCell.dnaModule)
    
    # Capture cellnDNA.py modified time
    thisCell.mTimeStart = os.path.getmtime(thisCell.dnaFile)
    
    foodObj = dna.Food()
    end_time = start_time + dna.ttl
    foodObj.printAll()

    while time.time() < end_time:
        print("----------TopOfLoop")
        thisCell.loopBody(dna, foodObj)
 
    # Write children to log file
    print("Time to die...")
    for c in thisCell.myChildren:
        print(c)
        writeLog("#" + c[0] + "," + c[1])
