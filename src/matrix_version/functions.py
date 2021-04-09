import numpy as np

import json
import random

def initializeInputVariables(jsonName, numberOfProcessors):
    with open("./src/data/" + jsonName, "r") as file:
        data = json.load(file)
        tasks = data["nodes"]

    taskIdToTaskName = [task for task in tasks]

    numberOfTasks = len(taskIdToTaskName)
    ET = np.zeros(numberOfTasks)
    D = np.zeros(numberOfTasks, dtype = object)
    allowedTasks = set()

    for task in tasks:
        splittedData = tasks[task]["Data"].split(":")
        hours = float(splittedData[0])
        minutes = float(splittedData[1])
        seconds = float(splittedData[2])

        taskId = taskIdToTaskName.index(task)
        ET[taskId] = hours*3600 + minutes*60 + seconds

        D[taskId] = [taskIdToTaskName.index(str(fatherTask)) for fatherTask in tasks[task]["Dependencies"]]
        
        if len(D[taskId]) == 0:
            allowedTasks.add(taskId)
                
    return ET, D, allowedTasks, taskIdToTaskName, numberOfTasks

def initializeOutputVariables(numberOfProcessors, numberOfTasks):

    processorInfoDict = {
        "endTime": 0
    }

    taskInfoDict = {
        "processor": None,
        "startTime": None,
        "endTime": None
    }

    mapInfo = []
    processorInfo = [processorInfoDict for i in range(numberOfProcessors)]
    taskInfo = [taskInfoDict for i in range(numberOfTasks)]

    x = np.zeros((numberOfProcessors, numberOfTasks))

    return x, mapInfo, processorInfo, taskInfo

def initializeAnt(allowedTasks, numberOfProcessors):
    nextTask = random.choice(list(allowedTasks))
    nextProcessor = random.choice(range(numberOfProcessors))

    return nextTask, nextProcessor

def selectTheNextMap(D, ET, allowedTasks, processorInfo, taskInfo, numberOfProcessors, numberOfTasks, pheromone, alpha, beta):
    eta = np.zeros((numberOfProcessors, numberOfTasks))
    for task in allowedTasks:
        for processor in range(numberOfProcessors):
            endTime = calculateStartAndEndTime(ET, D, task, processor, taskInfo, processorInfo)[1]
            eta[processor][task] = 1/endTime

    probability = pheromone**alpha * eta**beta
    probability = probability/np.sum(probability)

    accumulatedProbability = 0
    randomNumber = random.uniform(0, 1)
    for task in allowedTasks:
        for processor in range(numberOfProcessors):
            accumulatedProbability += probability[processor][task]
            if randomNumber < accumulatedProbability:
                return task, processor

def calculateStartAndEndTime(ET, D, task, processor, taskInfo, processorInfo):
    startTime = 0
    endTime = 0
    for fatherTask in D[task]:
        if taskInfo[fatherTask]["processor"] != None:
            if taskInfo[fatherTask]["endTime"] > startTime:
                startTime = taskInfo[fatherTask]["endTime"]

    if processorInfo[processor]["endTime"] > startTime:
        startTime = processorInfo[processor]["endTime"]

    endTime = startTime + ET[task]

    return startTime, endTime


def updateAllowedTasks(auxD, allowedTasks, lastTaskExecuted):
    allowedTasks.remove(lastTaskExecuted)

    for task in range(len(auxD)):
        if lastTaskExecuted in auxD[task]:
            auxD[task].remove(lastTaskExecuted)
            if len(auxD[task]) == 0:
                allowedTasks.add(task)

def updateSolution(ET, D, nextTask, nextProcessor, mapInfo, processorInfo, taskInfo, x):
    startTime, endTime = calculateStartAndEndTime(ET, D, nextTask, nextProcessor, taskInfo, processorInfo)

    mapInfo.append({
        "processor": nextProcessor,
        "task": nextTask,
        "startTime": startTime,
        "endTime": endTime
    })

    processorInfo[nextProcessor] = {
        "endTime": endTime
    }

    taskInfo[nextTask] = {
        "processor": nextProcessor,
        "startTime": startTime,
        "endTime": endTime
    }

    x[nextProcessor][nextTask] = 1

def costFunction(processorInfo):
    L = 0
    for processor in processorInfo:
        if processor["endTime"] > L:
            L = processor["endTime"]

    return L

def mapToTaskName(taskIdToTaskName, mapInfo):
    for allocation in mapInfo:
        allocation["task"] = taskIdToTaskName[allocation["task"]]
