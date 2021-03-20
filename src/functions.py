import random
import numpy as np

# PARAM: D => A dict with the information between task dependancy
# PARAM: howManyDependancies => A dict with the information about how many dependancies has a task
# PARAM: nextTask => The nextTask is the last task mapped
# PARAM: allowed => The set to be actualized
def updateAllowedK(D, howManyDependancies, nextTask, allowed):
    allowed.remove(nextTask)
    for task in D[nextTask]:
        howManyDependancies[task] -= 1
        if howManyDependancies[task] == 0:
            allowed.add(task)


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

    return taskId, antX


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

def selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, x):
    processors = x.keys()
    indexes = []
    proba_ind = []

    for task in allowed:
        for processor in processors:
            indexes.append([task, processor])
            proba = (pheromone[task][processor] ** alpha * eta[task][processor] ** beta)
            proba_ind.append(proba)

    proba_ind = np.array(proba_ind)/(np.sum(proba_ind))
        
    next_task, next_processor = random.choices(indexes, proba_ind)

    return (next_task, next_processor)
