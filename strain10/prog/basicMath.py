# basicMath.py
#
# 

import sys
import pickle


class Arithmetic:

    def __init__(
        self,
        N = {'Natural Numbers': {1,2,3,5,5,6,7,8,9}},
        N0 = {'Whole Numbers': {0,1,2,3,5,5,6,7,8,9}},
        Z = {'Integers': {-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9}},
        additionSymbol = '+',
        subtractionSymbol = '-',
        multiplicationSymbol = '*',
        divisionSymbol = '/',
#/INIT1        
        _x = ''
        ):


        self.N = N
        self.N0 = N0
        self.Z = Z
        self.additionSymbol = additionSymbol
        self.subtractionSymbol = subtractionSymbol
        self.multiplicationSymbol = multiplicationSymbol
        self.divisionSymbol = divisionSymbol
#/INIT2  
        self._x = _x

    def isNatural(self, x):
        if x in self.N['Natural Numbers']:
            return True
        elif isinstance(x, int) and x > 0:
            self.N['Natural Numbers'].add(x)
            return True
        return False

    def isWhole(self, x):
        if x in self.N['Whole Numbers']:
            return True
        elif isinstance(x, int) and x > -1:
            self.N['Whole Numbers'].add(x)
            return True
        return False

    def isInteger(self, x): # Just use int class?
        if x in self.N['Integers']:
            return True
        elif isinstance(x, int):
            self.N['Integers'].add(x)
            return True
        return False

    def printAll(self):
        print("N:  ", self.N)
        print("N0: ", self.N0)
        print("Z:  ", self.Z)
        print("Operation symbols:")
        print("   Addition:       ", self.additionSymbol)
        print("   Subtraction:    ", self.subtractionSymbol)
        print("   Multiplication: ", self.multiplicationSymbol)
        print("   Division:       ", self.divisionSymbol)

    def getAll(self):
        return {"N": self.N, "N0": self.N0, "Z": self.Z, "additionSymbol": self.additionSymbol,
                "subtractionSymbol": self.subtractionSymbol,
                "multiplicationSymbol": self.multiplicationSymbol,
                "divisionSymbol": self.divisionSymbol}

#/END_OF_ARITHMETIC_CLASS
    def x(self):
        return self._x

