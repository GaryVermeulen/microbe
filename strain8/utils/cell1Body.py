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


fList = "txt/fileList.txt"
myChildren = []


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
        myChildren = []
        ):
        
        self.population = population
        self.basePath = self.setBasePath(__file__)
        self.baseFile = self.setBaseFile(__file__)
        self.parent = parent
        self.dnaFile = dnaFile
        self.dnaModule = dnaModule
        self.mTimeStart = mTimeStart
        self.myChildren = myChildren

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
        return (self.__class__, (self.population, self.basePath, self.baseFile, self.parent, self.dnaFile, self.dnaModule, self.mTimeStart, self.myChildren))

    def printAll(self):
        print("population: ", self.population)
        print("basePath: ", self.basePath)
        print("baseFile: ", self.baseFile)
        print("parent: ", self.parent)
        print("dnaFile: ", self.dnaFile)
        print("dnaModule: ", self.dnaModule)
        print("mTimeStart: ", self.mTimeStart)
        if len(self.myChildren) > 0:
            print("myChildren:")
            for c in self.myChildren:
                print(c)
        else:
            print("No Children.")

    def setPopulation(self, stopReplication):
        if dna.stopReplication == 0:
            self.population = 0
        else:
            self.population = len([f for f in os.listdir(self.basePath) if os.path.isfile(os.path.join(self.basePath, f))])

    def toReplicate(self, MAXPOP, foodObj):
        if self.population < (MAXPOP - 5):        
            # Trying self-replication (typical max loop count is 120)
            random_int = random.randint(1, 120)
            # With sleepTime = 0 many more loops
            if (random_int == foodObj.loopCnt) or (foodObj.loopCnt % 25 == 0): #(loopCnt == 100): # One free pass at 100
                if (foodObj.loopCnt % 25 == 0): #(loopCnt == 100): # Reduce odds with "coin flip"
                    random_coin = random.randint(0, 1)
                    if random_coin == 1:
                        print("Won multiple of 100 - 50/50 coin toss, Replicate. ", random_coin)
                        replicate(self, foodObj)
                    else:
                        print("Lost multiple of 100 - 50/50 coin toss, no replication. ", random_coin)
                else:
                    print("Replicating randomly at: ", random_int)
                    replicate(self, foodObj)
        else:
            print("Max Population (-5) Exceeded, no further replications: " + str(self.population))

    def toSelfMutate(self, foodObj, starvingCheck):
        if (foodObj.loopCnt % starvingCheck == 0) and (foodObj.runningP < 100.0):
            print("Let's attempt to mutate starvingCheck...: ", starvingCheck)
            newValue = starvingCheck - 5
            if newValue <= 5: # Divide by zero check
                newValue = 5
            
            mutateWhichFile(thisCell.dnaFile, newValue, "STARVINGCHECK")
            
        mTimeNow = os.path.getmtime(thisCell.dnaFile)
        
        if self.mTimeStart < mTimeNow:
            print("!!! *** Mutation Detected: Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason was throwing an error
            #print("*** dna: ", dna)
            #print(sys.modules)
            importlib.reload(dna)
        
            # Hack
            #del sys.modules[dna] # This used to work when reload did not???
            ##dna = importlib.import_module(dnaModule)

            # Reset possibily mutated var's
            #sleepTime = dna.sleepTime
            #ttl       = dna.ttl
            #starvingCheck = dna.starvingCheck
            
            print("!!! *** Re-imported cellFunction and reset starvingCheck variable to:")
            #print("   local starvingCheck: ", starvingCheck)
            #print("   dna starvingCheck: ", dna.starvingCheck)
            self.mTimeStart = mTimeNow
        else:
            print("!!! *** No mutation detected.")

        return


    def checkOverpopulation(self, MAXPOP):
        #global myChildren
        
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
        sleep(1)        
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


def mutateWhichFile(newDNA, newValue, dnaPart):

    file = readDNAFile(newDNA)
    found = False
    newFile = []

    if dnaPart == "WHICHFILE":
        for i in range(len(file)):
            if file[i].strip() == "#/WHICHFILE":
                #print("FOUND: ", file[i])
                newFile.append(file[i])
                newFile.append("        whichFile = " + str(newValue) + ",")
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

    return


def replicate(thisCell, foodObj):
    #global myChildren
    
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
    if foodObj.runningP < 100.0:
        if foodObj.whichFile == 6:
            print("Attempted mutation failed: Cannot roll whichFood higher than: ", foodObj.whichFile)
        else:
            newFileNum = int(foodObj.whichFile) + 1
            mutateWhichFile(newDNA, newFileNum, "WHICHFILE")
            print("Mutated: ", newFileNum)
    
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

    while time.time() < end_time:
        print("----------TOL")

        thisCell.setPopulation(dna.stopReplication)
        thisCell.toReplicate(dna.MAXPOP, foodObj)
        
        print("dna.starvingCheck: ", dna.starvingCheck)
        thisCell.toSelfMutate(foodObj, dna.starvingCheck)        
        print("After self mutate: dna starvingCheck: ", dna.starvingCheck)
        
        foodObj.metabolize()
        print('---')
        foodObj.printAll()
        print('---')
        thisCell.printAll()
        print('Running: parent: {}, ttl: {}, baseFile: {}, sleepTime: {}, DNA: {}, loopCnt: {}, thisFood: {}, isPrime: {}, runningP: {}'.format(
            thisCell.parent, dna.ttl, thisCell.baseFile, dna.sleepTime, thisCell.dnaFile, foodObj.loopCnt, foodObj.thisFood, foodObj.isPrime, round(foodObj.runningP, 2)))

        # Write to log file
        #  parent, TTL, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime
        writeLog(thisCell.parent + ',' + str(dna.ttl) + ',' + thisCell.baseFile + ',' + str(dna.sleepTime) + ',' + str(thisCell.dnaFile) + ',' +
                 str(foodObj.loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) + ',' + str(round(foodObj.runningP, 2)) + '\n')

        time.sleep(dna.sleepTime) # Small delay to reduce excessive CPU usage

        foodObj.loopCnt += 1

        thisCell.checkOverpopulation(dna.MAXPOP)
 
    # Write children to log file
    for c in thisCell.myChildren:
        print(c)
        writeLog("#" + c[0] + "," + c[1])
