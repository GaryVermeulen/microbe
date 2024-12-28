# genAnalyzer.py
#
# Analyze results from generation runs.
#

import os
import sys
import pickle
import shutil

def getFile(f):
    fileLines = []

    with open('../' + f, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


if __name__ == "__main__":

    whoami = __file__

    files = []
    filesBrief = []
    keeper = []

    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    #basePath = whoami[:res[-1]]
    basePath = whoami[:res[-2]]

    print("basePath: ", basePath)

    #path = '/path/to/directory'  # Replace with the actual path to your directory
    fileList = os.listdir(basePath)

    for f in fileList:
        if f[-7:] == "Log.txt":

            contents = getFile(f)

            isTrue = 0
            isFalse = 0
            
            listOfLines = []
            reducedLines = []
            for l in contents:
                if l[0] != "#":
                    lineList = l.split(',')
                    listOfLines.append(lineList)
                else:
                    listOfLines.append(l)
                    #print(l)

            files.append((f, listOfLines))

    print('---------')
    print(len(files))
    
    if len(files) == 0:
        #
        print("No log files found, reading pickle from last run...")
        with open("../pickles/logs.p", "rb") as f:
            files = pickle.load(f)
        f.close()
        if len(files) == 0:
            sys.exit("No log files found, exiting...")
    else:
        # Save this gen's log files
        print('Saving this generation\'s logs to pickle...')
        with open("../pickles/logs.p", "wb") as f:
            pickle.dump(files, f)
        f.close()

    print("Processing:")
    print('---------')
    for f in files:
        #print(f[0])
        logName = f[0]
        idx = 0
        
        if f[1][-1][0] == "#":
            lastLineP = f[1][-2]
            filesBrief.append((logName, f[1][-1], lastLineP))
        else:
            lastLineP = f[1][-1]
            filesBrief.append((logName, "NC", lastLineP))
            
    print('---------')
    
    #for f in files:
    #    filesBrief.append((f[0], f[1][-1]))

    print('---------')
    print(len(filesBrief))

    #for f in filesBrief:
    #    print(f)

    print('---------')
    #filesBrief.sort()

    # Sort by %
    filesBrief.sort(key = lambda x: x[-1][-1])
    #
    cnt100 = 0
    for f in filesBrief:
        #print(f)
        if f[2][-1] == '100.0':
            cnt100 += 1
            print(f)
    #    else:
    #        print(f)
    print("cnt100: ", cnt100)
    P = (cnt100 / len(filesBrief)) * 100
    print("P: ", P)
    print('---------')

    cnt90 = 0
    for f in filesBrief:
        #print(f)
        if (f[2][-1] >= '90.0') and (f[2][-1] <= '99.0'):
            cnt90 += 1
            print(f)
            
    print("cnt90: ", cnt90)
    P = (cnt90 / len(filesBrief)) * 100
    print("P: ", P)
    print('---------')

    # List Childern
    for f in filesBrief:
        if f[1] != "NC":
            print(f[0])
            tmpLst = f[1].split("#")
            for i in tmpLst:
                if len(i) > 0:
                    print("\t", i)
            print("---")
