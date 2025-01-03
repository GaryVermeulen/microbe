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


def getNewCode():
    
    codeLines = []

    with open('txt/newCodeFile.txt', 'r') as inFile:
        for line in inFile:
            codeLines.append(line.strip())
    inFile.close()
    return codeLines


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


def mutateDNAFileCode(newDNA):

    file = readDNAFile(newDNA)

    newCode = getNewCode()

    found = False
    newFile = []
    for i in range(len(file)):
        if file[i].strip() == "#/START":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append("    " + j)
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


def mutateDNAFileSleepTime(newDNA):

    sleepTime = 1 # Need atleast 1 second due to file operations

    file = readDNAFile(newDNA)

    sleepTime = random.randint(1, 3)
    
    newCode = ['sleepTime = ' + str(sleepTime)]

    found = False
    newFile = []
    for i in range(len(file)):
        if file[i].strip() == "#/SLEEPTIME":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append(j)
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


def mutateDNAFileStartNum(newDNA):

    file = readDNAFile(newDNA)

    random_int = random.randint(1, 120)
    
    newCode = ['startNum = ' + str(random_int)]

    found = False
    newFile = []
    for i in range(len(file)):
        if file[i].strip() == "#/STARTNUM":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append(j)
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


def mutateDNAFileTTL(newDNA):

    file = readDNAFile(newDNA)

    random_int = random.randint(120, 180)
    
    newCode = ['ttl = ' + str(random_int)]

    found = False
    newFile = []
    for i in range(len(file)):
        if file[i].strip() == "#/TTL":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append(j)
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


def replicate(baseFile, dnaFile):
    print("-----")
    print("replicate:")

    parent, lastFile, lastDNA = getLastFile()
    newFile, newDNA = setNextFile(baseFile, lastFile, lastDNA)
        
    # Create file (replicant)
    shutil.copyfile(lastFile, newFile)

    # Create matching DNA file
    shutil.copyfile(lastDNA, newDNA)

    
    # Mutate DNA?
    # Mutate which part?
    # Not usewd at this time - 3 - mutate cell function (code)
    # 2 - mutate sleepTime
    # 1 - mutate ttl
    #
    random_int = random.randint(0, 2)
    
    if random_int == 2:
        # Mutate sleepTime
        print("*** Mutating sleepTime: ", newDNA)
        mutateDNAFileSleepTime(newDNA)
    elif random_int == 1:
        # Mutate ttl
        print("*** Mutating ttl: ", newDNA)
        mutateDNAFileTTL(newDNA)
    else:
        print("*** No mutation.")
    
    print("Starting replicated file: ", newFile)
    print("Replicated DNA file: ", newDNA)

    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newFile + "; bash"
    call(callStr)
    
    return


if __name__ == "__main__":

    #MAXPOP = 50
    whoami = __file__

    currentNum = 0
    loopCnt = 1
    P = 0
    
    #basePath = "/home/gary/src/petri_dish/strain3"
    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    basePath = whoami[:res[-1]]
    baseFile = whoami[res[-1]:]
    baseFile = baseFile[1:]
    
    start_time = time.time()
    #end_time = start_time + 120  # 2 minutes

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
    #startNum        = dna.startNum
    sleepTime       = dna.sleepTime
    isPrimeTotal    = foodObj.isPrimeTotal #dna.isPrimeTotal
    #currentNum = startNum
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
            if (random_int == loopCnt) or (loopCnt % 100 == 0): #(loopCnt == 100): # One free pass at 100
                if (loopCnt % 100 == 0): #(loopCnt == 100): # Reduce odds with "coin flip"
                    random_coin = random.randint(0, 1)
                    if random_coin == 1:
                        print("Won multiple of 100 - 50/50 coin toss, Replicate. ", random_coin)
                        replicate(baseFile, dnaFile)
                    else:
                        print("Lost multiple of 100 - 50/50 coin toss, no replication. ", random_coin)
                else:
                    print("Replicating randomly at: ", random_int)
                    replicate(baseFile, dnaFile)
        else:
            print("Max Population (-5) Exceeded, no further replications: " + str(population))
            
        # Mutated? Has the timestamp changed?
        mTimeNow = os.path.getmtime(dnaFile)

        if mTimeStart < mTimeNow:
            print("*** Mutation Detected: Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason throws an error
            # Hack
            del sys.modules[dna]
            dna = importlib.import_module(dnaModule)
            #from cellFunction import cellFunction
            print("!!! Re-imported cellFunction")
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
        

        print('Running: parent: {}, ttl: {}, baseFile: {}, sleepTime: {}, DNA: {}, loopCnt: {}, thisFood: {}, isPrime: {}'.format(
            parent, ttl, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime))

        # Write to log file
        #  parent, TTL, baseFile, sleepTime, dnaFile, loopCnt, foodObj.thisFood, foodObj.isPrime
        writeLog(parent + ',' + str(ttl) + ',' + baseFile + ',' + str(sleepTime) + ',' + str(dnaFile) + ',' +
                 str(loopCnt) + ',' + str(foodObj.thisFood) + ',' + str(foodObj.isPrime) + '\n')

        time.sleep(sleepTime) # Small delay to reduce excessive CPU usage

        loopCnt += 1

        # Over population?
        #
        population = len([f for f in os.listdir(basePath) if os.path.isfile(os.path.join(basePath, f))])
        if population > MAXPOP:
            sys.exit("Max Population Exceeded: " + str(population))
