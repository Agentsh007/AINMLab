from collections import deque
import time

# --- Helper function to print the board ---
def print_board(board):
    print("-------")
    for row in board:
        print(row)
    print("-------")
# --- Merged Puzzle Solver Class (Refactored) ---
class PuzzleSolver:
    def __init__(self, start_board, start_x, start_y):
        self.start_board = start_board
        self.start_x = start_x
        self.start_y = start_y
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.row_moves = [-1, 1, 0, 0] # Up, Down
        self.col_moves = [0, 0, -1, 1] # Left, Right

    def _is_valid(self, x, y):
        """Checks if (x, y) is on the 3x3 board."""
        return 0 <= x < 3 and 0 <= y < 3

    def _is_goal(self, board):
        """Checks if the board is the goal state."""
        return board == self.goal_state

    def _search_loop(self, data_structure, pop_method, move_indices, algo_name):
        # Add the initial state: (board, x_pos, y_pos, depth)
        data_structure.append((self.start_board, self.start_x, self.start_y, 0))
        
        visited = set()
        visited.add(tuple(map(tuple, self.start_board))) 

        print(f'Initial State ({algo_name}):')
        print_board(self.start_board)
        print(f"\nStarting {algo_name} Search...\n")

        # --- 2. START THE SEARCH LOOP ---
        while data_structure:
            # Use the chosen pop method (popleft for BFS, pop for DFS)
            curr_board, curr_x, curr_y, curr_depth = pop_method()
            
            # --- 3. CHECK FOR GOAL ---
            if self._is_goal(curr_board):
                print(f"--- Goal Found! ({algo_name}) ---")
                print(f"Final board state:")
                print_board(curr_board) 
                print(f"Solved in {curr_depth} moves.")
                print(f"Total states explored: {len(visited)}")
                return # Solution found!

            # --- 4. EXPLORE NEIGHBORS ---
            for i in move_indices:
                new_x = curr_x + self.row_moves[i]
                new_y = curr_y + self.col_moves[i]

                if self._is_valid(new_x, new_y):
                    # Create a deep copy of the board
                    new_board = [row[:] for row in curr_board]
                    
                    # Swap tiles
                    new_board[curr_x][curr_y], new_board[new_x][new_y] = \
                        new_board[new_x][new_y], new_board[curr_x][curr_y]

                    new_board_tuple = tuple(map(tuple, new_board))

                    if new_board_tuple not in visited:
                        visited.add(new_board_tuple)
                        data_structure.append((new_board, new_x, new_y, curr_depth + 1))

        # --- 5. NO SOLUTION ---
        print(f"No solution found ({algo_name}).")
        print(f"Total states explored: {len(visited)}")

    def solve(self, algorithm='bfs'):
        if algorithm.lower() == 'bfs':
            # 1. Data structure is a deque
            data_structure = deque()
            # 2. Pop method is popleft()
            pop_method = data_structure.popleft
            # 3. Move order is standard (0, 1, 2, 3)
            move_indices = range(4)
            algo_name = "BFS"
            
        elif algorithm.lower() == 'dfs':
            # 1. Data structure is a list (as a stack)
            data_structure = [] 
            # 2. Pop method is pop()
            pop_method = data_structure.pop
            # 3. Move order is reversed (3, 2, 1, 0)
            move_indices = range(3, -1, -1)
            algo_name = "DFS"
            
        else:
            print(f"Unknown algorithm: {algorithm}. Defaulting to BFS.")
            # Default to BFS parameters
            data_structure = deque()
            pop_method = data_structure.popleft
            move_indices = range(4)
            algo_name = "BFS"
        
        # Call the common loop with the chosen parameters
        self._search_loop(data_structure, pop_method, move_indices, algo_name)

# --- Driver Code (for the notebook) ---
start = [[1, 2, 3],
         [4, 0, 5],
         [6, 7, 8]]  # Initial state
x, y = 1, 1
# --- Run BFS ---
print("======= RUNNING BFS =======")
solver = PuzzleSolver(start, x, y)
solver.solve(algorithm='bfs') 
print("\n" + "="*30 + "\n")
# --- Run DFS ---
print("======= RUNNING DFS =======")
solver2 = PuzzleSolver(start, x, y)
solver2.solve(algorithm='dfs')