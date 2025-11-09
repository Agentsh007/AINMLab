from collections import deque
import time

# --- Helper function to print the board ---
def print_board(board):
    print("-------")
    for row in board:
        print(row)
    print("-------")

# --- Puzzle Solver Class ---
class PuzzleSolverBFS:
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

    def solve(self):
        """Runs the BFS algorithm."""
        
        # 1. --- SETUP ---
        q = deque()
        q.append((self.start_board, self.start_x, self.start_y, 0))

        visited = set()
        visited.add(tuple(map(tuple, self.start_board))) 

        print('Initial State:')
        print_board(self.start_board)
        print("\nStarting BFS Search...\n")

        # --- 2. START THE BFS LOOP ---
        while q:
            curr_board, curr_x, curr_y, curr_depth = q.popleft()
            
            # --- ADDED PRINT STATEMENTS ---
            # This will print every board state as it is checked
            print(f"Checking Depth: {curr_depth}")
            print_board(curr_board)
            # time.sleep(0.1) # Optional: Uncomment to watch it solve slowly
            # --- END OF ADDED PRINT STATEMENTS ---

            # --- 3. CHECK FOR GOAL ---
            if self._is_goal(curr_board):
                print(f"--- Goal Found! ---")
                print(f"Final board state:")
                print_board(curr_board) # Print the final goal board
                print(f"Solved in {curr_depth} moves.")
                print(f"Total states explored: {len(visited)}")
                return 

            # --- 4. EXPLORE NEIGHBORS ---
            for i in range(4):
                new_x = curr_x + self.row_moves[i]
                new_y = curr_y + self.col_moves[i]

                if self._is_valid(new_x, new_y):
                    new_board = [row[:] for row in curr_board]
                    
                    # Swap tiles
                    new_board[curr_x][curr_y], new_board[new_x][new_y] = \
                        new_board[new_x][new_y], new_board[curr_x][curr_y]

                    new_board_tuple = tuple(map(tuple, new_board))

                    if new_board_tuple not in visited:
                        visited.add(new_board_tuple)
                        q.append((new_board, new_x, new_y, curr_depth + 1))

        # --- 5. NO SOLUTION ---
        print("No solution found.")
        print(f"Total states explored: {len(visited)}")

# --- Driver Code (for the notebook) ---
# We can just call the code directly
start = [[1, 2, 3],
         [4, 0, 5],
         [6, 7, 8]]  # Initial state
x, y = 1, 1

solver = PuzzleSolverBFS(start, x, y)
solver.solve()