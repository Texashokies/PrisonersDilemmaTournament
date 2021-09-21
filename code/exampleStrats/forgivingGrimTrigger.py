# Strategy known as "Forrgviing Grim Trigger" or "Grudger".
# We will cooperate repeatedly until our opponent betrays us twice.
# Then, we will get angry and defect for the rest of time.
# Memory is the number of times the strategy has been wronged

def strategy(history, memory):
    wronged = memory
    if history.shape[1] ==0:
        wronged = 0
    if history.shape[1] >= 1 and history[1,-1] == 0: # Just got wronged.
        wronged += 1
    
    if wronged >= 2:
        return 0, wronged
    else:
        return 1, wronged
    