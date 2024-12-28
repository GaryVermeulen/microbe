# startRun.py
#

import os
import sys
import shutil
from subprocess import call




if __name__ == "__main__":

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

    print("Files placed in Petri dish...")

    os.chdir(petriDishPath)
    print("chdir to: ", petriDishPath)

    # Start the run...
    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + "cell1Body.py" + "; bash"
    call(callStr)

    print("Run started...")
