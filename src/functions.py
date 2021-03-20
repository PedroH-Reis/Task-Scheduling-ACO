import random

# PARAM: D => A dict with the information between task dependancy
# PARAM: howManyDependancies => A dict with the information about how many dependancies has a task
# PARAM: nextTask => The nextTask is the last task mapped
# PARAM: allowed => The set to be atualized
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