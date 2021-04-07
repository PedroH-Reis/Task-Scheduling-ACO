from mpi4py import MPI

from functions import *

import numpy as np
# import matplotlib.pyplot as plt
import copy
import time

jsonName = "xsmallComplex.json"

numberOfProcessors = 10
numberOfIterations = 100
numberOfAnts = 16



alpha = 1.0
beta = 5.0
rho = 0.6
Q = 100.0

comm = MPI.COMM_WORLD

numberOfProcess = comm.Get_size()
Me = comm.Get_rank()
if Me == 0:
    print('''
        jsonName           = {jsonName},
        numberOfProcessors = {numberOfProcessors},
        numberOfIterations = {numberOfIterations},
        numberOfAnts       = {numberOfAnts},
        numberOfProcess    = {numberOfProcess}
    '''.format(jsonName=jsonName, numberOfProcessors= numberOfProcessors, numberOfIterations=numberOfIterations, numberOfAnts=numberOfAnts, numberOfProcess=numberOfProcess))

startTime = time.time()

ET, D, initialAllowedTasks, taskIdToTaskName, numberOfTasks = initializeInputVariables(jsonName, numberOfProcessors)
pheromone = np.full((numberOfProcessors, numberOfTasks), 1/np.mean(ET))

if Me == 0:
    x, mapInfo, processorInfo, taskInfo = initializeOutputVariables(numberOfProcessors, numberOfTasks)
    L = float("inf")
    historicL = []

sumDeltaPheromone = np.zeros((numberOfProcessors, numberOfTasks))

for i in range(numberOfIterations):
    if Me == 1:
        print("Iteration:", i)

    deltaPheromone = np.zeros((numberOfProcessors, numberOfTasks))
    antL = float("inf")

    for j in range(numberOfAnts//numberOfProcess):
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

        newAntL = costFunction(antProcessorInfo)
        deltaPheromone = deltaPheromone + antX*(Q/antL)

        if newAntL < antL:
            antL = newAntL

    minAntL = comm.reduce(antL, op = MPI.MIN, root = 0)

    comm.Reduce(deltaPheromone, sumDeltaPheromone, op = MPI.SUM, root = 0)

    if Me == 0:
        if minAntL < L:
            L = minAntL
        
        historicL.append(L)
        pheromone = (1 - rho)*pheromone + rho*sumDeltaPheromone

        comm.Bcast(pheromone, root = 0)

if Me == 0:
    print("The makespan:", L)
    print("--- %s seconds ---", time.time() - startTime)

    # plt.plot(historicL)
    # plt.ylabel("Makespan")
    # plt.xlabel("Iteration")
    # plt.show()


# print("Map Info")
# print(json.dumps(mapInfo, indent = 4))
# print()

# print("Processor Info")
# print(json.dumps(processorInfo, indent = 4))
# print()

# print("Task Info")
# print(json.dumps(taskInfo, indent = 4))
# print()