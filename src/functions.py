# PARAM: D => A dict with the information between task dependancy
# PARAM: howManyDependancies => A dict with the information about how many dependancies has a task
# PARAM: nextTask => The nextTask is the last task mapped
# PARAM: allowed => The set to be atualized
def updateAllowedK(D, howManyDependancies, nextTask, allowed):
    allowed.remove(nextTask)
    for task in D[nextTask]:
        howManyDependancies[task] -= 1
        if howManyDependancies[task] == 0:
            allowed.add(task)
