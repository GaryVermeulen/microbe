# genAnalyzer.py
#
# Analyze results from generation runs.
#

import os
import pickle
import shutil

#from genMutator import mutate

def getFile(f):
    fileLines = []

    with open(f, 'r') as inFile:
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
    basePath = whoami[:res[-1]]

    #path = '/path/to/directory'  # Replace with the actual path to your directory
    fileList = os.listdir(basePath)

    for f in fileList:
        if f[-3:] == "log":
            print('-----')
            print(f)

            contents = getFile(f)

            isTrue = 0
            isFalse = 0
            cnt = 1
            listOfLines = []
            reducedLines = []
            for l in contents:
                #print(l)

                lineList = l.split(',')
                #print(lineList)
                # Log file:
                # pid, ppid, DNA, loopCnt, startNum, currentNum, isPrime

                pid = lineList[0]

                ppid = lineList[1]

                #print(pid, ppid)
                sleepTime = lineList[2]
                dnaFile = lineList[3]
                
                #print(pid, ppid, dnaFile)
                
                
                if lineList[-1] == "True":
                    #print("TRUE")
                    isTrue += 1
                else:
                    #print("FALSE")
                    isFalse += 1
                cnt += 1

                listOfLines.append(lineList)



            totalCnt = cnt - 1
            
            print("cnt: {}; True: {}; False: {}".format(totalCnt, isTrue, isFalse))
            X = cnt - 1
            Y = isTrue
            P = Y / X
            print("What % of {} is {}? {} or {}".format(X, Y, round(P, 2), round(P*100)))
                

            files.append((f, listOfLines))
            filesBrief.append((f, [pid, ppid, sleepTime, dnaFile, totalCnt, isTrue, isFalse, round(P*100)]))


    print('---------')
    print(len(files))

    #print(files[0])
    #print(files[5])

    # Save this gen's log files
    print('Saving this generation\'s logs to pickle...')
    with open("logs.p", "wb") as f:
        pickle.dump(files, f)
    f.close()
        
    print('Pickle saved.')

    print('---------')
    print(len(filesBrief))

    #print(filesBrief[0])
    highestP = 0
    for f in filesBrief:
        print('---')
        print(f)
        print(f[0])
        print(f[1])
        print('---')

        # Keep if over 40%
        #if f[1][-1] > 40:
        #    print("KEEP: ", f[1][2], f[1][-1])
        #    keepers.append((f[1][2], f[1][-1]))
        #    print(keepers)
        #else:
        #    print("DROP")

        # Keep the highest %
        if f[1][-1] > highestP:
            highestP = f[1][-1]
            keeper = [(f[1][3], f[1][-1])]

    print("Keeper: ", keeper)
    print(keeper[0][0])

    #ans = input("Mutate & set DNA1 to keeper <Y/n>? ")
    #if ans in ['Y', 'y']:
        # Set keeper to cell1DNA.py
        #shutil.copyfile(keeper[0][0], 'cell1DNA.py')
        #print("file copied...")

        # Mutate newCodeFile.txt 
        #mutate(keeper[0][0]) # Send the highestP for enhancement
    
    #print("last keeper: ", keepers[-1])
    #        
    #mutate(keepers[-1][0])

    #for k in keepers:
    #    tmp = k
    
