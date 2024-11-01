

import heapq
import math
import time
from queue import Queue
import time

goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]


def is_goal_reached(puzzle):
    return puzzle == goal


def move(puzzle, direction):
    for i, row in enumerate(puzzle):
        if 0 in row:
            j = row.index(0)
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
    start_time = time.time()
    frontair = Queue()
    explored = set()
    frontair.put((start_puzzle, []))
    nodes_expanded = 0

    frontair_states = set()
    frontair_states.add(tuple(map(tuple, start_puzzle)))

    while not frontair.empty():
        puzzle, path = frontair.get()
        nodes_expanded += 1

        if is_goal_reached(puzzle):
            return path, nodes_expanded, len(path), time.time() - start_time

        explored.add(tuple(map(tuple, puzzle)))

        for neighbor, direction in neighbors(puzzle):
            neighbor_tuple = tuple(map(tuple, neighbor))

            if neighbor_tuple not in explored and neighbor_tuple not in frontair_states:
                frontair.put((neighbor, path + [direction]))
                frontair_states.add(neighbor_tuple)

    return None, nodes_expanded, len(path)


def dfs(start_puzzle, max_depth=float('inf')):
    start_time = time.time()
    frontair = [(start_puzzle, [])]
    explored = set()
    nodes_expanded = 0  
    max_depth_reached = 0  

    while frontair:
        puzzle, path = frontair.pop()
        n = 0
        n += 1
        nodes_expanded += 1  
        current_depth = len(path)
        new_cost = len(path) - n 
        cost = new_cost
        if is_goal_reached(puzzle):
            cost = cost + 1
            return path, cost, nodes_expanded, max_depth_reached, time.time() - start_time

        explored.add(tuple(map(tuple, puzzle)))

        if current_depth < max_depth:
            for neighbor, direction in neighbors(puzzle):
                if (tuple(map(tuple, neighbor)) not in explored and
                        all(tuple(map(tuple, neighbor)) != tuple(map(tuple, p[0])) for p in frontair)):
                    neighbor_depth = len(path)
                    max_depth_reached = max(max_depth_reached,  neighbor_depth +1)  
                    frontair.append((neighbor, path + [direction]))
                   
    return None, nodes_expanded, max_depth_reached, time.time() - start_time


def ddfs(start_puzzle, max_depth, explored_depth):
    frontair = [(start_puzzle, [])]
    nodes_expanded = 0  
    max_depth_reached = 0  

    while frontair:
        puzzle, path = frontair.pop()
        nodes_expanded += 1
        current_depth = len(path)
        max_depth_reached = max(max_depth_reached, current_depth)  

        if is_goal_reached(puzzle):
            return path, nodes_expanded, current_depth, max_depth_reached  

        puzzle_tuple = tuple(map(tuple, puzzle))
        if puzzle_tuple not in explored_depth or current_depth < explored_depth[puzzle_tuple]:
            explored_depth[puzzle_tuple] = current_depth
            if current_depth < max_depth:
                for neighbor, direction in neighbors(puzzle):
                    neighbor_tuple = tuple(map(tuple, neighbor))
                    neighbor_depth = current_depth + 1
                    if neighbor_tuple not in explored_depth or neighbor_depth < explored_depth[neighbor_tuple]:
                        frontair.append((neighbor, path + [direction]))

    return None, nodes_expanded, 0, max_depth_reached  


def iddfs(start_puzzle, max_depth):
    start_puzzle = tuple(map(tuple, start_puzzle))
    nodes_expanded = 0 
    for depth in range(max_depth):
        explored_depth = {}  
        path, expanded, search_depth, max_depth_reached = ddfs(start_puzzle, max_depth=depth, explored_depth=explored_depth)
        nodes_expanded += expanded
        if path is not None:
            return path, nodes_expanded, search_depth, max_depth_reached  
    return None, nodes_expanded, 0, max_depth  


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
    heapq.heappush(frontier, (0, start_puzzle, []))  
    explored = set()
    nodes_expanded = 0
    max_depth_reached = 0  

    while frontier:
        cost, puzzle, path = heapq.heappop(frontier) 
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
                new_cost = len(new_path) + heuristic(neighbor) 
                heapq.heappush(frontier, (new_cost, neighbor, new_path))
                explored.add(tuplee(neighbor))

    return None
