# makeFood.py
#
# Generate data (food) for cells.
#

import random
import pickle


def isNumPrime(num):

    retValue = False

    if num > 1:
        for i in range(2, (num//2)+1):
            if (num % i) == 0:
                break
        else:
            retValue = True
    
    return retValue


if __name__ == "__main__":

    start = 0
    # A stop value less than loopCnt will induce starvation
    stop = 500
    foodList = []
    totalPrime = 0

    for i in range(start, stop):
        random_int = random.randint(start, stop)
        foodList.append(random_int)

        isPrime = isNumPrime(random_int)

        if isPrime:
            totalPrime += 1
            
    P = (totalPrime / stop) * 100
    print("First data/food P% ", P)
    print("len: ", len(foodList))
    
    #for n in foodList:
    #    print(n)

    # Save food and stats...
    print('Saving data/food to pickle...')
    with open("../pickles/dataFood1.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "w") as f:
        f.write("dataFood1 P% ," + str(P) + "\n")
        f.write("dataFood1 list len: ," + str(len(foodList)) + "\n")
    f.close

    print('-----')

    # Let's try something as little different...
    foodList = []
    randStop = 100
    totalPrime = 0
    
    for i in range(start, stop):
        random_int = random.randint(start, randStop)
        foodList.append(random_int)

        isPrime = isNumPrime(random_int)

        if isPrime:
            totalPrime += 1
    P = (totalPrime / stop) * 100
    print("Second data/food P% ", P)
    print("len: ", len(foodList))
    
    #for n in foodList:
    #    print(n)

    # Save differnet food
    print('Saving second data/food to pickle...')
    with open("../pickles/dataFood2.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "a") as f:
        f.write("dataFood2 P% ," + str(P) + "\n")
        f.write("dataFood2 list len: ," + str(len(foodList)) + "\n")
    f.close


    print('-----')

    # Let's force the issue...
    foodList = []
    randStop = 31
    totalPrime = 0
    
    for i in range(start, stop):
        random_int = random.randint(start, randStop)
        foodList.append(random_int)

        isPrime = isNumPrime(random_int)

        if isPrime:
            totalPrime += 1
    P = (totalPrime / stop) * 100
    print("Third data/food P% ", P)
    print("len: ", len(foodList))
    
    #for n in foodList:
    #    print(n)

    # Save differnet food
    print('Saving third data/food to pickle...')
    with open("../pickles/dataFood3.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "a") as f:
        f.write("dataFood3 P% ," + str(P) + "\n")
        f.write("dataFood3 list len: ," + str(len(foodList)) + "\n")
    f.close

    print('-----')

    # Let's force the issue some more...
    start = 0
    foodList = []
    randStart = 2
    randStop = 11
    totalPrime = 0
    
    for i in range(start, stop):
        random_int = random.randint(start, randStop)
        foodList.append(random_int)

        isPrime = isNumPrime(random_int)

        if isPrime:
            totalPrime += 1
    P = (totalPrime / stop) * 100
    print("Fourth data/food P% ", P)
    print("len: ", len(foodList))
    
    #for n in foodList:
    #    print(n)

    # Save differnet food
    print('Saving fourth data/food to pickle...')
    with open("../pickles/dataFood4.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "a") as f:
        f.write("dataFood4 P% ," + str(P) + "\n")
        f.write("dataFood4 list len: ," + str(len(foodList)) + "\n")
    f.close

    print('-----')
    
    # Can we get 75%?...
    start = 0
    foodList = []
    randStart = 2
    randStop = 7
    totalPrime = 0
    
    for i in range(start, stop):
        random_int = random.randint(start, randStop)
        foodList.append(random_int)

        isPrime = isNumPrime(random_int)

        if isPrime:
            totalPrime += 1
    P = (totalPrime / stop) * 100
    print("Fifth data/food P% ", P)
    print("len: ", len(foodList))
    
    #for n in foodList:
    #    print(n)

    # Save differnet food
    print('Saving fifth data/food to pickle...')
    with open("../pickles/dataFood5.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "a") as f:
        f.write("dataFood5 P% ," + str(P) + "\n")
        f.write("dataFood5 list len: ," + str(len(foodList)) + "\n")
    f.close


    print('-----')

    # Let's make all prime
    foodList = []
    randStop = 31
    totalPrime = 0

    primeList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
                 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                 263, 269, 271, 277, 281, 283, 293,
                 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
                 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
                 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
                 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997,
                 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
                 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171,
                 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1223, 1229, 1231, 1237, 1249, 1259, 1277,
                 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373,
                 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481,
                 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571,
                 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667,
                 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783,
                 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889,
                 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003,
                 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111,
                 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237,
                 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339,
                 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423,
                 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551,
                 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677,
                 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753,
                 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861,
                 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999,
                 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119,
                 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251,
                 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347,
                 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467,
                 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571,
                 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677,
                 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797,
                 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917,
                 3919, 3923, 3929, 3931, 3943]	         
                 
    random.shuffle(primeList)
    
    
    
    # Just for fun
    for n in primeList:
        isPrime = isNumPrime(n)

        if isPrime:
            totalPrime += 1
    P = (totalPrime / len(primeList)) * 100
    print("Prime data/food P% ", P)
    print("len primeList: ", len(primeList))

    # Save differnet food
    print('Saving all prime data/food to pickle...')
    with open("../pickles/dataFoodP.p", "wb") as f:
        pickle.dump(primeList, f)
    f.close()

    print('Saving data/food stats...')
    with open("../txt/dataFoodStats.txt", "a") as f:
        f.write("dataFoodP P% ," + str(P) + "\n")
        f.write("dataFoodP list len: ," + str(len(primeList)) + "\n")
    f.close
    