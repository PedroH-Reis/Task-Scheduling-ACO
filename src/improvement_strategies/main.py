from functions import *
from initialization_utils import initializeDependancyAndExecutionTimeMatrizes
import copy
from tqdm import tqdm

def exec(jsonPath, numberOfAnts, processorList, iterMax, alpha, beta, rho):
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
                nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos, ET, iter, iterMax) # Theodore and Pedro
                updateVariables(ant_dependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime) # Theodore and Pedro
                antX[nextProcessor].append(nextTask)

            antL = costFunction(processorInfos) # Eylul
            if antL < L:
                x = copy.deepcopy(antX)
                L = antL
                print(L)
                
        update_pheromone(pheromone, rho, allowed, ET, L, x, taskInfos, processorInfos, meanTime)  
        

        if rho<0.5:    
            rho *= 1.01
        
	
    return (x, L)

print(exec(r"./src/data/smallComplex.json", 200, range(0, 10), 10, 1, 5, 0.05))
			
			