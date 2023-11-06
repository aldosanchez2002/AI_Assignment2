from Part1 import *
import copy

# You will run an experiment to test six variations of your algorithms against each 
# other, as listed below. The numbers after the algorithm acronym are the parameter 
# settings. Run a round-robin tournament where you run each combination of the six 
# against each other for 100 games, recording the number of wins for each algorithm. 
# There should be 36 combinations in total. Present a table in your final report of the 
# results, showing the winning percentage for the algorithm specified on the row vs 
# the algorithm specified on the column. 
 
# 1) UR 
# 2) DLMM (5)  
# 3) PMCGS (500) 
# 4) PMCGS (10000)   
# 5) UCT (500)  
# 6) UCT (10000) 

def main():
    board = [
        ['O','O','O','O','O','O','O'],
        ['O','O','O','O','O','O','O'],
        ['O','O','O','O','O','O','O'],
        ['O','O','O','O','O','O','O'],
        ['O','O','O','O','O','O','O'],
        ['O','O','O','O','O','O','O'],
        ]
    contenders = ["UR","DLMM5","PMCGS500","PMCGS10000","UCT500","UCT10000"]
    for contender1 in contenders:
        for contender2 in contenders:
            wins=[0,0]
            for x in range(50):
                tempBoard = copy.deepcopy(board)
                winner = playGame(contender1,contender2,tempBoard)
                wins[winner]+=1
            wins = wins[::-1]
            for x in range(50):
                tempBoard = copy.deepcopy(board)
                winner = playGame(contender2,contender1,tempBoard)
                wins[winner]+=1
            wins = wins[::-1]
            print(f"{contender1} {wins[0]} to  {contender2} {wins[1]}")
    
def playGame(contender1, contender2, board):
    #yellow goes first
    Yturn = True
    while not isTerminal(board)[0]:
        if Yturn:
            move = getMove(contender1, "Y", board)
            board = playMove(board, "Y", move)
        else:
            move = getMove(contender2, "R", board)
            board = playMove(board, "R", move)
        Yturn = not Yturn
    if isTerminal(board)[1] == "Y":
        return 0
    return 1

def getMove(algorithm, turn, board, print_mode="NONE"):
    if algorithm == "UR":
        return uniformRandom(0, turn, board, print_mode)
    if algorithm == "DLMM5":
        return depthLimitedMinMax(5, turn, board, print_mode)
    if algorithm == "PMCGS500":
        return pureMonteCarloGameSearch(500, turn, board, print_mode)
    if algorithm == "PMCGS10000":
        return pureMonteCarloGameSearch(10000, turn, board, print_mode)
    if algorithm == "UCT500":
        return upperConfidenceBound(500, turn, board, print_mode)
    if algorithm == "UCT10000":
        return upperConfidenceBound(10000, turn, board, print_mode)

if __name__ == '__main__':
    main()