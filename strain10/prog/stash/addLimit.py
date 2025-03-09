# addLimit.py

import sys
from timeit import default_timer as timer

x = 0
startTime = timer()

while True:
    nowTime = timer()
    timePassed = nowTime - startTime
    print("timePassed: ", timePassed)
    print("memory used by x: ", sys.getsizeof(x))
    print("x:")
    print(x)
    x += 1
