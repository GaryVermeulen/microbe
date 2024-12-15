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
from subprocess import call


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


def getLastFile():

    # Read file
    fLst = []
    with open("txt/fileList.txt", "r") as f:
        for line in f:
            line = line.replace("\n", "")
            lineLst = line.split(',')
            fLst.append(lineLst)
    f.close()

    # Get last entry
    parent = fLst[-1][0]
    lastFile = fLst[-1][1]
    lastDNA = fLst[-1][2]

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
    fileEntry = baseFile + "," + newFile + "," + newDNA + "\n"

    filer = open("txt/fileList.txt", "a")
    filer.writelines(fileEntry)
    filer.close()
    
    return newFile, newDNA


def mutateWhichFile(newDNA, newFileNum):

    file = readDNAFile(newDNA)
    found = False
    newFile = []
    
    for i in range(len(file)):
        if file[i].strip() == "#/WHICHFILE":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            newFile.append("        whichFile = " + str(newFileNum) + ",")
            found = True
        else:
            #print("NF: ", file[i])
            if found:
                found = False
                continue
            newFile.append(file[i])

    with open(newDNA, "w") as outFile:
        for l in newFile:
            outFile.write(l + "\n")
    outFile.close()

    return


def replicate(baseFile, dnaFile, foodObj):
    print("-----")
    print("replicate:")

    parent, lastFile, lastDNA = getLastFile()
    newFile, newDNA = setNextFile(baseFile, lastFile, lastDNA)
        
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
        newFileNum = int(foodObj.whichFile) + 1
        mutateWhichFile(newDNA, newFileNum)
    
    
    print("Starting replicated file: ", newFile)
    print("Replicated DNA file: ", newDNA)

    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newFile + "; bash"
    call(callStr)
    
    
    return


if __name__ == "__main__":

    whoami = __file__
    currentNum = 0
    loopCnt = 1
    
    #basePath = "/home/gary/src/petri_dish/strain3"
    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    basePath = whoami[:res[-1]]
    baseFile = whoami[res[-1]:]
    baseFile = baseFile[1:]
    
    start_time = time.time()

    print("--- START CELL INSTANCE ---")
    print("whoami: ", whoami)
    print("basePath: ", basePath)
    print("baseFile: ", baseFile)

    #sys.exit("TEMP")

    # Determine and import appropriate DNA module
    #
    if "cell1Body.py" in whoami: # First cell -- rewrite list file
        parent = "cell1Body.py"
        dnaFile = "cell1DNA.py"
        dnaModule = "cell1DNA"

        fileEntry = "cell1Body.py" + ",cell1Body.py," + dnaFile + "\n"

        filer = open("txt/fileList.txt", "w")
        filer.writelines(str(fileEntry))
        filer.close()
    else:
        parent, lastFile, dnaFile = getLastFile()
        dnaModule = dnaFile[:-3]
        
    print("dnaFile: ", dnaFile)
    print("dnaModule: ", dnaModule)
    print("parent: ", parent)

    dna = importlib.import_module(dnaModule)
    
    # cellnDNA.py modified time
    mTimeStart = os.path.getmtime(dnaFile)
    print("{} modified time: {}".format(dnaFile, mTimeStart))
    print("----------")
    
    # Starting point
    foodObj         = dna.Food()
    ttl             = dna.ttl
    MAXPOP          = dna.MAXPOP
    stopReplication = dna.stopReplication
    sleepTime       = dna.sleepTime
    isPrimeTotal    = foodObj.isPrimeTotal
    
    end_time = start_time + ttl
          
    while time.time() < end_time:
        print("----------")

        # Replicate (or attempt to) as per stopReplication and if within file number limit
        #
        if stopReplication == 0:
            population = 0
        else:
            population = len([f for f in os.listdir(basePath) if os.path.isfile(os.path.join(basePath, f))])
            
        if population < (MAXPOP - 5):        
            # Trying self-replication (typical max loop count is 120)
            random_int = random.randint(1, 120)
            # With sleepTime = 0 many more loops
            if (random_int == loopCnt) or (loopCnt % 25 == 0): #(loopCnt == 100): # One free pass at 100
                if (loopCnt % 25 == 0): #(loopCnt == 100): # Reduce odds with "coin flip"
                    random_coin = random.randint(0, 1)
                    if random_coin == 1:
                        print("Won multiple of 100 - 50/50 coin toss, Replicate. ", random_coin)
                        replicate(baseFile, dnaFile, foodObj)
                    else:
                        print("Lost multiple of 100 - 50/50 coin toss, no replication. ", random_coin)
                else:
                    print("Replicating randomly at: ", random_int)
                    replicate(baseFile, dnaFile, foodObj)
        else:
            print("Max Population (-5) Exceeded, no further replications: " + str(population))
            
        # Mutated? Has the DNA file timestamp changed?
        # In other words: Was the DNA file mutated while running?
        # This kind-of works, but is unreliable and there are possible
        # side-effects and is not always guaranteed.
        #
        mTimeNow = os.path.getmtime(dnaFile)

        if mTimeStart < mTimeNow:
            print("!!! *** Mutation Detected: Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason was throwing an error
            #print("*** dna: ", dna)
            #print(sys.modules)
            importlib.reload(dna)

            # Hack
            #del sys.modules[dna] # This used to work when reload did not???
            ##dna = importlib.import_module(dnaModule)

            # Reset possibily mutated var's
            sleepTime = dna.sleepTime
            ttl       = dna.ttl
            
            print("!!! *** Re-imported cellFunction")
            mTimeStart = mTimeNow
         
        # Principal cell functions
        #
        # Currently: metabolize via Food class
        #
        foodObj.printAll()
        print('---')
        foodObj.metabolize(loopCnt)
        print('---')
        foodObj.printAll()

        print('Running: parent: {}, ttl: {}, baseFile: {}, sleepTime: {}, DNA: {}, loopCnt: {}, thisFood: {}, isPrime: {}, runningP: {}'.format(
            parent, ttl, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime, foodObj.runningP))

        # Write to log file
        #  parent, TTL, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime
        writeLog(parent + ',' + str(ttl) + ',' + baseFile + ',' + str(sleepTime) + ',' + str(dnaFile) + ',' +
                 str(loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) + ',' + str(foodObj.runningP) + '\n')

        time.sleep(sleepTime) # Small delay to reduce excessive CPU usage

        loopCnt += 1

        # Over population?
        #
        population = len([f for f in os.listdir(basePath) if os.path.isfile(os.path.join(basePath, f))])
        if population > MAXPOP:
            sys.exit("Max Population Exceeded: " + str(population))
