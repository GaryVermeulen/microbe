# startRun.py
#

import os
import sys
import time
import shutil
import psutil
import datetime 
from subprocess import call



if __name__ == "__main__":

    processFound = False
    whoami = __file__
    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    #basePath = whoami[:res[-1]]
    petriDishPath = whoami[:res[-2]]

    print("whoami: ", whoami)
    print("petriDishPath: ", petriDishPath)
    
    for entry in os.listdir(petriDishPath):
        if os.path.isfile(os.path.join(petriDishPath, entry)):
            # File found, so exit...
            print(entry)
            sys.exit("Petri dish not empty, please clean Petri dish before use...")

    # Put a copy of cell1Body.py into the Petri dish 
    shutil.copyfile("cell1Body.py", "../cell1Body.py")

    # Put a copy of cell1DNA.py into the Petri dish
    shutil.copyfile("cell1DNA.py", "../cell1DNA.py")

    print("Cell files placed in Petri dish...")

    os.chdir(petriDishPath)
    print("chdir to: ", petriDishPath)

    # Start the run...
    start_time = time.time()
    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + "cell1Body.py" + "; bash"
    call(callStr)

    print("Run started...")
    print(datetime.datetime.now())
    print("----------")

    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == 'python3':
            if "cell" in process.info["cmdline"][1]:
                processFound = True
    
    while processFound:
        print("-----: ", datetime.datetime.now())
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            if process.info['name'] == 'python3':
                if "cell" in process.info["cmdline"][1]:
                    print("Running cell: ", process.info)
                    processFound = True
                else:
                    processFound = False
        if processFound:
            time.sleep(10)

    print("Run end at: ", datetime.datetime.now())
