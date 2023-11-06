import sys

def uniformRandom():
    pass

def depthLimitedMinMax():
    pass

def pureMonteCarloGameSearch():
    pass

def upperConfidenceBound():
    pass

def injestTestFile(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()
        algorithm = content[0].strip().upper()
        parameter = content[1].strip()
        turn = content[2].strip()
        board = [line.strip() for line in content[3:]]
    print(algorithm, parameter, turn, board)
    return algorithm, parameter, turn, board

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 Part1.py <input_file>")
        sys.exit(1)
    print_mode = "VERBOSE"
    if len(sys.argv) == 3:
        print_mode = sys.argv[2].upper()
        if print_mode not in ['VERBOSE', 'BRIEF', 'NONE']:
            print("Invalid print mode")
            sys.exit(1)
    input_file = sys.argv[1]
    algorithm, parameter, turn, board = injestTestFile(input_file)
    
    