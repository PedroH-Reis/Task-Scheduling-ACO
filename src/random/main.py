from functions import *

import copy
import time

def exec(jsonName, numberOfProcessors, strategy = "RTRP", manual = False):
    ET, D, allowedTasks, taskIdToTaskName, numberOfTasks = initializeInputVariables(jsonName, numberOfProcessors)
    mapInfo, processorInfo, taskInfo = initializeOutputVariables(numberOfProcessors, numberOfTasks)
    auxD = copy.deepcopy(D)

    for i in range(numberOfTasks):
        if manual:
            nextTask = int(input("Task: "))
            nextProcessor = int(input("Processor: "))
        else:
            nextTask, nextProcessor = selectTheNextMap(allowedTasks, processorInfo, strategy)
        updateAllowedTasks(auxD, allowedTasks, nextTask)
        updateSolution(ET, D, nextTask, nextProcessor, mapInfo, processorInfo, taskInfo)
        
    L = costFunction(processorInfo)
    mapToTaskName(taskIdToTaskName, mapInfo)

    return L, mapInfo, processorInfo, taskInfo

<<<<<<< HEAD
L, mapInfo, processorInfo, taskInfo = exec("mediumRandom", 4, strategy = "RTRP")
=======
# L, mapInfo, processorInfo, taskInfo = exec("test-1.json", 2, strategy = "RTGP", manual = False)
>>>>>>> 013e142a6658a607ba5dcd7822e94843f8c3bb99

# print("The makespan:", L)

# print("Map Info")
# print(json.dumps(mapInfo, indent = 4))
# print()

# print("Processor Info")
# print(json.dumps(processorInfo, indent = 4))
# print()

# print("Task Info")
# print(json.dumps(taskInfo, indent = 4))
# print()

startTime = time.time()

fileName = "mediumRandom.json"
numberOfProcessors = 10

RTRP = []
RTGP = []

for i in range(100):
    RTRP_L = exec(fileName, numberOfProcessors, strategy = "RTRP", manual = False)[0]
    RTGP_L = exec(fileName, numberOfProcessors, strategy = "RTGP", manual = False)[0]

    RTRP.append(RTRP_L)
    RTGP.append(RTGP_L)

RTRP_Results = {
    "min": min(RTRP),
    "max": max(RTRP),
    "mean": sum(RTRP)/len(RTRP)
}

RTGP_Results = {
    "min": min(RTGP),
    "max": max(RTGP),
    "mean": sum(RTGP)/len(RTGP)
}

print("RTRP")
print(json.dumps(RTRP_Results, indent = 4))
print()
print("RTGP")
print(json.dumps(RTGP_Results, indent = 4))
print()

print("--- %s seconds ---", time.time() - startTime)