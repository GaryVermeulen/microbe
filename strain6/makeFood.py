# makeFood.py
#
# Generate data (food) for cells.
#

import random
import pickle


if __name__ == "__main__":

    start = 0
    # A stop value less than loopCnt will induce starvation
    stop = 200
    foodList = []

    for i in range(start, stop):
        random_int = random.randint(start, stop)
        foodList.append(random_int)

    for n in foodList:
        print(n)

    # Save food
    print('Saving data/food to pickle...')
    with open("dataFood.p", "wb") as f:
        pickle.dump(foodList, f)
    f.close()
    
