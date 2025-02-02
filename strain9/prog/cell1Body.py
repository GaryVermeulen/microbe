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


#fList = "/home/gary/src/strain9/txt/fileList.txt"


class Cell:

    def __init__(
        self,
        population = 0,
        basePath = '',
        baseFile = '',
        fileList = '',
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
        self.fileList = fileList
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

    def setFileList(self):
        self.fileList = self.basePath + "/txt/fileList.txt"
        return

    def __reduce__(self):
        return (self.__class__, (self.population, self.basePath, self.baseFile,
                                 self.parent, self.dnaFile, self.dnaModule, self.mTimeStart,
                                 self.loopCnt, self.myChildren, self.foodList,
                                 self.windowSize, self.windowList, self.fatAndHappy))

    def printAll(self):
        print("Cell: population: ", self.population)
        print("Cell: basePath: ", self.basePath)
        print("Cell: baseFile: ", self.baseFile)
        print("Cell: parent: ", self.parent)
        print("Cell: dnaFile: ", self.dnaFile)
        print("Cell: dnaModule: ", self.dnaModule)
        print("Cell: mTimeStart: ", self.mTimeStart)
        print("Cell: loopCnt: ", self.loopCnt)
        if len(self.myChildren) > 0:
            print("Cell: myChildren:")
            for c in self.myChildren:
                print("Cell: child: ", c)
        else:
            print("Cell: No Children.")
        print("Cell: foodList len: ", len(self.foodList))
        print("Cell: windowSize: ", self.windowSize)
        print("Cell: windowList: ", self.windowList)
        print("Cell: fatAndHappy: ", self.fatAndHappy)
        return

    def readDNAFile(self):
        fileLines = []

        with open(self.dnaFile, 'r') as inFile:
            for line in inFile:
                fileLines.append(line.strip("\n"))
        inFile.close()
        return fileLines

    def writeLog(self, fInput):
        baseStr = __file__[:-7] # remove the Base.py
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
                    print("Replicating semi-randomly at: ", random_int)
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
        # global dna #?
        self.setPopulation(dna.stopReplication)
        self.toReplicate(dna.MAXPOP, foodObj)
        self.prosperityCheck(dna, foodObj)
        self.setAvalon(dna, foodObj) # Have we found Avalon?

        # Has another cell found Avalon?
        # Overrides prosperity/fatAndHappy
        if dna.Pheromone:
            
            if dna.hasAvalonBeenFound():
                print("AVALON {} was found: dna.AVALON:". format(dna.AVALON))
                print("foodObj.foodFile: ", foodObj.foodFile)
                foodObj.foodFile = dna.AVALON
                print("Reset foodObj.foodFile: ",foodObj.foodFile)
            else:
                print("AVALON {} was NOT found: dna.AVALON:". format(dna.AVALON))
                
        else:
            # What to do if fat-and-happy...?
            # Extend ttl, sleep more, starvingCheck less?
            ##self.prosperityCheck(dna, foodObj)

            if not self.fatAndHappy:
                print("NOT self.fatAndHappy: ", self.fatAndHappy)
                if (self.loopCnt % foodObj.starvingCheck == 0) and (foodObj.runningP < 100.0):
                    print("YES: Change food source.")
                    foodObj.changeFoodSource(thisCell.loopCnt)
                else:
                    print("NO: Change food source.")

            ##self.setAvalon(dna, foodObj) # Have we found Avalon?

            # Was DNA file mutated?
            mTimeNow = os.path.getmtime(self.dnaFile)
        
            if self.mTimeStart < mTimeNow:
                print("!!! *** Mutation Detected: Start time < time now")
                print("!!! self.dnaModule: ", self.dnaModule)
                print("!!! type(dna): ", type(dna))
            
                #importlib.reload(cellFunction) # For some unkonwn reason was throwing an error
                #print("*** dna: ", dna)
                #print(sys.modules)
                importlib.reload(dna) # Does dna need to be Global?

                # Hack
                #del sys.modules[dna] # This used to work when reload did not???
                ##dna = importlib.import_module(dnaModule)

                # Reset possibily mutated var's
                #sleepTime = dna.sleepTime
                #ttl       = dna.ttl
            
                print("!!! *** Re-imported dnaModule")
                self.mTimeStart = mTimeNow
            
        foodObj.metabolize(thisCell.loopCnt)
        self.foodList.append(foodObj.thisFood)

        #self.setAvalon(dna, foodObj) # Have we found Avalon?
       
        print('--- foodObj.printAll():')
        foodObj.printAll()
        print('--- thisCell.printAll():')
        self.printAll()
        print('Running: Avalon: {}, parent: {}, ttl: {}, baseFile: {}, sleepTime: {}, DNA: {}, loopCnt: {}, thisFood: {}, isPrime: {}, runningP: {}'.format(
            dna.AVALON, self.parent, dna.ttl, self.baseFile, dna.sleepTime, self.dnaFile, self.loopCnt, foodObj.thisFood, foodObj.isPrime, round(foodObj.runningP, 2)))

        # Write to log file
        #  parent, TTL, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime
        self.writeLog(dna.AVALON + ',' + str(self.parent) + ',' + str(dna.ttl) + ',' + self.baseFile + ',' + str(dna.sleepTime) +
                      ',' + str(self.dnaFile) + ',' + str(self.loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) +
                      ',' + str(round(foodObj.runningP, 2)) + '\n')
        
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
        
        if "cell1Body.py" in __file__: # First cell -- rewrite list file
            self.baseFile = "cell1Body.py"
            self.parent = "cell1Body.py"
            self.dnaFile = "cell1DNA.py"
            self.dnaModule = "cell1DNA"
            fileEntry = "1" + ",cell1Body.py" + ",cell1Body.py," + self.dnaFile + "\n"

            filer = open(self.fileList, "w")
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
        
        with open(self.fileList, "r") as file:
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

        while self.isFileLocked(self.fileList):
            time.sleep(1)        
            if not self.isFileLocked(self.fileList):
                break

        with open(self.fileList, "r") as file:
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
    
        with open(self.fileList, "a") as file:
            #fcntl.flock(file.fileno(), fcntl.LOCK_EX) ## Should still be locked!?
            file.write(nextFileEntry)
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        file.close()
    
        return childParent, childCell, childDNA

    def setAvalon(self, dna, foodObj):
        if self.loopCnt > foodObj.starvingCheck: # Must be old enough, but is this checking too often?
        #? if (self.loopCnt % foodObj.starvingCheck == 0) and (foodObj.runningP < 100.0):
            print("AVALON check...")
            if self.fatAndHappy and (foodObj.runningP == 100):
                print("$$$ Re-write DNA file to retain AVALON")
                print("$$$ dna.AVALON: ", dna.AVALON)
                print("$$$ foodObj.foodFile: ", foodObj.foodFile)
                if not foodObj.avalonFound:
                    print("$$$ setting Avalon in DNA file.")
                    self.mutateDNAFile(foodObj.foodFile, "AVALON")
                    foodObj.avalonFound = True
                    if dna.Pheromone:
                        dna.setAvalonFile(foodObj.foodFile)
                else:
                    print("$$$ Avalon already located.")
        return

    def mutateDNAFile(self, newValue, dnaPart):
        file = self.readDNAFile()
        found = False
        newFile = []

        if dnaPart == "AVALON":
            for i in range(len(file)):
                if file[i].strip() == "#/AVALON":
                    #print("FOUND: ", file[i])
                    newFile.append(file[i])
                    newFile.append("AVALON = '" + str(newValue) + "'")
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

        with open(self.dnaFile, "w") as outFile:
            for l in newFile:
                outFile.write(l + "\n")
        outFile.close()
        
        print("DNA Mutated: {}, {}".format(newValue, self.dnaFile))
        return



##########################
if __name__ == "__main__":

    print("--- START __main__ CELL INSTANCE ---")
    start_time = time.time()
    thisCell = Cell()
    
    thisCell.setBasePath(__file__)
    thisCell.setFileList()

    thisCell.setDNA()
    
    dna = importlib.import_module(thisCell.dnaModule)

    thisCell.mTimeStart = os.path.getmtime(thisCell.dnaFile)
    
    if (thisCell.parent == '') or (thisCell.parent == None):
        thisCell.setParent()

    foodObj = dna.Food()

    print("B4 Loop: dna.AVALON: ", dna.AVALON)
    if not dna.AVALON == '?':
        foodObj.avalonFound = True
        foodObj.foodFile = dna.AVALON
        
    end_time = start_time + dna.ttl

    print("B4 Loop: foodObj:")
    foodObj.printAll()

    while time.time() < end_time:
        print("----------TopOfLoop")
        thisCell.loopBody(dna, foodObj)
 
    # Write children to log file
    print("Time to die...")
    for c in thisCell.myChildren:
        print(c)
        thisCell.writeLog("#" + c[0] + "," + c[1])
