import sys

def uniformRandom(parameter, turn, board):
    pass

def depthLimitedMinMax(parameter, turn, board):
    pass

def pureMonteCarloGameSearch(parameter, turn, board):
    pass

def upperConfidenceBound(parameter, turn, board):
    pass

def injestTestFile(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()
        algorithm = content[0].strip().upper()
        parameter = content[1].strip()
        turn = content[2].strip()
        board = [line.strip() for line in content[3:]]
    return algorithm, parameter, turn, board

if __name__ == "__main__":

    #input file
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

    #print mode
    print_mode = "VERBOSE"
    if len(sys.argv) == 3:
        print_mode = sys.argv[2].upper()
        if print_mode not in ['VERBOSE', 'BRIEF', 'NONE']:
            print("Invalid print mode")
            sys.exit(1)
    

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
    
    