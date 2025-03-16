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
    return a, p


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
            if file[i].strip() == "#/INIT1":
                newFile.pop()
                newFile.append(file[i - 1] + ",")
                newFile.append(file[i])
                newFile.append("        _x = ''")
                newFile.append("        ):\n")
                found = True
            elif file[i].strip() == "#/INIT2":
                newFile.append(file[i])
                newFile.append("        self._x = _x\n")
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
    

def modifyClass():
    # Creat new property within Arithmetic class
    newProperties = []
    newDef      = "    def x(self):"
    newDefBody  = "        return self._x"
    newProperties.append(newDef)
    newProperties.append(newDefBody)
    
    addProperty2Class(newProperties, "ARITHMETIC")
    return
    

if __name__ == "__main__":

    print("Start: basicMathMain __main__")

    a = None
    p = None

    mathMod = importlib.import_module('basicMath')
    a, p = setup(mathMod)
    
    if debug:
        print('--- Setup Complete ---')
        p.printAll()
        print('---')
        a.printAll()
        
    print('--- Do Stuff ---')
    # Add new property to Class and reload Class
    print('a.getAll():')
    aAll = a.getAll()

    print('aAll:')
    print(aAll)

    """
    Seems to be two ways to modify code:
    1) Just modify/add functions (def) within the file
    2) Modify a class:
        a) load all class vars to locals
        b) modify the class
        c) Instantiate a new object from the modified class
           using the original class vars
    """
    modifyClass() # Modify Arithmetic class file

    importlib.reload(mathMod) # Reload (import) file

    # Create new (modified) instance of modofied class
    a2 = mathMod.Arithmetic(aAll['N'], aAll['N0'], aAll['Z'], aAll['additionSymbol'],
                            aAll['subtractionSymbol'], aAll['multiplicationSymbol'],
                            aAll['divisionSymbol'], 'NEWXVALUE')

    

    print("End: basicMathMain __main__")
