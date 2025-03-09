# rna.py
#
# Fact base...~?

import sys


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
    
def commutativeProperty(x, y, op):
    print(" --- commutativeProperty check:")
    print("op: ", op)
    if op == '+':
        test1 = x + y
        test2 = y + x
    elif op == '*':
        test1 = x * y
        test2 = y * x
    else:
        print("Invalid op: ", op)
        return None

    if test1 == test2:
        return True
    
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

    print("Start: rna __main__")

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

    print("End: rna __main__")
