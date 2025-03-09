# basicMathMain.py
# Can we learn math?
#
from basicMath import pickleMemory ###, Arithmetic
import importlib

debug = True


def setup(mathMod):
    global debug
    p = mathMod.pickleMemory()
    p.setupPickle()
    if debug:
        p.printAll()
    ans = input("Use existing data <Y/n>? ")
    if ans in ['Y', 'y']:
        a = None
        a = p.loadPickle(a)
    else:
        a = mathMod.Arithmetic()
    return p, a


def readClassFile():
    fileLines = []

    with open('basicMath.py', 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


def addProperty2Class(newProperties, whichClassSection):
    file = readClassFile()
    found = False
    newFile = []

    if whichClassSection == "ARITHMETIC":
        for i in range(len(file)):
            if file[i].strip() == "#/END_OF_ARITHMETIC_CLASS_INIT":
                newFile.append(file[i])
                newFile.append("        self._x = None")
                found = True
            elif file[i].strip() == "#/END_OF_ARITHMETIC_CLASS":
                newFile.append(file[i])
                for p in newProperties:
                    newFile.append(p)
                found = True
            else:
                if found:
                    found = False
                    continue
                newFile.append(file[i])
    else:
        print("Invalid addition: {}; Not added to class.".format(whichClassSection))
        return

    with open('basicMath.py', "w") as outFile:
        for l in newFile:
            outFile.write(l + "\n")
    outFile.close()
        
    print("New class added: {}, {}".format(newProperties, whichClassSection))
    return
    

def createProperty(a):
    # Creat new property within Arithmetic class
    newProperties = []
    newProperty = "    @property"
    newDef      = "    def x(self):"
    newDefBody  = "        return self._x"
    newProperties.append(newProperty)
    newProperties.append(newDef)
    newProperties.append(newDefBody)
    
    addProperty2Class(newProperties, "ARITHMETIC")
    return
    

if __name__ == "__main__":

    print("Start: basicMathMain __main__")

    mathMod = importlib.import_module('basicMath')
    p, a = setup(mathMod)
    if debug:
        print('--- Setup Complete ---')
        p.printAll()
        print('---')
        a.printAll()
        
    print('--- Do Stuff ---')
    # Add new property to Class and reload Class
    createProperty(a)
    importlib.reload(mathMod)

    

    print("End: basicMathMain __main__")
