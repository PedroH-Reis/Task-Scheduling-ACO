from functions import *
from initialization_utils import initializeDependancyAndExecutionTimeMatrizes
import copy


def exec(jsonPath, numberOfAnts, processorList, iterMax, alpha, beta, rho1, rho2):
    D, howManyDependancies, ET, initialAllowed, numberOfTasks, eta, pheromone, Dp, meanTime  = initializeDependancyAndExecutionTimeMatrizes(jsonPath, processorList) # Matheus
    # The solution
    x = {}
    for processors in processorList:
        x[processors] = []
    L = float("inf")

    for iter in tqdm(range(iterMax)):    
        for ant in tqdm(range(numberOfAnts)):
            allowed = copy.deepcopy(initialAllowed)
            ant_dependancies = copy.deepcopy(howManyDependancies)
            taskId, processorId, antX, taskInfos, processorInfos = initializeAnt(ET, allowed, processorList) # Eylul
            updateVariables(ant_dependancies, taskId, processorId, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime)

            while len(allowed)>0 :
                nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos, ET) # Theodore and Pedro
                updateVariables(ant_dependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime) # Theodore and Pedro
                antX[nextProcessor].append(nextTask)

            antL = costFunction(processorInfos) # Eylul
            if antL < L:
                x = copy.deepcopy(antX)
                L = antL
                print(L)
                update_pheromone(pheromone, rho2, allowed, ET, L, x, taskInfos, processorInfos, meanTime, 1.5)

            update_pheromone(pheromone, rho1, allowed, ET, antL, antX, taskInfos, processorInfos, meanTime)  
            

        if rho1>0.4:    
            rho1 *= 0.99
        if rho2>0.6:    
            rho2 *= 0.99
        
	
    return (x, L)

print(exec(r"./data/mediumRandom.json", 10, range(0, 10), 50, 3, 5, 1, 1))
			
			