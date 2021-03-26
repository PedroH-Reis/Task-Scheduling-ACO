import copy
import json
import os
from functions import *

# Strategy RTRP - Random Task Random Processor
# 1 - Take a random disponible task
# 2 - Take a random processor
# 3 - Map them
#
# Strategy RTGP - Random Task Greedy Processor
# 1 - Take a random disponible task
# 2 - Take the processor with the smallest end time
# 3 - Map them
def exec(jsonName, numberOfProcessors, strategy = "RTRP"):
    ET, D, allowedTasks, taskIdToTaskName, numberOfTasks = initializeInputVariables(jsonName, numberOfProcessors)
    mapInfo, processorInfo, taskInfo = initializeOutputVariables(numberOfProcessors, numberOfTasks)
    auxD = copy.deepcopy(D)

    for i in range(numberOfTasks):
        nextTask, nextProcessor = selectTheNextMap(allowedTasks, processorInfo, strategy)
        updateAllowedTasks(auxD, allowedTasks, nextTask)
        updateSolution(ET, D, nextTask, nextProcessor, mapInfo, processorInfo, taskInfo)
        
    L = costFunction(processorInfo)
    mapToTaskName(taskIdToTaskName, mapInfo)
    return L, mapInfo, processorInfo, taskInfo

L, mapInfo, processorInfo, taskInfo = exec("test", 2, strategy = "RTGP")

print("Map Info")
print(json.dumps(mapInfo, indent = 4))
print()

# print("Processor Info")
# print(json.dumps(processorInfo, indent = 4))
# print()

# print("Task Info")
# print(json.dumps(taskInfo, indent = 4))
# print()

print("The makespan:", L)
