from functions import *

import numpy as np
import matplotlib.pyplot as plt
import copy
import time

def exec(jsonName,
         numberOfProcessors, numberOfIterations, numberOfAnts,
         alpha, beta, rho, Q):
    ET, D, initialAllowedTasks, taskIdToTaskName, numberOfTasks = initializeInputVariables(jsonName, numberOfProcessors)
    x, mapInfo, processorInfo, taskInfo = initializeOutputVariables(numberOfProcessors, numberOfTasks)
    L = float("inf")

    pheromone = np.full((numberOfProcessors, numberOfTasks), 1/np.mean(ET))

    historicL = []
    for i in range(numberOfIterations):
        print("Iteration:", i)
        deltaPheromone = np.zeros((numberOfProcessors, numberOfTasks))

        for j in range(numberOfAnts):
            auxD = copy.deepcopy(D)
            allowedTasks = copy.deepcopy(initialAllowedTasks)
            antX, antMapInfo, antProcessorInfo, antTaskInfo = initializeOutputVariables(numberOfProcessors, numberOfTasks)

            nextTask, nextProcessor = initializeAnt(allowedTasks, numberOfProcessors)
            updateAllowedTasks(auxD, allowedTasks, nextTask)
            updateSolution(ET, D, nextTask, nextProcessor, antMapInfo, antProcessorInfo, antTaskInfo, antX)

            for k in range(numberOfTasks - 1):
                nextTask, nextProcessor = selectTheNextMap(D, ET, allowedTasks, antProcessorInfo, antTaskInfo, numberOfProcessors, numberOfTasks, pheromone, alpha, beta)
                updateAllowedTasks(auxD, allowedTasks, nextTask)
                updateSolution(ET, D, nextTask, nextProcessor, antMapInfo, antProcessorInfo, antTaskInfo, antX)

            antL = costFunction(antProcessorInfo)

            if antL < L:
                L = antL
                x = copy.deepcopy(antX)
                mapInfo = copy.deepcopy(antMapInfo)
                processorInfo = copy.deepcopy(antProcessorInfo)
                taskInfo = copy.deepcopy(antTaskInfo)

            deltaPheromone = deltaPheromone + antX*(Q/antL)
        
        historicL.append(L)
        pheromone = (1 - rho)*pheromone + rho*deltaPheromone
        
    mapToTaskName(taskIdToTaskName, mapInfo)
    
    return L, historicL, mapInfo, processorInfo, taskInfo

jsonName = "test-1.json"

numberOfProcessors = 2
numberOfIterations = 100
numberOfAnts = 5

alpha = 1.0
beta = 5.0
rho = 0.6
Q = 100.0

startTime = time.time()

L, historicL, mapInfo, processorInfo, taskInfo = exec(jsonName,
                                                    numberOfProcessors, numberOfIterations, numberOfAnts,
                                                    alpha, beta, rho, Q)

print("The makespan:", L)

print("--- %s seconds ---", time.time() - startTime)

plt.plot(historicL)
plt.ylabel("Makespan")
plt.xlabel("Iteration")
plt.show()

# print("Map Info")
# print(json.dumps(mapInfo, indent = 4))
# print()

# print("Processor Info")
# print(json.dumps(processorInfo, indent = 4))
# print()

# print("Task Info")
# print(json.dumps(taskInfo, indent = 4))
# print()