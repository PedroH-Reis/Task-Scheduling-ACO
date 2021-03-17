from functions import updateAllowedK

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
    assert allowedK == {3, 4, 5, 7}, "ERROR"
    assert howManyDependancies == checkHowManyDependancies, "ERROR"
    print("SUCCESS")

    print("TEST 2: ", end = "")
    nextTask = 4
    updateAllowedK(D, howManyDependancies, nextTask, allowedK)
    assert allowedK == {3, 5, 7, 6}, "ERROR"

    checkHowManyDependancies = howManyDependancies
    checkHowManyDependancies[4] = 0
    assert howManyDependancies == checkHowManyDependancies, "ERROR"
    print("SUCCESS")

    print("TEST 3: ", end = "")
    nextTask = 6
    updateAllowedK(D, howManyDependancies, nextTask, allowedK)
    assert allowedK == {3, 5, 7}, "ERROR"

    checkHowManyDependancies = howManyDependancies
    checkHowManyDependancies[6] = 0
    assert howManyDependancies == checkHowManyDependancies, "ERROR"
    print("SUCCESS")
    print("---------- ENDING TEST: updateAllowedK ----------")

def test():
    TESTupdateAllowedK()

test()
