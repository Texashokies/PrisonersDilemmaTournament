def strategy(history, memory):
    choice = 1
    if history.shape[1] == 0:
        memory = 0
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to defect if and only if the opponent just defected.
        choice = 0
        memory += 1
    
    if memory >= 5:
        choice = 0

    return choice, memory