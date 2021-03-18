from functions import updateAllowedK

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
			antX = initializeAnt(allowed) # Eylul

			for task in numberOfTasks:
				nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX) # Theodore and Pedro
				updateAllowedK(D, howManyDependancies, nextTask, allowedTasks) # Theodore and Pedro
				antX[nextProcessor].append(nextTask)

			antL = costfunction(antX, ET) # Eylul
			if antL < L:
				x = antX
				L = antL
			updatePheromone(pheromone, rho, antX, ET) # Yasmine
