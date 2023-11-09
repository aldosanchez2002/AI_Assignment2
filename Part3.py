import sys
from Part1 import *
from Part2 import *
'''
This file is for player itneraction to play against the AI
'''

columns = 7
rows = 6

def selectAI():
    choice = ""
    while choice not in ["1", "2", "3", "4", "5", "6"]:
        print("Welcome to Connect 4!")
        print("You will be playing as Yellow (Y) against the AI as Red (R)")
        print("Select which AI you want to play against:")
        print("1. Random AI")
        print("2. MinMax AI")
        print("3. Monte Carlo AI")
        print("4. Upper Confidence Tree AI")  
        print("5. Change board size")
        print("6. Exit")
        choice = input()
    if choice == "6":
        sys.exit(0)
    if choice == "5":
        setBoardSize()
        return selectAI()
    if choice == "1":
        return "UR"
    if choice == "2":
        param=-1
        maxDepth = 10
        while param >maxDepth or param < 0:
            param = int(input(f"Enter dificulty for Minimax AI (0-{maxDepth})"))
        return f"DLMM{param}"
    if choice == "3":
        param=-1
        maxParam = 10000
        while param >maxParam or param < 0:
            param = int(input(f"Enter number of simulations for Monte Carlo AI (0-{maxParam})"))
        return f"PMCGS{param}"
    if choice == "4":
        param=-1
        maxParam = 10000
        while param > maxParam or param < 0:
            param = int(input(f"Enter number of simulations for Upper Confidence Tree AI (0-{maxParam})"))
        return f"UCT{param}"

def setBoardSize():
    global columns
    global rows
    columns = -1
    rows = -1
    while columns not in range(4, 11):
        columns = int(input("Enter number of columns (4-10): "))
    while rows not in range(4, 11):
        rows = int(input("Enter number of rows (4-10): "))
    print(f"Board size set to {columns}x{rows}\n")

def selectMove(board):
    move = -1
    columns = [i+1 for i in range(len(board[0]))]
    print("\t"+" ".join([str(i) for i in columns]))
    print()
    for row in board:
        print("\t"+" ".join(row))
    while move not in range(1,len(board[0])+1):
        move = input(f"Select a column to play in (1-{len(board[0])}): ")
        try:
            move = int(move)
            if not isLegalMove(board, move-1):
                move = -1
        except:
            move = -1
    return move-1
    
def playAI():
    global flag
    board = ["O"*columns for j in range(rows)]
    opponent = selectAI()
    while not isTerminal(board)[0]:
        move = selectMove(board)
        board = playMove(board, "Y", move)
        if isTerminal(board)[0]:
            break
        print("AI is thinking... consider a smaller board", end="\r")
        move = getMove(opponent, "R", board)
        print(f"AI played in column {move+1}")
        board = playMove(board, "R", move)
    _, winner = isTerminal(board)
    print("Final Board:")
    printBoard(board)
    if winner == "O":
        print(f"Game ended in a tie")
    else:
        if "UR" in opponent:
            opponent = "Uniform Random AI"
        elif "DLMM" in opponent:
            opponent = "Depth Limited MinMax AI"
        elif "PMCGS" in opponent:
            opponent = "Pure Monte Carlo AI"
        elif "UCT" in opponent:
            opponent = "Upper Confidence Tree AI"
        if winner == "R":
            print(f"{opponent} won!!")
        else:
            print(f"You beat {opponent}!!")
    choice = -1
    while choice not in ["1", "2"]:
        choice = input("1. Play again\n2. Exit\n")
    if choice == "1":
        playAI()

if __name__ == "__main__":
    playAI()