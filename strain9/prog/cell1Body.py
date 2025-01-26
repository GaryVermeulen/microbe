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
        self.basePath = f[:res[-1]]
        return

    def setBaseFile(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        baseFile = f[res[-1]:]
        self.baseFile = baseFile[1:]
        return

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
        return

    def writeLog(self, fInput):
        whoami = __file__
        baseStr = whoami[:-7] # remove the Base.py
        newStr = baseStr + "Log.txt"
        outFile = open(newStr, "a")
        outFile.writelines(str(fInput))
        outFile.close()
        return

    def getFileNumber(self, file):
        bx = [i for i in range(len(file)) if file.startswith("B", i)]
        bIdx = bx[0]
        cIdx = 0
        fileNumber = file[cIdx + 4:bIdx]
        return fileNumber

    def isFileLocked(self, file_path):
        try:
            with open(file_path, "r") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return False
        except BlockingIOError:
            return True

    def setPopulation(self, stopReplication):
        if dna.stopReplication == 0:
            self.population = 0
        else:
            self.population = len([f for f in os.listdir(self.basePath) if os.path.isfile(os.path.join(self.basePath, f))])
        return

    def toReplicate(self, MAXPOP, foodObj):
        if self.population < (MAXPOP - 5):        
            
            random_int = random.randint(1, 120)
            
            if (random_int == self.loopCnt) or (self.loopCnt % 25 == 0): #(loopCnt == 100): # One free pass at 100
                if (self.loopCnt % 25 == 0): #(loopCnt == 100): # Reduce odds with "coin flip"
                    random_coin = random.randint(0, 1)
                    if random_coin == 1:
                        print("Won multiple of 25 - 50/50 coin toss, Replicate. ", random_coin)
                        self.replicate(foodObj)
                    else:
                        print("Lost multiple of 25 - 50/50 coin toss, no replication. ", random_coin)
                else:
                    print("Replicating randomly at: ", random_int)
                    self.replicate(foodObj)
        else:
            print("Max Population (-5) Exceeded, no further replications: " + str(self.population))
        return

    def replicate(self, foodObj):
        print("-----")
        print("replicate:")

        childParent, childCell, childDNA = self.setNextFileEntry(thisCell.baseFile)

        self.myChildren.append((childCell, childDNA))
        
        # Create file (replicant)
        shutil.copyfile(self.baseFile, childCell)

        # Create matching DNA file
        shutil.copyfile(self.dnaFile, childDNA)
         
        print("Starting replicated file: ", childCell)
        print("Replicated DNA file: ", childDNA)

        callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + childCell + "; bash"
        call(callStr)        
        return

    def loopBody(self, dna, foodObj):
        self.setPopulation(dna.stopReplication)
        self.toReplicate(dna.MAXPOP, foodObj)

        # What to do if fat-and-happy...?
        # Extend ttl, sleep more, starvingCheck less?
        self.prosperityCheck(dna, foodObj)

        if not self.fatAndHappy:
            print("NOT self.fatAndHappy: ", self.fatAndHappy)
            if (self.loopCnt % foodObj.starvingCheck == 0) and (foodObj.runningP < 100.0):
                print("YES: Change food source.")
                foodObj.changeFoodSource(thisCell.loopCnt)
            else:
                print("NO: Change food source.")
                   
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
        self.writeLog(str(self.parent) + ',' + str(dna.ttl) + ',' + self.baseFile + ',' + str(dna.sleepTime) + ',' + str(self.dnaFile) + ',' +
                 str(self.loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) + ',' + str(round(foodObj.runningP, 2)) + '\n')

        time.sleep(dna.sleepTime) # Small delay to reduce excessive CPU usage
        self.loopCnt += 1
        self.checkOverpopulation(dna.MAXPOP)
        return

    def prosperityCheck(self, dna, foodObj):
        self.fatAndHappy = True
        self.windowList = self.foodList[-5:]
        
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
                self.writeLog("#" + c[0] + "," + c[1])
            sys.exit("Max Population Exceeded: " + str(self.population))
        return

    def setDNA(self):
        print("*** setDNA ***")

        whoami = __file__
        
        if "cell1Body.py" in whoami: # First cell -- rewrite list file
            self.baseFile = "cell1Body.py"
            self.parent = "cell1Body.py"
            self.dnaFile = "cell1DNA.py"
            self.dnaModule = "cell1DNA"

            fileEntry = "1" + ",cell1Body.py" + ",cell1Body.py," + self.dnaFile + "\n"

            filer = open(fList, "w")
            filer.writelines(str(fileEntry))
            filer.close()
        else:
            self.BaseFile = self.setBaseFile(__file__)
            fileNum = self.getFileNumber(self.baseFile)
            print("*** setDNA; fileNum: ", fileNum)
            
            self.dnaFile = "cell" + str(fileNum) + "DNA.py"
            self.dnaModule = "cell" + str(fileNum) + "DNA"
            print("*** setDNA; self.dnaFile: ", self.dnaFile)
        return

    def setParent(self):
        print("setParent: start")
        fLst = []
        
        with open(fList, "r") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            fileContent = file.read()
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        file.close()

        fileLines = fileContent.split("\n")

        for line in fileLines:
            lineLst = line.split(',')
            if len(lineLst) == 4:
                fLst.append(lineLst)

        for line in fLst:
            if line[2] == self.baseFile:
                print("setParent: line: ", line)
                self.parent = line[1]
        print("self.parent: ", self.parent)
        self.printAll()
        print("setParent: end")
        return

    def setNextFileEntry(self, baseFile):
        print("*** getLastFile; baseFile: ", baseFile)

        fLst = []

        while self.isFileLocked(fList):
            time.sleep(1)        
            if not self.isFileLocked(fList):
                break

        with open(fList, "r") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            fileContent = file.read()
            #fcntl.flock(file.fileno(), fcntl.LOCK_UN) # Keep lock
        #file.close()

        fileLines = fileContent.split("\n")

        for line in fileLines:
            lineLst = line.split(',')
            if len(lineLst) == 4:
                fLst.append(lineLst)
        print("*** getLastFile; last entry: ", fLst[-1])
    
        lastFile = fLst[-1][2]
        print("*** getLastFile; lastFile: ", lastFile)
    
        lastFileNum = self.getFileNumber(lastFile)
        print("*** getLastFile; lastFileNum: ", lastFileNum)

        nextFileNum = int(lastFileNum) + 1

        childParent = self.baseFile

        childCell = "cell" + str(nextFileNum) + "Body.py"
        childDNA = "cell" + str(nextFileNum) + "DNA.py"
    
        nextFileEntry = str(nextFileNum) + "," + childParent + "," + childCell + "," + childDNA + "\n"
        print("*** getLastFile; nextFileEntry: ", nextFileEntry)
    
        with open(fList, "a") as file:
            #fcntl.flock(file.fileno(), fcntl.LOCK_EX) ## Should still be locked!?
            file.write(nextFileEntry)
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        file.close()
    
        return childParent, childCell, childDNA


##########################
if __name__ == "__main__":

    print("--- START __main__ CELL INSTANCE ---")
    start_time = time.time()
    thisCell = Cell()
    thisCell.setDNA()
    thisCell.setBasePath(__file__)

    dna = importlib.import_module(thisCell.dnaModule)

    if (thisCell.parent == '') or (thisCell.parent == None):
        thisCell.setParent()

    # Capture cellnDNA.py modified time
    thisCell.mTimeStart = os.path.getmtime(thisCell.dnaFile)
    
    foodObj = dna.Food()
    end_time = start_time + dna.ttl

    print("B4 Loop:")
    thisCell.printAll()

    while time.time() < end_time:
        print("----------TopOfLoop")
        thisCell.loopBody(dna, foodObj)
 
    # Write children to log file
    print("Time to die...")
    for c in thisCell.myChildren:
        print(c)
        thisCell.writeLog("#" + c[0] + "," + c[1])
