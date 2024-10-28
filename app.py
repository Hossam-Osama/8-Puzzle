


import heapq
import math
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

def tuplee(puzzle):
    return tuple(tuple(row) for row in puzzle)


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


def manhattan(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            path = puzzle[i][j]
            if path != 0:
                goalx, goaly = path // 3, path % 3
                distance += abs(i - goalx) + abs(j - goaly)
    return distance

def euclideane(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            path = puzzle[i][j]
            if path != 0:
                goalx, goaly = path // 3, path % 3
                distance += math.sqrt((i - goalx)**2 + (j - goaly)**2)
    return distance

# A* Search

def A_star(start_puzzle, heuristic):
    start_time = time.time()
    frontier = []
    heapq.heappush(frontier, (0, start_puzzle, []))  # (cost, puzzle state, path)
    explored = set()
    nodes_expanded = 0
    max_depth_reached = 0  

    while frontier:
        cost, puzzle, path = heapq.heappop(frontier)  # Pop the smallest cost node
        nodes_expanded += 1  
        current_depth = len(path)
        max_depth_reached = max(max_depth_reached, current_depth)  

        if is_goal_reached(puzzle):
            path_cost = len(path)
            return path, path_cost, nodes_expanded, max_depth_reached, time.time() - start_time
        
        explored.add(tuplee(puzzle))
        for neighbor, move_direction in neighbors(puzzle):
            if tuplee(neighbor) not in explored:
                new_path = path + [move_direction]
                new_cost = len(new_path) + heuristic(neighbor)  # Cost calculation
                heapq.heappush(frontier, (new_cost, neighbor, new_path))
                explored.add(tuplee(neighbor))

    return None

# Example puzzle state
initial_state = [[1, 4, 2],
                 [6, 5, 8],
                 [7, 3, 0]]

# Running A* with Manhattan heuristic
print("A* with Manhattan Distance:")
path, path_cost, nodes_expanded, search_depth, runtime = A_star(initial_state, manhattan)
print(f"Path: {path}\nCost of Path: {path_cost}\nNodes Expanded: {nodes_expanded}\nSearch Depth: {search_depth}\nRuntime: {runtime:.4f} seconds\n")

# Running A* with Euclidean heuristic
print("A* with Euclidean Distance:")
path, path_cost, nodes_expanded, search_depth, runtime = A_star(initial_state, euclideane)
print(f"Path: {path}\nCost of Path: {path_cost}\nNodes Expanded: {nodes_expanded}\nSearch Depth: {search_depth}\nRuntime: {runtime:.4f} seconds\n")
