import sys
import numpy as np

def uniformRandom(parameter, turn, board):
    '''
    This is a trivial algorithm used for basic testing and benchmarking. It selects a legal 
    move for the specified player using the uniform random strategy (i.e., each legal 
    move is selected with the same probability. The parameter value should always be 0 
    for this algorithm. 
    '''
    possible_moves = [i for i in range(len(board[0])) if board[0][i] == 'O']
    np.random.shuffle(possible_moves)
    return possible_moves[0]

def isTerminal(board):
    # Horozontal -
    for i in range(len(board)):
        for j in range(len(board[0])-3):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] != 'O':
                return True, board[i][j]
    # Vertical |
    for i in range(len(board)-3):
        for j in range(len(board[0])):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] != 'O':
                return True, board[i][j]
    # Diagonal /
    for i in range(len(board)-3):
        for j in range(len(board[0])-3):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != 'O':
                return True, board[i][j]
    # Diagonal \
    for i in range(len(board)-3):
        for j in range(3, len(board[0])):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] != 'O':
                return True, board[i][j]        

def heuristic(board,player):
    '''
     For each set, if a player is the only player who has pieces inside that set, 
     then that player will receive a point for each piece they have in that set. 
     This means pieces will be counted multiple times if they appear in multiple 
     sets which are only occupied by that player.
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

def playMove(board, player, move):
    for i in range(len(board)-1, -1, -1):
        if board[i][move] == 'O':
            board[i][move] = player
            return board

def depthLimitedMinMax(maxDepth, turn, board, ):
    '''
    This algorithm uses depth-first minmax search out to a specified  maximum depth to 
    select a move. You should test each node to see whether it is a terminal state (i.e., a 
    win for one player or a draw); if so return that value immediately. If you reach the 
    depth limit without reaching a terminal state, apply a heuristic evaluation function 
    to the game state and return that value. You may choose to implement any 
    reasonable heuristic; you will give a brief description in your report. The heuristic 
    should take in any valid (non-terminal) board state as input and return a predicted 
    value for that state between -1 and 1. For example, you may want to count the 
    number of lines of 2 or 3 pieces that can be extended for each player. If there are 
    ties, break them randomly. Make sure you keep track of which player (maximizing 
    or minimizing) is making the choice at each node. Output the value for each of the 
    immediate next moves from the root (with Null for illegal moves) and the final move 
    selected. Example in Instructions.pdf
    '''
    scores=[0]
    for col in range(len(board[0])):
        temp_board = playMove(board, turn, col)
        if temp_board: # check if it's a legal move
            if isTerminal(temp_board) == [True, turn]:
                return float('inf'), col
            if maxDepth == 1:
                scores.append(heuristic(temp_board, turn))
            else:
                score,index = depthLimitedMinMax(maxDepth-1, turn, temp_board)
                scores.append(score)
    if len(scores) == 0:
        return None
    if maxDepth % 2 == 0:
        return scores.index(max(scores))
    return scores.index(min(scores))

def pureMonteCarloGameSearch(parameter, turn, board):
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
    pass

def upperConfidenceBound(parameter, turn, board):
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
    pass

def injestTestFile(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()
        algorithm = content[0].strip().upper()
        parameter = int(content[1].strip())
        turn = content[2].strip()
        board = [line.strip() for line in content[3:]]
        board = [line.split() for line in board]
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
        output = uniformRandom(parameter, turn, board)
    elif algorithm == "DLMM":
        output = depthLimitedMinMax(parameter, turn, board)
    elif algorithm == "PMCGS":
        output = pureMonteCarloGameSearch(parameter, turn, board)
    elif algorithm == "UCT":
        output = upperConfidenceBound(parameter, turn, board)
    else:
        print("Invalid algorithm")
        sys.exit(1)

    print(f"Final Move Selected: {output}")