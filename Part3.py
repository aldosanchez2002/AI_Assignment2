import sys
from Part1 import *
from Part2 import *
'''
This file is for player itneraction to play against the AI
'''

def selectAI():
    choice = ""
    while choice not in ["1", "2", "3", "4", "5"]:
        print("Welcome to Connect 4!")
        print("You will be playing as Yellow (Y) against the AI as Red (R)")
        print("Select which AI you want to play against:")
        print("1. Random AI")
        print("2. Minimax AI")
        print("3. Monte Carlo AI")
        print("4. Upper Confidence Tree AI")  
        print("5. Exit")
        choice = input()
    if choice == "5":
        sys.exit(0)
    if choice == "1":
        return "UR"
    if choice == "2":
        param=-1
        while param >10 or param < 0:
            param = int(input("Enter dificulty for Minimax AI (0-10)"))
        return "DLMM"+str(param)
    if choice == "3":
        param=-1
        while param >10000 or param < 0:
            param = int(input("Enter number of simulations for Monte Carlo AI (0-10000)"))
        return "PMCGS"+str(param)
    if choice == "4":
        param=-1
        while param >10000 or param < 0:
            param = int(input("Enter number of simulations for Upper Confidence Tree AI (0-10000)"))
        return "UCT"+str(param)

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
    board = ["O"*6 for j in range(5)]
    opponent = selectAI()
    while not isTerminal(board)[0]:
        validMove = False
        while not validMove:
            move = selectMove(board)
            newboard = playMove(board, "Y", move)
            if not newboard:
                print("\tINVALID MOVE")
            else:
                board = newboard
                validMove = True
            
        if isTerminal(board)[0]:
            break
        print("AI is thinking...", end="\r")
        move = getMove(opponent, "R", board)
        print(f"AI played in column {move}")
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
            opponent = "Depth Limited Minimax AI"
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