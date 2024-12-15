# genAnalyzer.py
#
# Analyze results from generation runs.
#

import os
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

                lineList = l.split(',')
                """
                if lineList[-1] == "True":

                    isTrue += 1
                else:

                    isFalse += 1

                # Running % of True
                X = lineList[5]
                Y = isTrue
                P = (int(Y) / int(X)) * 100

                lineList.append(round(P))
                """
                listOfLines.append(lineList)

            files.append((f, listOfLines))

    print('---------')
    print(len(files))

    # Save this gen's log files
    print('Saving this generation\'s logs to pickle...')
    with open("../pickles/logs.p", "wb") as f:
        pickle.dump(files, f)
    f.close()
        
    print('Pickle saved.')
    print('---------')

    for f in files:
        filesBrief.append((f[0], f[1][-1]))

    print('---------')
    print(len(filesBrief))

    #for f in filesBrief:
    #    print(f)

    print('---------')
    #filesBrief.sort()

    filesBrief.sort(key = lambda x: x[-1][-1])
    
    for f in filesBrief:
        if f[1][-1] == '100.0':
            print("Keeper: ", f)
        else:
            print(f)
    
