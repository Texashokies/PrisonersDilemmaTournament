import numpy as np
def strategy(history, memory):
    choice = 0

    numC = np.count_nonzero(history[1])
    if history.shape[1] >= 1 and (numC > (history.shape[1] - numC)):
        choice = 1
    return choice, None