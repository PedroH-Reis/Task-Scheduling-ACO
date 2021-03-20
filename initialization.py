""""
eta nTask x nProcess
"""
import numpy as np

import json

def initializeDependancyAndExecutionTimeMatrizes(jsonPath : str, numberOfProcessors: int):
    f = open(jsonPath)
    data = json.load(f) 
    keys = data['nodes'].keys()
    nTaks = len(keys)
    D = {}
    ET = {}
    dependenciesCount = {}
    intialAllowed = []
    sum_time = 0
    for i in keys:
        actual = data['nodes'][i]
        dependenciesCount[i] = len(actual['Dependencies'])
        timeSplitted = actual["Data"].split(":")
        time = 3600*float(timeSplitted[0]) + 60*float(timeSplitted[1]) + float(timeSplitted[2])
        sum_time += time
        ET[i] = [time for i in range(numberOfProcessors)]
        if(dependenciesCount[i] == 0):
            intialAllowed.append(i)
        for j in actual['Dependencies']:
            if(j not in D):
                D[j] = []
            D[j].append(i)
    

    eta = sum_time/nTaks
    initializionPheromone = (1/eta)*np.ones((nTaks,nTaks))
    
    initializionPheromone = {i: {j:(1/eta) for j in keys} for i in keys}
    eta = {i: {j:eta for j in keys} for i in keys}
    # print(eta)

    return D,ET, intialAllowed, nTaks, dependenciesCount, eta, initializionPheromone


def initializePheromone(ET):
    pass