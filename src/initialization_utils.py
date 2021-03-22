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
    eta = {}
    for i in keys:
        actual = data['nodes'][i]
        dependenciesCount[i] = len(actual['Dependencies'])
        timeSplitted = actual["Data"].split(":")
        time = 3600*float(timeSplitted[0]) + 60*float(timeSplitted[1]) + float(timeSplitted[2])
        sum_time += time
        ET[i] = [time for i in range(numberOfProcessors)]
        for j in range(numberOfProcessors):
            if j not in eta:
                eta[j] = {}
            eta[j][i] = 1/time
        if(dependenciesCount[i] == 0):
            intialAllowed.append(i)
        for j in actual['Dependencies']:
            if(j not in D):
                D[j] = []
            D[j].append(i)
    
    mean_time = sum_time/nTaks

    initializionPheromone = {i: {j:(1/mean_time) for j in keys} for i in keys}
    

    return D, dependenciesCount ,ET, intialAllowed, nTaks,  eta, initializionPheromone

