""""
eta nTask x nProcess
"""

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
    print(eta)

    return D,ET, intialAllowed, nTaks, dependenciesCount, eta


def initializePheromone(ET):
    pass