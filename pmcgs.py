from copy import deepcopy
import random
import sys
import time

def possibleMoves(board):
    possible_moves = [i for i in range(len(board[0])) if board[0][i] == 'O']
    return possible_moves

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

def flipPlayer(player):
    return 'R' if player == 'Y' else 'Y'

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

class Node:
    def __init__(self, move, parent, player = ''):
        self.parent = parent
        self.move = move
        self.Ni = 0
        self.Wi = 0
        self.children = []
        self.player = player
    
    def is_leaf(self):
        return len(self.children) == 0


class MCTS:
    def __init__(self,board, player, print_mode):
        root_player = 'Y' if player == 'R' else 'Y'
        self.root_board = deepcopy(board)
        self.root = Node(None, None, root_player)
        self.print_mode = print_mode   
    
    def print_values(self):
        if len(self.root.children) == 0:
            print("Board was given in solved state. Game was not played")
            return
        
        column_counter = 0
        for child in self.root.children:
            if child.move == column_counter and child.Ni != 0:
                print('Column:', child.move, ':', child.Wi/child.Ni)
            else:
                print('Column:', column_counter, ': NULL')
            column_counter += 1
    

    def pmcgs_select_node(self, node): 
        temp_board = deepcopy(self.root_board)

        # Randomly selects node to expand
        while not node.is_leaf():
            children = node.children
            node = random.choice(children)
            temp_board = playMove(temp_board, node.player, node.move, print_mode)
            
        return node, temp_board
    
    def pmcgs_best_move(self):
        if len(self.root.children) == 0: 
            return None
        max_value = float('-inf')
        max_move = None
        for child in self.root.children:
            if child.Wi/child.Ni > max_value:
                max_value = child.Wi/child.Ni
                max_move = child.move
        return max_move

    

    def expand(self,parent_node, board):
        #check here if game is over
        if isTerminal(board)[0]:
            return 

        child_player = 'R' if parent_node.player == 'Y' else 'Y'

        #Store all possible moves as children of selected node
        parent_node.children = [Node(move,parent_node, child_player) for move in possibleMoves(board)]


    def rollout(self,node,board):
        current_node_player = node.player

        while not isTerminal(board)[0]:
            random_move = random.choice(possibleMoves(board))
            board = playMove(board, current_node_player, random_move, self.print_mode)
            current_node_player = flipPlayer(current_node_player)
        
        return isTerminal(board)[1]

    def back_propogate(self, node, winner):
        reward = 0
        if winner == self.root.player:
            reward = -1
        elif winner != self.root.player and winner != 'O':
            reward = 1

        while node is not None:
            node.Ni += 1
            node.Wi += reward
            node = node.parent

            

def pureMonteCarloGameSearch(time_limit, player, board, print_mode="VERBOSE"):
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
    mcts = MCTS(board, player, print_mode)

    start_time = time.time()
    num_rollouts = 0

    while time.time() - start_time < time_limit:
        node, board = mcts.pmcgs_select_node(mcts.root)
        mcts.expand(node, board)
        winner = mcts.rollout(node, board)
        mcts.back_propogate(node, winner)
        num_rollouts += 1
    
    print('Number of rollouts:', num_rollouts)
    print('Seconds Elapsed:', time.time() - start_time)
    mcts.print_values()
    best_move = mcts.pmcgs_best_move()

    return best_move




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

    if algorithm == "PMCGS":
        output = pureMonteCarloGameSearch(parameter, turn, board, print_mode)
    else:
        print("Invalid algorithm")
        sys.exit(1)

    print(f"Final Move Selected: {output}")
    print()