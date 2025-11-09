import heapq
import time

# --- Heuristic Functions ---

def h_misplaced_tiles(state, goal_state, goal_positions=None):
    """Heuristic: Counts misplaced tiles."""
    return sum(1 for r in range(3) for c in range(3) 
               if state[r][c] != goal_state[r][c] and state[r][c] != 0)

def h_manhattan_distance(state, goal_state, goal_positions):
    """Heuristic: Calculates the sum of Manhattan distances."""
    return sum(abs(r - goal_positions[tile][0]) + abs(c - goal_positions[tile][1])
               for r in range(3) for c in range(3) if (tile := state[r][c]) != 0)

# --- Node Class for A* ---

class PuzzleNode:
    """Represents a state in the puzzle search (state, parent, move, g, h, f)."""
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = self.g + self.h
    
    def __lt__(self, other):
        """Used by the priority queue (heapq) to sort by f-cost."""
        return self.f < other.f
    
    def __eq__(self, other):
        """Checks if two nodes represent the same state."""
        return self.state == other.state

    def __hash__(self):
        """Allows nodes to be added to a set (closed list)."""
        return hash(self.state)

# --- Helper Functions ---

def get_neighbors(node):
    """Generates all valid neighboring states from the current node's state."""
    neighbors = []
    # Find the blank space (0)
    blank_r, blank_c = -1, -1
    for r in range(3):
        for c in range(3):
            if node.state[r][c] == 0:
                blank_r, blank_c = r, c
                break
        if blank_r != -1: 
            break
            
    possible_moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
    
    for dr, dc, move_name in possible_moves:
        new_r, new_c = blank_r + dr, blank_c + dc
        
        # Check if the new position is within the grid (0-2)
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_state_list = [list(row) for row in node.state]
            # Swap the blank tile with the adjacent tile
            new_state_list[blank_r][blank_c], new_state_list[new_r][new_c] = \
                new_state_list[new_r][new_c], new_state_list[blank_r][blank_c]
            # Convert back to immutable tuple-of-tuples
            neighbors.append((tuple(tuple(row) for row in new_state_list), move_name))
            
    return neighbors

def reconstruct_path(end_node):
    """Traces the path from the end_node back to the start."""
    path = []
    current = end_node
    while current.parent is not None:
        path.append((current.move, current.state))
        current = current.parent
    path.append(("START", current.state))
    return path[::-1] # Reverse from goal->start to start->goal

def print_board(state):
    """Prints the 3x3 puzzle board in a nice format."""
    for row in state:
        print(" --- --- ---")
        print(f"| {row[0]} | {row[1]} | {row[2]} |".replace('0', ' '))
    print(" --- --- ---")

def is_solvable(state, goal_state):
    """Checks if the 8-puzzle is solvable using inversion count."""
    flat_state = [tile for row in state for tile in row if tile != 0]
    # Count inversions
    inversions = sum(1 for i in range(len(flat_state)) 
                     for j in range(i + 1, len(flat_state)) 
                     if flat_state[i] > flat_state[j])
    # Solvable if inversions are even (assuming goal state has 0 inversions)
    return inversions % 2 == 0

# --- A* Solver ---

def solve(initial_state_list, goal_state_list, heuristic_func):
    """
    Solves the 8-puzzle problem using A* search.
    Returns: (path, time_taken, nodes_expanded) or (None, time_taken, nodes_expanded)
    """
    initial_state = tuple(tuple(row) for row in initial_state_list)
    goal_state = tuple(tuple(row) for row in goal_state_list)
    
    # Pre-calculate goal positions for Manhattan distance
    goal_positions = {}
    for r in range(3):
        for c in range(3):
            goal_positions[goal_state[r][c]] = (r, c)
            
    if not is_solvable(initial_state, goal_state):
        print(f"This puzzle is NOT solvable (checked with {heuristic_func.__name__}).")
        return None, 0, 0
    
    start_node = PuzzleNode(
        state=initial_state,
        h=heuristic_func(initial_state, goal_state, goal_positions)
    )
    
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set() # Stores *states* we've already processed
    g_costs = {initial_state: 0} # Stores g-cost for states in open_list
    
    start_time = time.time()
    nodes_expanded = 0
    
    while open_list:
        current_node = heapq.heappop(open_list)
        nodes_expanded += 1

        if current_node.state == goal_state:
            end_time = time.time()
            path = reconstruct_path(current_node)
            return path, (end_time - start_time), nodes_expanded
        
        closed_set.add(current_node.state)
        
        for new_state, move in get_neighbors(current_node):
            if new_state in closed_set:
                continue
                
            new_g = current_node.g + 1
            
            if new_state not in g_costs or new_g < g_costs[new_state]:
                g_costs[new_state] = new_g
                new_h = heuristic_func(new_state, goal_state, goal_positions)
                new_node = PuzzleNode(new_state, current_node, move, new_g, new_h)
                heapq.heappush(open_list, new_node)

    return None, (time.time() - start_time), nodes_expanded # No solution found

# --- Main Execution ---

if __name__ == "__main__":
    
    # "Medium" puzzle (solvable)
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    # "Harder" puzzle (solvable)
    # initial_state = [
    #     [8, 6, 7],
    #     [2, 5, 4],
    #     [3, 0, 1]
    # ]
    
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("--- Solving with Manhattan Distance ---")
    solution_path, time_taken, nodes = solve(initial_state, goal_state, h_manhattan_distance)
    
    if solution_path:
        print(f"\n--- Solution Found! ---")
        print(f"Time taken: {time_taken:.4f} seconds")
        print(f"Nodes expanded: {nodes}")
        print(f"Moves: {len(solution_path) - 1}")
        # for i, (move, state) in enumerate(solution_path):
        #     print(f"\nMove {i}: {move}")
        #     print_board(state)
    else:
        print(f"--- No Solution Found ---")
        print(f"Time taken: {time_taken:.4f} seconds")
        print(f"Nodes expanded: {nodes}")
            
    print("\n" + "="*30 + "\n")
    
    print("--- Solving with Misplaced Tiles ---")
    solution_path_m, time_taken_m, nodes_m = solve(initial_state, goal_state, h_misplaced_tiles)

    if solution_path_m:
        print(f"\n--- Solution Found! ---")
        print(f"Time taken: {time_taken_m:.4f} seconds")
        print(f"Nodes expanded: {nodes_m}")
        print(f"Moves: {len(solution_path_m) - 1}")
    else:
        print(f"--- No Solution Found ---")
        print(f"Time taken: {time_taken_m:.4f} seconds")
        print(f"Nodes expanded: {nodes_m}")