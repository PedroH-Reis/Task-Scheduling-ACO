import random
import numpy as np

# PARAM: global D constant => A dict with the information between task dependancy
# PARAM: global Dp constant => Reverse D
# PARAM: taskInfos => A dict, start time, end time, processor for each task
# PARAM: processorInfos => A dict, end exec time for each processor
# PARAM: schedule => mapping processor => list of tasks. Final solution
# PARAM: howManyDependancies => A dict with the information about how many dependancies has a task
# PARAM: nextTask => The nextTask is the last task mapped
# PARAM: allowed => The dictionnary to be actualized, contains task name -> (min) start time
# PARAM: eta => eta parameter
def updateVariables(howManyDependancies, nextTask, nextProcessor, allowed, eta, taskInfos, processorInfos, D, Dp, ET, meanTime, eps = 10**(-9)):
    del allowed[nextTask]
    #before adding a task to the allowed vector, we have to update eta for the current allowed tasks according to the new end time of nextProcessor
    for task in allowed:         
        #We have to take into account the begin execution time for the tasks in allowed
        eta[task][nextProcessor] = meanTime/(processorInfos[nextProcessor] + eps)

    if nextTask in D:        
        for task in D[nextTask]:
            howManyDependancies[task] -= 1
            if howManyDependancies[task] == 0:
                        
                for processor in processorInfos:
                    beginTaskTime = 0
    
                    for parentTask in Dp[task]: #we look for the parent tasks to find the begin execution time
                        beginTaskTime = max(beginTaskTime, taskInfos[nextTask]["end_time"])
                    
    
                    allowed[task] = beginTaskTime #we add the begin task time to the allowed vector
                    
                    eta[task][processor]= meanTime/(processorInfos[processor] + eps)
                    

# Chooses a random initially allowed task and assigns it randomly to a processor
    # allowedTasks -> a set of tasks with no dependency
    # numberOfProcessors -> the number of processors available
# returns:
    # taskId: assigned task's id
    # antX: dict with (processorId, [taskId])
def initializeAnt(ET, allowedTasks, processorList):
    taskId = random.choice(list(allowedTasks))
    processorId = random.choice(processorList)
    antX = {}
    for processor in processorList:
        antX[processor] = []
        
    antX[processorId] = [taskId]
        
    taskInfos= {taskId : {"start_time":0, "end_time": ET[taskId][processorId], "processor":processorId} }
    
    processorInfos = {}
    
    #We store all the processors in processorInfos (more practical)
    for processor in processorList:
        processorInfos[processor] = 0

    processorInfos[processorId] = ET[taskId][processorId]

    return taskId, processorId, antX, taskInfos, processorInfos



# Calculates the maximum execution time between all processors.
def costFunction(processorInfos):

    maxET = 0
    for processor, ET in processorInfos.items():
        if ET > maxET:
            maxET = ET

    return maxET


# PARAM: pheromone => A matrix where pheromone[i][j] contains the pheromone for task i on processor j
# PARAM: allowed => A set that contains the next tasks that can be proceeded
# PARAM: x => a dictionnary where the keys are the processors and the values the tasks that are executed on the processor

def activation(X, strategy = "argmax", min_pound = 1/4, max_pound = 3/4): #modified activation function : to allow modified random choice, min_pound & max_pound only for relu
    
    if strategy == "relu":
        maxVal = np.max(X)
        minVal = np.min(X)
        
        limit = minVal * min_pound + maxVal * max_pound #pounderation according to the maximum and mean values. enhances the convergence
        
        X = np.array(X)
        
        return np.where(X>=limit, X, X*(10**(-5))) #one can choose X/10**(5) as a minimum value

    if strategy == "max":
        maxVal = np.max(X)
        
        return np.where(X >= (maxVal-(10**(-8))), 1, 0)
    
def selectTheNextRoute(eta, alpha, pheromone, beta, allowed, antX, taskInfos, processorInfos, ET, iter, iterMax):
    processors = processorInfos.keys()
    indexes = []
    probaInd = []
    
    eps = 10**(-5)
    
    beginTime = [1/(allowed[task]+eps) for task in allowed.keys()]
    
    task = random.choices(list(allowed.keys()), beginTime)[0]
  
    for processor in processors:
        
        indexes.append([task, processor])
        proba = (pheromone[task][processor] ** alpha * eta[task][processor] ** beta) 
        
        probaInd.append(proba)
        
           
    if iter <= iterMax * 1/10: #at first we explore all the best solutions
        Id = np.argmax(probaInd)
        nextTask, nextProcessor = indexes[Id]
        
    else: #then we choose using an activation function
        nextTask, nextProcessor = random.choices(indexes, activation(probaInd, "relu"))[0]

    
    #We have to update the taskInfos and ProcessorInfos vectors
    taskInfos[nextTask] = {"start_time": (max(allowed[nextTask], processorInfos[nextProcessor])), "processor":nextProcessor}
    taskInfos[nextTask]["end_time"] = (taskInfos[nextTask]["start_time"] + ET[nextTask][nextProcessor])
    processorInfos[nextProcessor] = taskInfos[nextTask]["end_time"] 
    
    return (nextTask, nextProcessor)

def update_pheromone(pheromone, rho, allowed, ET,L,antX, taskInfos, processorInfos, meanTime, bonus = 1):
    pheromone_delta = {}
    for task in taskInfos:
        pheromone_delta[task] = {}
        for processor in processorInfos:
            if task in antX[processor]:
                pheromone_delta[task][processor] = bonus * meanTime*len(processorInfos)/L

            else:
                pheromone_delta[task][processor] = 0
                
            pheromone[task][processor] *= (1-rho)
            pheromone[task][processor] += rho * pheromone_delta[task][processor]
            
