import numpy as np

import json

# D : dictionnary, keys = task i, values = list tasks that depends on i
# Dp : dictionnary, keys = task i, values = list parent tasks of i
# dependenciesCount : dictionnary, keys = task, values = nb of dependencies
# ET : dictionnary, keys = task, values = dictionnary, keys = processors, values = time to process task on processor
# initialAllowed = the initial allowed tasks
# nTasks = number of tasks
# InitializationPheromone = dictionnary, keys = tasks, values = dictionnary, keys = processors, values = pheromone of task i on processor j

def initializeDependancyAndExecutionTimeMatrizes(jsonPath : str, processorList : list):
    f = open(jsonPath)
    data = json.load(f) 
    tasks = data['nodes'].keys()
    nTasks = len(tasks)
    D = {}
    ET = {}
    dependenciesCount = {}
    initialAllowed = {}
    sum_time = 0
    eta = {}
    Dp = {}
    for task in tasks:
        eta[task] = {}
        ET[task] = {}
        
        task_data = data['nodes'][task]
        Dp[task] = [str(p_task) for p_task in task_data['Dependencies']]
        
        dependenciesCount[task] = len(Dp[task])
        
        timeSplitted = task_data["Data"].split(":")
        time = 3600*float(timeSplitted[0]) + 60*float(timeSplitted[1]) + float(timeSplitted[2])
        sum_time += time

        for processor in processorList:
            eta[task][processor] = (1/time)
            ET[task][processor] = time
            
        if(dependenciesCount[task] == 0):
            initialAllowed[task] = 0
            
        for parent in Dp[task]:
            
            if(parent not in D):
                D[parent] = []
            D[parent].append(task)
    
    mean_time = sum_time/nTasks
    
    initializationPheromone = {task: {processor:(1/mean_time) for processor in processorList} for task in tasks}

    return (D, dependenciesCount ,ET, initialAllowed, nTasks,  eta, initializationPheromone, Dp)

#(D, dependenciesCount ,ET, initialAllowed, nTasks,  eta, initializationPheromone, Dp) = initializeDependancyAndExecutionTimeMatrizes("data/smallRandom.json", range(1, 10))