# controller with Gui
def solve_puzzle(start_puzzle, algorithm, limit=0):
    if not is_solvable(start_puzzle):
        return "There is no possible solution."
    
    start_time = time.time()  
    path = None
    nodes_expanded = 0
    search_depth = 0
    cost = 0
    max_depth_reached = 0

    if algorithm == 'BFS':
        path, nodes_expanded, search_depth, running_time = bfs(start_puzzle)
        cost = len(path) if path is not None else 0  
        max_depth_reached = search_depth  
    elif algorithm == 'DFS':
        path, cost, nodes_expanded, max_depth_reached, running_time = dfs(start_puzzle, max_depth=limit)
        search_depth = max_depth_reached  
    elif algorithm == 'IDDFS':
        path, nodes_expanded, search_depth, max_depth_reached = iddfs(start_puzzle, max_depth=limit)
        cost = len(path) if path is not None else 0 
    else:
        raise ValueError("Unsupported algorithm")

    # Calculate total running time
    running_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    return {
        # 'path': path,
        'path_length':len(path),
        'nodes_expanded': nodes_expanded,
        'search_depth': search_depth,
        'cost_of_path': cost,
        'max_depth_reached': max_depth_reached,
        'running_time': running_time
    }



def count_inversions(puzzle):
    # Flatten the puzzle and exclude 0
    flat_puzzle = [tile for row in puzzle for tile in row if tile != 0]
    inversions = 0

    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1
    return inversions


def is_solvable(puzzle):
    inversions = count_inversions(puzzle)
    return inversions % 2 == 0  # Solvable if the number of inversions is even


# Example puzzle state
initial_state = [[8, 1, 2],
                 [0, 4, 3],
                 [7, 6, 5]]
from pprint import pprint

# # tests
test_cases = [
    {
        "initial_state": [[1,2,3], [4,5,6], [0,7,8]],
        "description": "Reverse order",
        "goal": [[1, 0, 3], [4, 5, 6], [7, 8,2]]
    }
]

# Run each test case for BFS, DFS, and IDDFS
for i, case in enumerate(test_cases, 1):
    print(f"Test Case {i}: {case['description']}")
    initial_state = case["initial_state"]
    goal = case["goal"]

    # Solving using BFS
    bfs_result = solve_puzzle(initial_state, 'BFS')
    print("BFS Result:")
    pprint(bfs_result)

    # Solving using DFS with a reasonable depth limit (for demonstration, set to 200)
    dfs_result = solve_puzzle(initial_state, 'DFS', limit=500)
    print("DFS Result:")
    pprint(dfs_result)

    # Solving using IDDFS with a depth limit
    iddfs_result = solve_puzzle(initial_state, 'IDDFS', limit=50)
    print("IDDFS Result:")
    pprint(iddfs_result)

    print("\n" + "="*40 + "\n")
# # Solving using BFS
# bfs_result = solve_puzzle(initial_state, 'BFS')
# print("BFS Result:", bfs_result)

# # Solving using DFS
# dfs_result = solve_puzzle(initial_state, 'DFS', 200)
# print("DFS Result:", dfs_result)

# # Solving using IDDFS with default = 30
# iddfs_result = solve_puzzle(initial_state, 'IDDFS', 200)
# print("IDDFS Result:", iddfs_result)
# # Running A* with Manhattan heuristic
# print("A* with Manhattan Distance:")
# path, path_cost, nodes_expanded, search_depth, runtime = A_star(
#     initial_state, manhattan)
# print(f"Path: {path}\nCost of Path: {path_cost}\nNodes Expanded: {nodes_expanded}\nSearch Depth: {search_depth}\nRuntime: {runtime:.4f} seconds\n")

# Running A* with Euclidean heuristic
# print("A* with Euclidean Distance:")
# path, path_cost, nodes_expanded, search_depth, runtime = A_star(
#     initial_state, euclideane)
# print(f"Path: {path}\nCost of Path: {path_cost}\nNodes Expanded: {nodes_expanded}\nSearch Depth: {search_depth}\nRuntime: {runtime:.4f} seconds\n")
