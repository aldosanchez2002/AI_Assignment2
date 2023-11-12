from Part1 import *
from collections import defaultdict
import re

# You will run an experiment to test six variations of your algorithms against each 
# other, as listed below. The numbers after the algorithm acronym are the parameter 
# settings. Run a round-robin tournament where you run each combination of the six 
# against each other for 100 games, recording the number of wins for each algorithm. 
# There should be 36 combinations in total. Present a table in your final report of the 
# results, showing the winning percentage for the algorithm specified on the row vs 
# the algorithm specified on the column. 

def main():
    scores = defaultdict(lambda: defaultdict(int))
    contenders = ["UR", "DLMM3", "PMCGS500", "PMCGS10000", "UCT500", "UCT10000"]
    for contender1 in contenders:
        for contender2 in contenders:
            wins = [0, 0]
            ties = 0
            for x in range(20):
                board = ["O"*7 for j in range(6)]
                winner = playGame(contender1, contender2, board)
                if winner:
                    wins[winner] += 1
                else:
                    ties+=1
            scores[contender1][contender2]+=wins[0]
            scores[contender2][contender1]+=wins[1]
            print(f"{contender1} {wins[0]} to {contender2} {wins[1]}", end=" ")
            print(f"Ties: {ties}")
    print("_"*11*(len(contenders)+1))
    prettyPrint(scores)

def prettyPrint(scores):
    '''prints dictionary into a grid'''
    grid=[]
    temp=["     "]
    for contender1 in scores.keys():
        temp.append(contender1)
    grid.append(temp)
    for contender1 in scores.keys():
        temp=[contender1]
        grid.append(temp)
    for row in grid[1:]:
        for contender2 in scores.keys():
            row.append(scores[row[0]][contender2])

    #pad all values to 11 chars
    for row in grid:
        for i in range(len(row)):
            row[i] = str(row[i]).ljust(11)
    for row in grid:
        print("".join(row))

def printBoard(board):
    for row in board:
        print("\t"+" ".join(row))
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
            if winner:
                return int(winner == "R")
            return

def getMove(algorithm, turn, board, print_mode="NONE"):
    algoName, algoParam = splitName(algorithm)
    if algoName == "UR":
        return uniformRandom(algoParam, turn, board, print_mode)
    if algoName == "DLMM":
        return depthLimitedMinMax(algoParam, turn, board, print_mode)
    if algoName == "PMCGS":
        return pureMonteCarloGameSearch(algoParam, turn, board, print_mode)
    if algoName == "UCT":
        return upperConfidenceBound(algoParam, turn, board, print_mode)

def splitName(algoName):
    RightNumberRegex = re.compile(r'\d+$')
    LeftLetterRegex = re.compile(r'^[A-Z]+')
    number = RightNumberRegex.search(algoName)
    if number:
        number = number.group()
    letters = LeftLetterRegex.search(algoName)
    if letters:
        letters = letters.group()
    if not number:
        number=0
    return letters, int(number)

if __name__ == '__main__':
    main()