from Part1 import *
import copy
import sys

# You will run an experiment to test six variations of your algorithms against each 
# other, as listed below. The numbers after the algorithm acronym are the parameter 
# settings. Run a round-robin tournament where you run each combination of the six 
# against each other for 100 games, recording the number of wins for each algorithm. 
# There should be 36 combinations in total. Present a table in your final report of the 
# results, showing the winning percentage for the algorithm specified on the row vs 
# the algorithm specified on the column. 

def main():
    contenders = ["UR", "DLMM5", "PMCGS500", "PMCGS10000", "UCT500", "UCT10000"]
    for contender1 in contenders:
        for contender2 in contenders:
            wins = [0, 0]
            for x in range(100):
                board = [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ]
                winner = playGame(contender1, contender2, board)
                wins[winner] += 1
                # sys.exit(0)
            print(f"{contender1} {wins[0]} to {contender2} {wins[1]}")

def printBoard(board):
    for row in board:
        print(" ".join(row))
    print()

def playGame(contender1, contender2, board):
    #yellow goes first
    Yturn = True
    while True:
        if Yturn:
            move = getMove(contender1, "Y", board)
            board = playMove(board, "Y", move)
        else:
            move = getMove(contender2, "R", board)
            board = playMove(board, "R", move)
        Yturn = not Yturn
        done, winner = isTerminal(board)
        if done:
            return int(winner == "R")

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