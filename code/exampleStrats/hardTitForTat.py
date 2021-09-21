def strategy(history, memory):
    choice = 1
    if history.shape[1] == 1 and history[1,-1] == 0: # Choose to defect if and only if the opponent just defected.
        choice = 0

    if history.shape[1] == 2 and (history[1,-1] == 0 or history[1,-2] == 0):
        choice = 0

    if history.shape[1] >= 3 and (history[1,-1] == 0 or history[1,-2] ==0 or history[1,-3] ==0):
        choice = 0

    return choice, None