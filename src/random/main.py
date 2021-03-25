import copy

from functions import *

def exec(jsonName, numberOfProcessors):
    ET, D, allowedTasks = initialize(jsonName)
    auxD = copy.deepcopy(D)

    x = {key: {"tasks": {}, "time": 0} for key in range(1, numberOfProcessors + 1)}

    for task in D.keys():
        nextTask, nextProcessor = selectTheNextMap(allowedTasks, numberOfProcessors)
        updateSolution(ET, D, nextTask, nextProcessor, x)
        updateAllowedTasks(auxD, allowedTasks, nextTask)

    L = costFunction(x)
    return L, x

L, x = exec("test.json", 2)

print(json.dumps(x, indent = 4))
print(L)
