def exec(jsonPath, numberOfAnts, numberOfProcessors, iterMax, alpha, beta, rho):
	D, ET, initialAllowed, numberOfTasks = initializeDependancyAndExecutionTimeMatrizes(jsonPath) # Matheus
	eta = definingEta(ET) # Matheus
	pheromone = initializePheromone(ET) # Matheus
	
	# The solution
	x = np.ndarray((numberOfTasks, numberOfProcessors), int)
	L = float("inf")

	for iter in range(iterMAX):

		for ant in numberOfAnts:
			allowed = initialAllowed
			antX = initializeAnt(initialAllowed) # Eylul

			for task in numberOfTasks:
				nextTask, nextProcessor = selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX) # Theodore and Pedro
				updateAllowedK() # Theodore and Pedro
				antX[nextTask, nextProcessor] = 1

			antL = costfunction(antX, ET) # Eylul
			if antL < L:
				x = antX
				L = antL
			updatePheromone(pheromone, rho, antX, ET) # Yasmine