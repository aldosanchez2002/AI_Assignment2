import sys
import numpy as np
import random

def isTerminal(board):
    if not board:
        raise Exception("Empty board")
    # Horozontal -
    for i in range(len(board)):
        for j in range(len(board[0])-3):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] != 'O':
                return [True, board[i][j]]
    # Vertical |
    for i in range(len(board)-3):
        for j in range(len(board[0])):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] != 'O':
                return [True, board[i][j]]
    # Diagonal /
    for i in range(len(board)-3):
        for j in range(len(board[0])-3):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != 'O':
                return [True, board[i][j]]
    # Diagonal \
    for i in range(len(board)-3):
        for j in range(3, len(board[0])):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] != 'O':
                return [True, board[i][j]]
    
    # Check if there's any empty spaces left
    if 'O' not in board[0]:
        return [True, 'O']
    return [False, None]  

def heuristic2B(board,player):
    '''
     For each set, if a player is the only player who has pieces inside that set, 
     then that player will receive a point for each piece they have in that set. 
     This means pieces will be counted multiple times if they appear in multiple 
     sets which are only occupied by that player. 
     "Set" refers to a consecurtive group of 4 spaces.
    '''
    # window count checks if there's none of the other player's tokens in the window
    score = 0
    # Horozontal -
    for i in range(len(board)):
        for j in range(len(board[0])-3):
            window = board[i][j:j+4]
            if window.count(player) + window.count("O") == 4:
                windowScore = window.count(player)
                if windowScore == 3:
                    windowScore = 100
                score += windowScore
    # Vertical |
    for i in range(len(board)-3):
        for j in range(len(board[0])):
            window = [board[i+k][j] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                windowScore = window.count(player)
                if windowScore == 3:
                    windowScore = 100
                score += windowScore
    # Diagonal /
    for i in range(len(board)-3):
        for j in range(len(board[0])-3):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                windowScore = window.count(player)
                if windowScore == 3:
                    windowScore = 100
                score += windowScore
    # Diagonal \
    for i in range(len(board)-3):
        for j in range(3, len(board[0])):
            window = [board[i+k][j-k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                windowScore = window.count(player)
                if windowScore == 3:
                    windowScore = 100
                score += windowScore
    return score - heuristic1(board, flipPlayer(player))

def heuristic2(board,player):
    '''
     For each set, if a player is the only player who has pieces inside that set, 
     then that player will receive a point for each piece they have in that set. 
     This means pieces will be counted multiple times if they appear in multiple 
     sets which are only occupied by that player. 
     "Set" refers to a consecurtive group of 4 spaces.
    '''
    # window count checks if there's none of the other player's tokens in the window
    score = 0
    # Horozontal -
    for i in range(len(board)):
        for j in range(len(board[0])-3):
            window = board[i][j:j+4]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    # Vertical |
    for i in range(len(board)-3):
        for j in range(len(board[0])):
            window = [board[i+k][j] for k in range(4)]
            if window.count(player) + window.count("O") == 4: 
                score += window.count(player)
    # Diagonal /
    for i in range(len(board)-3):
        for j in range(len(board[0])-3):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    # Diagonal \
    for i in range(len(board)-3):
        for j in range(3, len(board[0])):
            window = [board[i+k][j-k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    return max(0,score - heuristic2B(board, flipPlayer(player)))

def heuristic1(board,player):
    '''
     For each set, if a player is the only player who has pieces inside that set, 
     then that player will receive a point for each piece they have in that set. 
     This means pieces will be counted multiple times if they appear in multiple 
     sets which are only occupied by that player. 
     "Set" refers to a consecurtive group of 4 spaces.
    '''
    # window count checks if there's none of the other player's tokens in the window
    score = 0
    # Horozontal -
    for i in range(len(board)):
        for j in range(len(board[0])-3):
            window = board[i][j:j+4]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    # Vertical |
    for i in range(len(board)-3):
        for j in range(len(board[0])):
            window = [board[i+k][j] for k in range(4)]
            if window.count(player) + window.count("O") == 4: 
                score += window.count(player)
    # Diagonal /
    for i in range(len(board)-3):
        for j in range(len(board[0])-3):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    # Diagonal \
    for i in range(len(board)-3):
        for j in range(3, len(board[0])):
            window = [board[i+k][j-k] for k in range(4)]
            if window.count(player) + window.count("O") == 4:
                score += window.count(player)
    return score

def playMove(board, player, move, print_mode="BRIEF"):
    '''
    Returns a new board with the move applied if the move is legal, otherwise returns False
    '''
    temp_board = [row[:] for row in board]
    if print_mode in ["VERBOSE"]:
        print(f"Player {player} plays in column {move}")
        for row in temp_board:
            print("\t"+" ".join(row))
    for i in range(len(temp_board)-1, -1, -1):
        if temp_board[i][move] == 'O':
            temp_board[i] = temp_board[i][:move] + player + temp_board[i][move+1:]
            return temp_board
    raise Exception("Invalid move")

def isLegalMove(board, move):
    return board[0][move] == 'O'

def flipPlayer(player):
    return 'R' if player == 'Y' else 'Y'

def depthLimitedMinMax(maxDepth, turn, board, print_mode="VERBOSE"):
    return depthLimitedMinMaxAux(maxDepth, turn, board, print_mode)[1]

def depthLimitedMinMaxAux(maxDepth, turn, board, print_mode="none"):
    scores = {}

    if print_mode in ["VERBOSE", "BRIEF"]:
        print(f"Depth Limited MinMax Algorithm with maxDepth={maxDepth}")
        input()

    if print_mode == "VERBOSE":
        for row in board:
            print("\t" + " ".join(row))

    for col in range(len(board[0])):
        if print_mode == "VERBOSE":
            print(f"Trying {turn} plays in column {col}")
        if not isLegalMove(board, col):
            if print_mode == "VERBOSE":
                print("Move Unsuccessful")
        else:
            board = playMove(board, turn, col)
            if print_mode == "VERBOSE":
                print("Move Successful")
                for row in board:
                    print("\t" + " ".join(row))
                input()
            isDone,winner = isTerminal(board)
            if isDone:
                if winner == turn:
                    return float('inf'), col
                if winner == flipPlayer(turn):
                    return float('-1'), col
                return 0, col # tie
            if maxDepth == 1:
                scores[col]=heuristic2(board, turn)
            else:
                score, _ = depthLimitedMinMaxAux(maxDepth-1, flipPlayer(turn), board)
                scores[col]=score
    if maxDepth % 2 == 0:
        score = max(scores.values())
        max_indices = [key for key in scores.keys() if scores[key] == score]
        index = random.choice(max_indices)
    else:
        score = min(scores.values())
        min_indices = [key for key in scores.keys() if scores[key] == score]
        index = random.choice(min_indices)

    return score, index

def uniformRandom(parameter, turn, board, print_mode="VERBOSE"):
    '''
    This is a trivial algorithm used for basic testing and benchmarking. It selects a legal 
    move for the specified player using the uniform random strategy (i.e., each legal 
    move is selected with the same probability. The parameter value should always be 0 
    for this algorithm. 
    '''
    if print_mode in ["VERBOSE","BRIEF"]:
        print("Uniform Random Algorithm")
    possible_moves = [i for i in range(len(board[0])) if board[0][i] == 'O']
    if print_mode in ["VERBOSE"]:
        print(f"Possible Moves: {possible_moves}")
    np.random.shuffle(possible_moves)
    if possible_moves:
        if print_mode in ["VERBOSE"]:
            print(f"Move Randomly Selected: {possible_moves[0]}")
        return possible_moves[0]
    raise Exception("No possible moves")

def pureMonteCarloGameSearch(parameter, turn, board, print_mode="VERBOSE"):
    '''
    This algorithm is the simplest form of game tree search based on randomized 
    rollouts. It is essentially the UCT algorithm without a sophisticated tree search 
    policy. Please refer to https://en.wikipedia.org/wiki/Monte_Carlo_tree_search for 
    detailed descriptions and examples for both PMCGS and UCT (of course you can also 
    use the course slides, textbook, and other references as needed). The main steps in 
    this algorithm are the same as in UCT, but every move both within the tree search 
    and the rollout is made at random. Output the value for each of the immediate next 
    moves (with Null for illegal moves) and the move selected at the end. Only if the 
    “Verbose” mode is selected you should also print out additional information during 
    each simulation trace, as shown below. For each node in the search tree output the 
    current values of wi and ni, and the move selected. When you reach a leaf in the 
    current tree and add a new node print “NODE ADDED”. For the rollout print only the 
    moves selected, and when you reach a terminal node print the value as “TERMINAL 
    NODE VALUE: X” where X is -1, 0, or 1. Then print the updated values. Example in 
    Instructions.pdf
    '''
    return uniformRandom(parameter, turn, board, print_mode)

def upperConfidenceBound(parameter, turn, board, print_mode="VERBOSE"):
    '''
    Builds on PMCGS and uses most of the same structure. The only 
    difference is in how nodes are selected within the existing search tree; instead of 
    selecting randomly the nodes are selected using the Upper Confidence Bounds 
    (UCB) algorithm. For any node that is NOT a leaf (i.e., all possible children are 
    already in the tree), calculate the UCB value for all children, and pick the one with 
    the highest (or lowest) value depending on which player is choosing a move. The 
    output should be mostly the same as for PMCGS, but adds the UCB values computed 
    for the children before specifying the move that is selected for the tree search part 
    of the simulation when in “Verbose” mode. Note that the final values printed for the 
    children of the root and the final move selection are NOT based on the UCB 
    equation, but the direct estimate of the node value (i.e., just wi/ni). Example in 
    Instructions.pdf
    '''
    return uniformRandom(parameter, turn, board, print_mode)

def injestTestFile(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()
        algorithm = content[0].strip().upper()
        parameter = int(content[1].strip())
        turn = content[2].strip()
        board = [line.strip() for line in content[3:]]
        board = [char for char in [line.strip().split() for line in board]]
        board = [b[0] for b in board]
    return algorithm, parameter, turn, board

if __name__ == "__main__":

    def input_file():
        if len(sys.argv) < 2:
            print("Usage: python3 Part1.py <input_file>")
            sys.exit(1)
        input_file = sys.argv[1]
        if not input_file.endswith(".txt"):
            print("Invalid file type")
            sys.exit(1)
        try:
            f = open(input_file, 'r')
            f.close()
        except:
            print("Invalid file path")
            sys.exit(1)
        return input_file

    def print_mode():
        print_mode = "VERBOSE"
        if len(sys.argv) == 3:
            print_mode = sys.argv[2].upper()
            if print_mode not in ['VERBOSE', 'BRIEF', 'NONE']:
                print("Invalid print mode")
                sys.exit(1)
        return print_mode
    
    input_file = input_file()
    print_mode = print_mode()
    algorithm, parameter, turn, board = injestTestFile(input_file)

    if algorithm == "UR":
        output = uniformRandom(parameter, turn, board, print_mode)
    elif algorithm == "DLMM":
        output = depthLimitedMinMax(parameter, turn, board, print_mode)
    elif algorithm == "PMCGS":
        output = pureMonteCarloGameSearch(parameter, turn, board, print_mode)
    elif algorithm == "UCT":
        output = upperConfidenceBound(parameter, turn, board, print_mode)
    else:
        print("Invalid algorithm")
        sys.exit(1)

    print(f"Final Move Selected: {output}")
    print()