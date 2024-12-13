# cell1DNA.py
#

import pickle


class Food:
    # We'll see if this works better or not...
    def __init__(
        self,
        loopCnt = 0,
        thisFood = 0,
        isPrime = False,
        runningP = 0,
        isPrimeTotal = 0
        ):

        self.loopCnt = loopCnt
        self.thisFood = thisFood
        self.isPrime = isPrime
        self.runningP = runningP
        self.isPrimeTotal = isPrimeTotal

    # How instances of the class are serialized and deserialized (pickles)
    def __reduce__(self):
        return (self.__class__, (self.loopCnt, self.thisFood, self.isPrime, self.runningP, self.isPrimeTotal))

    def printAll(self):
        print('loopCnt: ', self.loopCnt)
        print('thisFood: ', self.thisFood)
        print('isPrime: ', self.isPrime)
        print('runningP: ', self.runningP)
        print('isPrimeTotal: ', self.isPrimeTotal)

    def metabolize(self, loopCnt):

        self.loopCnt = loopCnt

        if self.loopCnt <= 10:
            print("Primary data/food. <=10")
            self.thisFood, self.isPrime = eatFood(self.loopCnt)
        else:
            if self.runningP < 50:
                print("*** Prime data/food.")
                self.thisFood, self.isPrime = eatFoodP(self.loopCnt)
            else:
                print("Primary data/food.")
                self.thisFood, self.isPrime = eatFood(self.loopCnt)

        if self.isPrime:
            self.isPrimeTotal += 1
        self.runningP = (self.isPrimeTotal / self.loopCnt) * 100
        print("M isPrimeTotal: ", self.isPrimeTotal)
        print("M loopCnt: ", self.loopCnt)
        print("M runningP: ", self.runningP)

        return

    

#/TTL
ttl = 120 # Seconds

#/STARTNUM
startNum = 1

# Need at least one second due to file opertions
#/SLEEPTIME
sleepTime = 1

# stopReplication:
# 0 allows replcation until MAXPOP (maximum file (cell) population)
# is reached (immediate stop of all cells).
# 1 stops replication, but allows existing cells to complete.
stopReplication = 1

MAXPOP = 50 # Maximum file (cell) population

#isPrimeTotal = 0

# Simple function
#
def cellFunction(newNum):
    # Principal cell function using: add one
    #/START
    return newNum + 1
    #/END


# Prime number function
#
def isNumPrime1(num):
    
    retValue = False
    
    if num > 1:
        for i in range(2, (num//2)+1):
            if (num % i) == 0:
                break
        else:
            retValue = True

    return retValue


# Attempt to emulate consumption (eating)
#
def eatFood(loopCnt):

    # Get data/food
    with open('pickles/dataFood.p', 'rb') as f:
        dataFood = pickle.load(f)
    f.close()

    thisFood = dataFood[loopCnt]

    isPrime = isNumPrime1(thisFood)
    
    return thisFood, isPrime


def eatFood2(loopCnt):

    # Get data/food
    with open('pickles/dataFood2.p', 'rb') as f:
        dataFood = pickle.load(f)
    f.close()

    thisFood = dataFood[loopCnt]

    isPrime = isNumPrime1(thisFood)
    
    return thisFood, isPrime


def eatFood3(loopCnt):

    # Get data/food
    with open('pickles/dataFood3.p', 'rb') as f:
        dataFood = pickle.load(f)
    f.close()

    thisFood = dataFood[loopCnt]

    isPrime = isNumPrime1(thisFood)
    
    return thisFood, isPrime


def eatFoodP(loopCnt):

    # Get data/food
    with open('pickles/dataFoodP.p', 'rb') as f:
        dataFood = pickle.load(f)
    f.close()

    thisFood = dataFood[loopCnt]

    isPrime = isNumPrime1(thisFood)
    
    return thisFood, isPrime

