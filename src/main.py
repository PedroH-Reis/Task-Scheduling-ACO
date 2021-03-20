from functions import *

def exec(jsonPath, numberOfAnts, numberOfProcessors, iterMax, alpha, beta, rho):
	D, howManyDependancies, ET, initialAllowed, numberOfTasks = initializeDependancyAndExecutionTimeMatrizes(jsonPath) # Matheus
	eta = definingEta(ET) #Matheus
	pheromone = initializePheromone(ET) # Matheus
	
	# The solution
	x = {}
	for processors in numberOfProcessors:
		x[processors] = []
	L = float("inf")

	for iter in range(iterMAX):
		for ant in numberOfAnts:
			allowed = initialAllowed
			taskId, antX = initializeAnt(allowed, numberOfProcessors) # Eylul
			updateAllowedK(D, howManyDependencies, taskId, allowed)

			while len(allowed)>0 :
				nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, x) # Theodore and Pedro
				updateAllowedK(D, howManyDependancies, nextTask, allowed) # Theodore and Pedro
				antX[nextProcessor].append(nextTask)

			antL = costfunction(antX, ET) # Eylul
			if antL < L:
				x = antX
				L = antL
			updatePheromone(pheromone, rho, antX, ET) # Yasmine
