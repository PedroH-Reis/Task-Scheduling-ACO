from functions import *
from initialization_utils import initializeDependancyAndExecutionTimeMatrizes

def exec(jsonPath, numberOfAnts, numberOfProcessors, iterMax, alpha, beta, rho):
	D, taskInfos, processorInfos, howManyDependancies, ET, initialAllowed, numberOfTasks, eta, pheromone, Dp  = initializeDependancyAndExecutionTimeMatrizes(jsonPath, numberOfProcessors) # Matheus
	# The solution
	x = {}
	for processors in numberOfProcessors:
		x[processors] = []
	L = float("inf")

	for iter in range(iterMAX):
		for ant in numberOfAnts:
			allowed = initialAllowed
			taskId, processorId, antX, taskInfos, processorInfos = initializeAnt(ET, allowed, numberOfProcessors) # Eylul
			updateVariables(howManyDependancies, taskId, processorId, allowed, eta, taskInfos, processorInfos)

			while len(allowed)>0 :
				nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos) # Theodore and Pedro
				updateVariables(howManyDependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos) # Theodore and Pedro
				antX[nextProcessor].append(nextTask)

			antL = costfunction(processorInfos) # Eylul
			if antL < L:
				x = antX
				L = antL
<<<<<<< HEAD
			updatePheromone(pheromone, rho, antX, ET) # Yasmine

	return x

print(exec(r"./data/tasks.json", 15, 10, 10, 0.1, 0.1, 0.1))
=======
			
			update_pheromone(pheromone, rho, allowed, ET,L,antX,numberofTasks) # Yasmine
>>>>>>> f7be89d3809e4890b5baa368abfaafbc1424e674
