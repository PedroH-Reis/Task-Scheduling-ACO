import random

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

            antL = costfunction(antX, ET) # Eylul
            if antL < L:
                x = antX
                L = antL
            updatePheromone(pheromone, rho, antX, ET) # Yasmine 


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


# Initialization test
allowedTasks = ["A", "B", "C", "D"]
numberOfProcessors = 10
taskId, antX = initializeAnt(allowedTasks, numberOfProcessors)
print(taskId)
print(antX)