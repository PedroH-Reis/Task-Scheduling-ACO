import random
import numpy as np

# PARAM: global D constant => A dict with the information between task dependancy
# PARAM: global Dp constant => Reverse D
# PARAM: taskInfos => A dict, start time, end time, processor for each task
# PARAM: processorInfos => A dict, end exec time for each processor
# PARAM: schedule => mapping processor => list of tasks. Final solution
# PARAM: howManyDependancies => A dict with the information about how many dependancies has a task
# PARAM: nextTask => The nextTask is the last task mapped
# PARAM: allowed => The dictionnary to be actualized, contains task name -> (min) start time
# PARAM: eta => eta parameter
def updateVariables(howManyDependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET):
    del allowed[nextTask]

    #before adding a task to the allowed vector, we have to update eta for the current allowed tasks according to the new end time of nextProcessor
    for task in allowed:
        #We have to take into account the begin execution time for the tasks in allowed
        eta[task][nextProcessor] = 1/(max(processorInfos[nextProcessor], taskInfos[task]["begin_time"]) + ET[task])

    for task in D[nextTask]:
        howManyDependancies[task] -= 1
        if howManyDependancies[task] == 0:

            #Eta update.
            for processor in processorInfos:
                beginTaskTime = 0

                for parentTask in Dp[task]: #we look for the parent tasks to find the begin execution time
                    beginTaskTime = max(beginTaskTime, taskInfos[nextTask]["end_time"])
                

                allowed[task] = beginTaskTime #we add the begin task time to the allowed vector

                eta[task][processor] = 1/(max(processorInfos[processor], beginTaskTime) + ET[task]) #We have to take into account the allowed execution time for the processor.



# Chooses a random initially allowed task and assigns it randomly to a processor
    # allowedTasks -> a set of tasks with no dependency
    # numberOfProcessors -> the number of processors available
# returns:
    # taskId: assigned task's id
    # antX: dict with (processorId, [taskId])
def initializeAnt(allowedTasks, numberOfProcessors):
    taskId = random.choice(list(allowedTasks))
    processorId = random.randint(1, numberOfProcessors)
    antX = {
        processorId: [taskId]
    } 

    return taskId, processorId, antX


# Calculates the total execution time of a list of task IDs.
def calculateET(taskList, ET):

    sum = 0
    for task in taskList:
        sum += ET[task]
    
    return sum


# Calculates the maximum execution time between all processors.
def costFunction(antX, ET):

    maxET = 0
    for processor, taskList in antX.items():
        currentET = calculateET(taskList, ET)
        if currentET > maxET:
            maxET = currentET

    return maxET


# PARAM: pheromone => A matrix where pheromone[i][j] contains the pheromone for task i on processor j
# PARAM: allowed => A set that contains the next tasks that can be proceeded
# PARAM: x => a dictionnary where the keys are the processors and the values the tasks that are executed on the processor

def selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos):
    processors = processorInfos.keys()
    indexes = []
    probaInd = []

    for task in allowed:
        for processor in processors:
            indexes.append([task, processor])
            proba = (pheromone[task][processor] ** alpha * eta[task][processor] ** beta) #Maybe we should normalize eta so that it doesn't become too small
            probaInd.append(proba)

    probaInd = np.array(probaInd)/(np.sum(probaInd))
        
    nextTask, nextProcessor = random.choices(indexes, probaInd)[0]

    #We have to update the taskInfos and ProcessorInfos vectors
    taskInfos[nextTask] = {"start_time": (max(allowed[nextTask], processorInfos)), "processor":nextProcessor}
    taskInfos[nextTask]["end_time"] = (taskInfos[nextTask] + ET[nextTask])}
    processorInfos[nextProcessor] = taskInfos[nextTask]["end_time"] 
    
    return (nextTask, nextProcessor)

def _update_pheromone(pheromone, rho, allowed, ET,L,antX,numberofTasks,Q):
    pheromone_delta = [[0 for j in range( numberOfTasks)] for i in range(numberOfTasks)]
    for i in ET:
        for j in allowed:
            if i in antX and j in antX:
                pheromone_delta[i][j] = Q/L
            else:
                pheromone_delta[i][j] = 0
        pheromone[i][j] *= 1-rho
        pheromone[i][j] += pheromone_delta[i][j]
