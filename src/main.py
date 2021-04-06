from functions import *
from initialization_utils import initializeDependancyAndExecutionTimeMatrizes
import copy
from tqdm import tqdm
from mpi4py import MPI

def exec(jsonPath, numberOfAnts, processorList, iterMax, alpha, beta, rho):
    # Initializating MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print("Hello from {rank} of {size}".format(rank=rank+1, size=size))
    D, howManyDependancies, ET, initialAllowed, numberOfTasks, eta, pheromone, Dp, meanTime  = initializeDependancyAndExecutionTimeMatrizes(jsonPath, processorList) # Matheus
    # The solution
    x = {}
    for processors in processorList:
        x[processors] = []
    L = float("inf")

    # Getting the number of ants by process
    aux_tot = numberOfAnts
    numberOfAnts = (int)(numberOfAnts/size)
    if(rank == 0):
        numberOfAnts = numberOfAnts + (aux_tot - numberOfAnts*size)

    for iter in tqdm(range(iterMax)):    
        for ant in tqdm(range(numberOfAnts)):
            allowed = copy.deepcopy(initialAllowed)
            ant_dependancies = copy.deepcopy(howManyDependancies)
            taskId, processorId, antX, taskInfos, processorInfos = initializeAnt(ET, allowed, processorList) # Eylul
            updateVariables(ant_dependancies, taskId, processorId, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime)
            pheromone
            while len(allowed)>0 :
                nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos, ET, iter, iterMax) # Theodore and Pedro
                updateVariables(ant_dependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime) # Theodore and Pedro
                antX[nextProcessor].append(nextTask)

            antL = costFunction(processorInfos) # Eylul
            if antL < L:
                x = copy.deepcopy(antX)
                L = antL
        
        _, min_rank = comm.allreduce((L, rank), op= MPI.MINLOC)
        print(min_rank)
        if(rank == min_rank):
            update_pheromone(pheromone, rho, allowed, ET, L, x, taskInfos, processorInfos, meanTime)  
        pheromone = comm.bcast(pheromone, root = min_rank)
        L = comm.bcast(L, root = min_rank)
        x = comm.bcast(x, root = min_rank)
        if rho<0.5:    
            rho *= 1.01
        
	
    return (x, L)

print(exec(r"./data/mediumRandom.json", 200, range(0, 4), 10, 0.05, 2, 0.05))
			
			