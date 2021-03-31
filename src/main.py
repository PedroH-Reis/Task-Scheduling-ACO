from functions import *
from initialization_utils import initializeDependancyAndExecutionTimeMatrizes
import copy
from tqdm import tqdm

def exec(jsonPath, numberOfAnts, processorList, iterMax, alpha, beta, rho):
    D, howManyDependancies, ET, initialAllowed, numberOfTasks, eta, pheromone, Dp  = initializeDependancyAndExecutionTimeMatrizes(jsonPath, processorList) # Matheus
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
            updateVariables(ant_dependancies, taskId, processorId, allowed, eta, taskInfos, processorInfos, D, Dp, ET)

            while len(allowed)>0 :
                nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos, ET) # Theodore and Pedro
                updateVariables(ant_dependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET) # Theodore and Pedro
                antX[nextProcessor].append(nextTask)

            antL = costFunction(processorInfos) # Eylul
            if antL < L:
                x = copy.deepcopy(antX)
                L = antL
                # print(antL)
                
        update_pheromone(pheromone, rho, allowed, ET,L,antX, taskInfos, processorInfos)
	
    return x

print(exec(r"./data/tasks.json", 15, range(1, 40), 10, 0.1, 0.1, 0.1))
			
			