class pickleMemory:

    def __init__(
        self,
        basePath = '',
        picklePath = '',
        pickleFile = ''
        ):

        self.basePath = ''
        self.picklePath = ''
        self.pickleFile = ''

    def setBasePath(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        self.basePath = f[:res[-1]]
        return

    def setPicklePath(self):
        if self.basePath == None:
            print("Base Path Not Set.")
        else:
            testChar = "/"
            res = [i for i in range(len(self.basePath)) if self.basePath.startswith(testChar, i)]
            self.picklePath = self.basePath[:res[-1]] + "/p"
        return

    def setPickleFile(self):
        if self.picklePath == None:
            print("Pickle Path Not Set.")
        else:
            self.pickleFile = self.picklePath + "/pMem.p"
        return

    def writePickle(self, a):
        if self.pickleFile == None:
            print("Pickle File Not Set.")
        else:
            if a == None:
                print("No data to save to pickle: ", a)
            else:
                with open(self.pickleFile, 'wb') as pf:
                    pickle.dump(a, pf)
                pf.close()
        return

    def loadPickle(self, a):
        if self.pickleFile == None:
            print("Pickle File Not Set.")
        else:
            with open(self.pickleFile, 'rb') as pf:
                a = pickle.load(pf)
            pf.close()
        return a

    def setupPickle(self):
        self.setBasePath(__file__)
        self.setPicklePath()
        self.setPickleFile()
        return

    def printAll(self):
        print("basePath: ", self.basePath)
        print("picklePath: ", self.picklePath)
        print("pickleFile: ", self.pickleFile)
        return

    

def simpleAdd(x, y):
    return x + y

def simpleSubtract(x, y):
    return x - y

def myAdd(x, y):

    if isinstance(x, float):
        xFloat = x
        x = int(x)
        print("Converted x: {}  to int(x): {}.".format(xFloat, x))
    elif isinstance(y, float):
        yFloat = y
        y = int(y)
        print("Converted y: {}  to int(y): {}.".format(yFloat, y))

    xArr = []
    yArr = []

    if x < 0:
        xP = x * -1
    else:
        xP = x
        
    if y < 0:
        yP = y * -1
    else:
        yP= y

    #print("x & xP: ", x, xP)
    #print("y & yP: ", y, yP)
        

    for i in range(0, xP):
        xArr.append(1)

    for i in range(0, yP):
        yArr.append(1)

    #print(xArr)
    #print(yArr)

    xLen = len(xArr)
    yLen = len(yArr)

    if x < 0:
        xLen = xLen * -1
    if y < 0:
        yLen = yLen * -1

    return xLen + yLen


def commutativeCheck(x, y):

    # Addition test
    additionTest = False
    aTestXY = x + y
    aTestYX = y + x

    if aTestXY == aTestYX:
        additionTest = True

    # Multiplication test
    multiplicationTest = False
    mTestXY = x * y
    mTestYX = y * x

    if mTestXY == mTestYX:
        multiplicationTest = True
    
    if additionTest and multiplicationTest:
        return True
    
    return False
    
    
def commutativeProperty(x, y, op):
    print(" --- commutativeProperty check:")
    print("op: ", op)
    
    if op == '+' or op == '*':
        
        return commutativeCheck(x, y)
    else:
        print("Invalid op: ", op)
        return None
    
    return False

       
def noncommutativeProperty(x, y):
    print(" --- noncommutativeProperty check:")

    #print("x: ", x)
    #print("y: ", y)

    test1 = x - y
    test2 = y - x

    #print("test1: ", test1, type(test1))
    #print("test2: ", test2, type(test2))

    if test1 == test2:
        return False

    print("Order is dependent in regard to difference (- or /).")
    return True

def testFunc(f, x, y):
    return f(x, y) == f(y, x)

def numberCategory(x):
    """
    N  = Natural numbers
    N0 = Whole numbers
    Z  = Positive and negative whole numbers
    Q  = Rational numbers (for now just check for float)
    """
    cat = None

    if isinstance(x, int):
        if x > 0:
            cat = 'N'
        elif x > -1:
            cat = 'N0'
        else:
            cat = 'Z'
    elif isinstance(x, float):
        cat = 'Q'

    return cat

if __name__ == "__main__":

    print("Start: basicMath __main__")

    """

    x, y, op = input('Enter two values (x, y) and an operator (+, -, *, or /): ').split()

    x = eval(x)
    y = eval(y)

    print("type eval x: ", x, type(x))
    print("type eval y: ", y, type(y))
    print("op: ", op, type(op))
    print("numberCategory x: ", numberCategory(x))
    print("numberCategory y: ", numberCategory(y))

    if numberCategory(x) == None or numberCategory(y) == None:
        print("Unable to continue at this time. Can only handle number categfories N, N0, Z, and Q")
        sys.exit("Exiting due to mumber limitations.")

    print("Commutative check: ", commutativeProperty(x, y, op))

    print("Noncommutative check: ", noncommutativeProperty(x, y))

    print("testFunc: myAdd: ", testFunc(simpleAdd,x,y))

    print("testFunc: mySubtract: ", testFunc(simpleSubtract,x,y))

    print("myAdd:", myAdd(x, y))
    """

    print('---')
    p = pickleMemory()
    p.setupPickle()
    p.printAll()
    ans = input("Use existing data <Y/n>? ")
    if ans in ['Y', 'y']:
        a = None
        a = p.loadPickle(a)
    else:
        a = Arithmetic()
    print('--- Setup Complete ---')
    a.printAll()
    print('--- Do Stuff ---')

    
    print('--- Results ---')
    a.printAll()
    print('--- Save Stuff? ---')

    ans = input("Save current data <Y/n>? ")
    if ans in ['Y', 'y']:
        p.writePickle(a)

    print("End: basicMath __main__")
