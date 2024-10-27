import time


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]


def is_goal_reached(puzzle):
    return puzzle == goal


def move(puzzle, direction):
    for i, row in enumerate(puzzle):
        if 0 in row:
            j= row.index(0)
            break
    npuzz = [list(row) for row in puzzle] 
    
    if direction == 'Up' and i > 0:
        npuzz[i][j], npuzz[i-1][j] = npuzz[i-1][j], npuzz[i][j]
    elif direction == 'Down' and i < 2:
        npuzz[i][j], npuzz[i+1][j] = npuzz[i+1][j], npuzz[i][j]
    elif direction == 'Left' and j > 0:
        npuzz[i][j], npuzz[i][j-1] = npuzz[i][j-1], npuzz[i][j]
    elif direction == 'Right' and j < 2:
        npuzz[i][j], npuzz[i][j+1] = npuzz[i][j+1], npuzz[i][j]
    else:
        return None
    return npuzz


def neighbors(puzzle):
    neighbors = []
    for direction in ['Up', 'Down', 'Left', 'Right']:
        neighbor = move(puzzle, direction)
        if neighbor:
            neighbors.append((neighbor, direction))
    return neighbors


def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

def bfs(start_puzzle):
    return None
def dfs(start_puzzle, max_depth=float('inf')):
    return None
def iddfs(start_puzzle, max_depth=50):
    return None
# Manhattan Distance Heuristic
def manhattan(puzzle):
   
    return 0

# Euclidean Distance Heuristic
def euclideane(puzzle):
  
    return 0

# A* Search
def a_star(start_puzzle, heuristic):
    return None

# Example puzzle state
initial_state = [[1, 8, 2],
                 [0, 4, 3],
                 [7, 6, 5]]

