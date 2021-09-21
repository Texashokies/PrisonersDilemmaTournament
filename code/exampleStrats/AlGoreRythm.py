#My though going in is that most people are going to submit tit for tat varients. It performs the best from the example strats and in past torunaments.
#So my algorithm is also a tit for tat variant.
#The goal is to fix problematic patterns that tft can encounter, this hopefully brings in more consistency and thus better average score.
#Such as D death loops joss can cause 
#AlGoreRythm CDD...
#Joss        DDD...
#Or a tit for tat loop
#AlGoreRythm CDC...
#Opponent    DCD...
#Or if win-stay loose-shift with a D interrupt algorithm is submitted probably won't be but let's make sure
#Al    CDDCD...
#WSLSI DDCDD...
#And detection if algorithm is random
#Most algorithms won't throw out a C after a D except for random or if it's trying to fix a tft loop
#So check for that
#I did create other algorithms to add to the population. And so some checks look to counteract bad patterns from those algorithms

import numpy as np

#All this class is for passing memory in an understandable way
class EasyMemoryFormat:
    defaultChoice = 1
    WSI = False
    foundMisplacedC = -1 # This is the point at which a misplaced C was found used so that we don't keep checking if already determined to be random
    exploited = False
    foundTftfixer = 0 # This is the point at fich a tft fixer pattern was found

def strategy(history, memory):

    #Init memory
    if history.shape[1] == 0:
        #print("New Round")
        memory = EasyMemoryFormat()
        memory.defaultChoice = 1

    #Default tit for tat behavior
    choice = memory.defaultChoice
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to defect if and only if the opponent just defected.
        choice = 0

    #Check for an early tft loop
    if history.shape[1] == 5:
        if not(0 not in history[1] or 1 not in history[1]):
            earlyTft = np.array([0,1,0,1,0],dtype=int)
            if str(history[1]) == str(earlyTft):
                #This gets out of a tft loop from susTft and hard majority
                #print("Early tft loop ", history.shape[1])
                choice = 1


    #Tit for tat strats can get in death spirals let's break those
    if history.shape[1] >= 6:
        titTatLoop = np.zeros((2,3),dtype=int)
        titTatLoop[0] = [1,0,1]
        titTatLoop[1] = [0,1,0]
        if (str(history[1,-3:]) == str(titTatLoop[1])) and (str(history[0,-3:]) == str(titTatLoop[0])):
            #print("Possibly Found tit tat loop at round ", history.shape[1])
            choice = 1
            memory.defaultChoice = 1
        if (str(history[0,-3:]) == str(titTatLoop[1])) and (str(history[1,-3:]) == str(titTatLoop[0])):
            #print("Possibly Found tit tat loop at round ", history.shape[1])
            choice = 1
            memory.defaultChoice = 1
    
    #Checks for loop that happens with interrupting winStayLose 
    if memory.WSI == True: choice = 1

    if history.shape[1] >= 6:
        wsiPat = np.zeros((2,3),dtype=int)
        wsiPat[0] = [1,0,0]
        wsiPat[1] = [0,0,1]
        if (str(history[1,-3:]) == str(wsiPat[1])) and (str(history[0,-3:]) == str(wsiPat[0])):
            #print("Possibly Found WSI loop ", history.shape[1])
            choice = 0
            memory.WSI = True

    #A difference between joss/other tft and random is that joss will never misplace a C
    #WSI can be detected by this
    if history.shape[1] >= 6 and memory.WSI == False:
        if history[1,-1] == 1 and history[0,-2] == 0 and (not memory.foundMisplacedC < history.shape[1] or memory.foundMisplacedC == -1):
            #print("Possibly rand at round ", history.shape[1])
            choice = 0
            memory.defaultChoice = 0
            memory.foundMisplacedC = history.shape[1]
            if history[1,-2] == 1 and history[1,-3] == 0 and memory.foundMisplacedC == history.shape[1]:
                #The other alg may misplace a C if it is attempting to fix a tft death loop
                #print("Possibly tit tat fixer ", history.shape[1])
                choice = 1
                memory.defaultChoice = 1
                memory.foundMisplacedC = history.shape[1]
                memory.foundTftfixer = history.shape[1]
    
    if history.shape[1] >= 7 and history.shape[1] == memory.foundTftfixer:
        if history[1,-1] == 0:
            #Not a real tft fixer
            #print("Not real fixer ", history.shape[1])
            choice = 0
            memory.defaultChoice = 0
            memory.foundTftfixer = 0
            memory.foundMisplacedC = history.shape[1]

    #Joss can interrupt in such a way that causes a D death loop
    if history.shape[1] >= 3:
        jossPat = np.zeros((2,3),dtype=int)
        jossPat[0] = [1,1,0]
        jossPat[1] = [1,0,0]
        #print(history[1,-3:])
        #print(jossPat[1])
        if (str(history[1,-3:]) == str(jossPat[1])) and (str(history[0,-3:]) == str(jossPat[0])):
            #print("Possibly Joss Pattern at round ", history.shape[1])
            choice = 1
            memory.defaultChoice = 1
            
    #This code is tripped by random if random hasn't been detected before.
    #Plus it's a good backup
    if history.shape[1] >= 5:
        losingPat = np.zeros((2,3),dtype=int)
        losingPat[0] = [1,1,1]
        losingPat[1] = [0,0,0]
        if (str(history[1,-3:]) == str(losingPat[1])) and (str(history[0,-3:]) == str(losingPat[0])):
            #print("Exploted at ", history.shape[1])
            choice = 0
            memory.defaultChoice = 0
            memory.exploited = True

    if memory.exploited == True:
        choice = 0

    return choice, memory