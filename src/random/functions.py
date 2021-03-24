import ijson
import random

def initialize(jsonName):

    ET = {}
    D = {}
    allowedTasks = set()

    with open("../data/" + jsonName, 'r') as file:
        graph = ijson.items(file, "nodes")
        
        for tasks in graph:
            for task in tasks:
                splitData = tasks[task]["Data"].split(":")

                hours = float(splitData[0])
                minutes = float(splitData[1])
                seconds = float(splitData[2])

                ET[task] = hours*3600 + minutes*60 + seconds
                D[task] = [str(fatherTask) for fatherTask in tasks[task]["Dependencies"]]
                if len(D[task]) == 0:
                    allowedTasks.add(task)
                
    return ET, D, allowedTasks

def selectTheNextMap(allowedTasks, numberOfProcessors):
    nextTask = random.choice(list(allowedTasks))
    nextProcessor = random.choice(range(1, numberOfProcessors + 1))

    return nextTask, nextProcessor

def updateSolution(ET, D, nextTask, nextProcessor, x):
    startTime = 0
    endTime = 0

    for fatherTask in D[nextTask]:
        for processor in x.keys():
            if fatherTask in x[processor]["tasks"].keys():
                if x[processor]["tasks"][fatherTask]["endTime"] > startTime:
                    startTime = x[processor]["tasks"][fatherTask]["endTime"]

    if x[nextProcessor]["time"] > startTime:
        startTime = x[nextProcessor]["time"]

    endTime = startTime + ET[nextTask]

    x[nextProcessor]["tasks"][nextTask] = {
        "startTime": startTime,
        "endTime": endTime
    }

    x[nextProcessor]["time"] = endTime

def updateAllowedTasks(auxD, allowedTasks, nextTask):
    allowedTasks.remove(nextTask)

    for task in auxD.keys():
        if nextTask in auxD[task]:
            auxD[task].remove(nextTask)
            if len(auxD[task]) == 0:
                allowedTasks.add(task)

def costFunction(x):
    L = 0
    for processor in x.keys():
        if x[processor]["time"] > L:
            L = x[processor]["time"]

    return L
