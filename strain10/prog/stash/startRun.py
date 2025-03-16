# startRun.py
#

import os
import sys
import shutil
from utils import analyzeRun, cleanPetriDish, processRun


def evolveAndRun(cells100):
    print("...Start evolveAndRun...")
    print(len(cells100))

    if len(cells100) > 0:
        lastCell100 = cells100[-1]
        print("lastCell100: ", lastCell100)

        gen2CellBody = lastCell100[2][3]
        gen2CellDNA = lastCell100[2][5]
        print('gen2CellBody: ', gen2CellBody)
        print('gen2CellDNA: ', gen2CellDNA)

        cleanPetriDish(petriDishPath, gen2CellBody, gen2CellDNA)
    else:
        print('No 100% found, no evolution to run...')

    return


def prepare1stRun():

    whoami = __file__
    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    petriDishPath = whoami[:res[-2]]
    print("whoami: ", whoami)
    print("petriDishPath: ", petriDishPath)
    os.chdir(petriDishPath)
    print("chdir to: ", os.getcwd())
    
    for entry in os.listdir(petriDishPath):
        if os.path.isfile(os.path.join(petriDishPath, entry)):
            # File found, exit or clean?
            ans = input("Petri dish not empty, clean or exit <C/E>? ")
            if ans in ['c', 'C']:
                cleanPetriDish(petriDishPath, None, None)
                break
            else:
                sys.exit("Petri dish not empty, please clean Petri dish before use...")

    dataPath = petriDishPath + "/data"
    dataFound = False
    print("dataPath: ", dataPath)

    for entry in os.listdir(dataPath):
        if os.path.isfile(os.path.join(dataPath, entry)):
            dataFound = True

    if dataFound:
        print("Proceeding with existsing data...")
    else:
        print("Need to create data!")
        sys.exit("No data found, exiting.")

    # Copy cell1Body.py into the Petri dish 
    shutil.copyfile("prog/cell1Body.py", "cell1Body.py")

    # Copy cell1DNA.py into the Petri dish
    shutil.copyfile("prog/cell1DNA.py", "cell1DNA.py")

    print("Cell files placed in Petri dish...")

    return petriDishPath




if __name__ == "__main__":

    print('START startRun __main__')
    processFound = False
    cells100 = []
    petriDishPath = prepare1stRun()

    # Make sure
    os.chdir(petriDishPath)

    processRun("cell1Body.py")

    ans = input("Analyze Run <Y/n>? ")
    if ans in ['Y', 'y']:
        cells100 = analyzeRun()

    ans = input("Evolve and run <Y/n>? ")
    if ans in ['Y', 'y']:
        print("...Calling Evolve...")
        evolveAndRun(cells100)

    print("END startRun __main__.")
