import random


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


def exec(jsonPath, numberOfAnts, numberOfProcessors, iterMax, alpha, beta, rho):
    D, ET, initialAllowed, numberOfTasks = initializeDependancyAndExecutionTimeMatrizes(jsonPath) # Matheus
    eta = definingEta(ET) # Matheus
    pheromone = initializePheromone(ET) # Matheus

    # The solution
    x = dict([])
    '''
    x = {
        processorId : [taskId] 
    }
    '''
    L = float("inf")

    for iter in range(iterMAX):

        for ant in numberOfAnts:
            allowed = initialAllowed
            taskId, antX = initializeAnt(allowed, numberOfProcessors) # Eylul
            updateAllowedK(D, howManyDependencies, taskId, allowed)

            for task in (numberOfTasks - 1):
                nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX) # Theodore and Pedro
                updateAllowedK() # Theodore and Pedro
                antX[nextTask, nextProcessor] = 1

            antL = costFunction(antX, ET) # Eylul
            if antL < L:
                x = antX
                L = antL
            updatePheromone(pheromone, rho, antX, ET) # Yasmine 


# Initialization test
allowedTasks = ["A", "B", "C", "D"]
numberOfProcessors = 10
taskId, antX = initializeAnt(allowedTasks, numberOfProcessors)
print(taskId)
print(antX)

# Cost function test
antX = {
    1: ["A", "B"],
    2: ["C", "D"]
}

ET = {
    "A": 35,
    "B": 30,
    "C": 40,
    "D": 10
}

print("Max execution time: ", costFunction(antX, ET))
