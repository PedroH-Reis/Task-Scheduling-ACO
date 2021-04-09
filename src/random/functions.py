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

    return mapInfo, processorInfo, taskInfo

def selectTheNextMap(allowedTasks, processorInfo, strategy = "RTRP"):
    nextTask = random.choice(list(allowedTasks))
    nextProcessor = 0

    if strategy == "RTRP":
        nextProcessor = random.choice(range(len(processorInfo)))
    elif strategy == "RTGP":
        for processor in range(1, len(processorInfo)):
            if processorInfo[processor]["endTime"] < processorInfo[nextProcessor]["endTime"]:
                nextProcessor = processor
    else:
        raise Exception("ERROR: Strategy not supported!")

    return nextTask, nextProcessor

def updateAllowedTasks(auxD, allowedTasks, lastTaskExecuted):
    allowedTasks.remove(lastTaskExecuted)

    for task in range(len(auxD)):
        if lastTaskExecuted in auxD[task]:
            auxD[task].remove(lastTaskExecuted)
            if len(auxD[task]) == 0:
                allowedTasks.add(task)

def updateSolution(ET, D, nextTask, nextProcessor, mapInfo, processorInfo, taskInfo):
    startTime = 0
    endTime = 0

    for fatherTask in D[nextTask]:
        if taskInfo[fatherTask]["endTime"] > startTime:
            startTime = taskInfo[fatherTask]["endTime"]

    if processorInfo[nextProcessor]["endTime"] > startTime:
        startTime = processorInfo[nextProcessor]["endTime"]

    endTime = startTime + ET[nextTask]

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

def costFunction(processorInfo):
    L = 0
    for processor in processorInfo:
        if processor["endTime"] > L:
            L = processor["endTime"]

    return L

def mapToTaskName(taskIdToTaskName, mapInfo):
    for allocation in mapInfo:
        allocation["task"] = taskIdToTaskName[allocation["task"]]
        