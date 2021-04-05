from functions import *


def TESTinitializeAnt():

    # Initialization test
    allowedTasks = ["A", "B", "C", "D"]
    numberOfProcessors = 10
    taskId, antX = initializeAnt(allowedTasks, numberOfProcessors)
    print(taskId)
    print(antX)


def TESTcostFunction():

    # Cost function test
    antX = {
        1: ["A", "B"],
        2: ["C", "D"]
    }

    ET = {
        "A": 35,
        "B": 30,
        "C": 40,
        "D": 10
    }

    print("Max execution time: ", costFunction(antX, ET))


def TESTupdateAllowedK():
    print("---------- STARTING TEST: updateAllowedK ----------")

    print("TEST 1: ", end = "")
    D = {
        1: [2, 3, 4],
        2: [5, 7],
        3: [],
        4: [6],
        5: [8],
        6: [],
        7: [9],
        8: [10],
        9: [],
        10: [],
    }
    howManyDependancies = {
        1: 0,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
    }
    nextTask = 2
    allowedK = {2, 3, 4}

    checkHowManyDependancies = howManyDependancies
    checkHowManyDependancies[2] = 0
    updateAllowedK(D, howManyDependancies, nextTask, allowedK)
    assert allowedK == {3, 4, 5, 7}, "ERROR TEST 1"
    assert howManyDependancies == checkHowManyDependancies, "ERROR TEST 1"
    print("SUCCESS")

    print("TEST 2: ", end = "")
    nextTask = 4
    updateAllowedK(D, howManyDependancies, nextTask, allowedK)
    checkHowManyDependancies = howManyDependancies
    checkHowManyDependancies[4] = 0
    assert allowedK == {3, 5, 7, 6}, "ERROR TEST 2"
    assert howManyDependancies == checkHowManyDependancies, "ERROR TEST 2"
    print("SUCCESS")

    print("TEST 3: ", end = "")
    nextTask = 6
    updateAllowedK(D, howManyDependancies, nextTask, allowedK)
    checkHowManyDependancies = howManyDependancies
    checkHowManyDependancies[6] = 0
    assert allowedK == {3, 5, 7}, "ERROR TEST 3"
    assert howManyDependancies == checkHowManyDependancies, "ERROR TEST 3"
    print("SUCCESS")
    
    print("---------- ENDING TEST: updateAllowedK ----------")

def test():
    TESTupdateAllowedK()

test()
