# Import necessary libraries
from collections import deque

# Define the dimensions of the puzzle
N = 3

down = '↓'
up = '↑'
right = '→'
left = '←'

# Class to represent the state of the puzzle
class PuzzleState:
    def __init__(self, board, x, y, depth, last_move=None):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth
        self.last_move = last_move  # store arrow for the blank tile

# Possible moves: Left, Right, Up, Down
row = [0, 0, -1, 1]
col = [-1, 1, 0, 0]
move_symbols = [right, left, down, up]  # match index order to row/col

# Function to check if the current state is the goal state
def is_goal_state(board):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return board == goal

# Function to check if a move is valid
def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

# Function to print the puzzle board, replacing the 0 at (blank_x,blank_y) with symbol
def print_board(board, blank_x=None, blank_y=None, symbol=None):
    for i, r in enumerate(board):
        row_str = []
        for j, v in enumerate(r):
            if v == 0 and i == blank_x and j == blank_y:
                row_str.append(symbol if symbol is not None else ' ')
            elif v == 0:
                # This case should not be reached if blank_x/y are correct
                row_str.append(' ') 
            else:
                row_str.append(str(v))
        print(' '.join(row_str))
    print('--------')

# BFS function to solve the 8-puzzle problem
def solve_puzzle_bfs(start, x, y):
    q = deque()
    visited = set()

    # Enqueue initial state (no arrow for initial placement)
    q.append(PuzzleState(start, x, y, 0, None))
    visited.add(tuple(map(tuple, start)))

    while q:
        curr = q.popleft()

        # Print the current board state (show arrow instead of 0)
        print(f'Depth: {curr.depth}')
        print_board(curr.board, curr.x, curr.y, curr.last_move)

        # Check if goal state is reached
        if is_goal_state(curr.board):
            print(f'Goal state reached at depth {curr.depth}')
            return

        # Explore all possible moves
        for i in range(4):
            new_x = curr.x + row[i]
            new_y = curr.y + col[i]

            if is_valid(new_x, new_y):
                new_board = [r[:] for r in curr.board]
                new_board[curr.x][curr.y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr.x][curr.y]

                # If this state has not been visited before, push to queue
                if tuple(map(tuple, new_board)) not in visited:
                    visited.add(tuple(map(tuple, new_board)))
                    q.append(PuzzleState(new_board, new_x, new_y, curr.depth + 1, move_symbols[i]))

    print('No solution found (BFS Brute Force reached depth limit)')

# Driver Code
if __name__ == '__main__':
    start = [[1, 2, 3],
             [4, 0, 5],
             [6, 7, 8]]  # Initial state
    x, y = 1, 1

    print('Initial State:')
    print_board(start, x, y, None)  # initial blank shown as space
    solve_puzzle_bfs(start, x, y)