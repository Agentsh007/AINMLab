import tkinter as tk
from tkinter import font
import heapq
import random
import time

# --- A* Solver Logic (Copied from solve_8_puzzle.py) ---

# The target configuration of the puzzle
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0)) # 0 represents the empty space

# Pre-calculate the goal position for each tile (number) for fast heuristic lookup
GOAL_POSITIONS = {
    tile: (r, c)
    for r, row in enumerate(GOAL_STATE)
    for c, tile in enumerate(row)
}

def calculate_manhattan_distance(state):
    """Calculates the total Manhattan distance heuristic."""
    distance = 0
    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0: 
                goal_r, goal_c = GOAL_POSITIONS[tile]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

def is_solvable(state_tuple):
    """Checks if the given 8-puzzle state is solvable."""
    flat_list = [tile for row in state_tuple for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions % 2 == 0

def get_neighbors(state_tuple):
    """Generates all valid successor states (neighbors)."""
    neighbors = []
    r, c = -1, -1
    for i in range(3):
        for j in range(3):
            if state_tuple[i][j] == 0:
                r, c = i, j
                break
        if r != -1:
            break
            
    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in possible_moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            state_list = [list(row) for row in state_tuple]
            state_list[r][c], state_list[nr][nc] = state_list[nr][nc], state_list[r][c]
            neighbors.append(tuple(tuple(row) for row in state_list))
            
    return neighbors

def reconstruct_path(came_from, current_state):
    """Traces the path from the goal state back to the start state."""
    path = []
    while current_state in came_from:
        path.append(current_state)
        current_state = came_from[current_state]
    path.append(current_state)
    return path[::-1]

def solve_puzzle(initial_state_list):
    """Solves the 8-puzzle problem using A* search."""
    initial_state = tuple(tuple(row) for row in initial_state_list)
    
    if not is_solvable(initial_state):
        return None, "This puzzle is not solvable."

    if initial_state == GOAL_STATE:
        return [initial_state], "Puzzle is already solved."

    initial_h = calculate_manhattan_distance(initial_state)
    open_set = [(initial_h, initial_h, initial_state)] # f, h, state
    came_from = {}
    g_score = {initial_state: 0}
    states_explored = 0

    while open_set:
        current_f, current_h, current_state = heapq.heappop(open_set)
        states_explored += 1

        if current_state == GOAL_STATE:
            path = reconstruct_path(came_from, current_state)
            return path, f"Solved in {len(path) - 1} moves! (Explored {states_explored} states)"

        for neighbor in get_neighbors(current_state):
            tentative_g_score = g_score[current_state] + 1
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current_state
                g_score[neighbor] = tentative_g_score
                h_score = calculate_manhattan_distance(neighbor)
                f_score = tentative_g_score + h_score
                heapq.heappush(open_set, (f_score, h_score, neighbor))

    return None, f"No solution found. (Explored {states_explored} states)"

# --- Tkinter GUI Application ---

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Solver (A*)")
        master.config(bg="#F3F4F6") # gray-100

        self.current_state = GOAL_STATE
        self.tiles = [[None for _ in range(3)] for _ in range(3)]
        
        # Define fonts and colors
        self.tile_font = font.Font(family="Inter", size=24, weight="bold")
        self.button_font = font.Font(family="Inter", size=12, weight="bold")
        self.colors = {
            "tile": "#3B82F6",    # blue-500
            "empty": "#9CA3AF",  # gray-400
            "text": "white",
            "bg": "#F3F4F6",     # gray-100
            "frame": "#4B5563"   # gray-700
        }

        # --- Main Puzzle Frame ---
        self.board_frame = tk.Frame(master, bg=self.colors["frame"], bd=5, relief=tk.RIDGE, borderwidth=5)
        self.board_frame.pack(pady=20, padx=20)
        
        for r in range(3):
            for c in range(3):
                tile_label = tk.Label(
                    self.board_frame,
                    font=self.tile_font,
                    width=4,
                    height=2,
                    fg=self.colors["text"],
                    relief=tk.RAISED,
                    borderwidth=2
                )
                tile_label.grid(row=r, column=c, padx=5, pady=5)
                self.tiles[r][c] = tile_label

        # --- Control Frame ---
        self.control_frame = tk.Frame(master, bg=self.colors["bg"])
        self.control_frame.pack(pady=10)

        self.shuffle_button = tk.Button(
            self.control_frame,
            text="Shuffle",
            font=self.button_font,
            bg="#10B981", # green-500
            fg="white",
            command=self.shuffle_puzzle,
            padx=10,
            pady=5
        )
        self.shuffle_button.pack(side=tk.LEFT, padx=10)

        self.solve_button = tk.Button(
            self.control_frame,
            text="Solve",
            font=self.button_font,
            bg="#2563EB", # blue-600
            fg="white",
            command=self.solve_and_animate,
            padx=10,
            pady=5
        )
        self.solve_button.pack(side=tk.LEFT, padx=10)

        # --- Status Label ---
        self.status_label = tk.Label(
            master,
            text="Click 'Shuffle' to begin!",
            font=("Inter", 12),
            bg=self.colors["bg"],
            fg="#4B5563" # gray-700
        )
        self.status_label.pack(pady=10)

        self.shuffle_puzzle() # Start with a shuffled board

    def update_board(self, state):
        """Updates the text and colors of the tiles on the GUI."""
        self.current_state = state
        for r in range(3):
            for c in range(3):
                tile_value = state[r][c]
                label = self.tiles[r][c]
                
                if tile_value == 0:
                    label.config(text="", bg=self.colors["empty"])
                else:
                    label.config(text=str(tile_value), bg=self.colors["tile"])
        
        # This forces Tkinter to redraw the window immediately
        self.master.update_idletasks()

    def shuffle_puzzle(self):
        """Generates a new, random, solvable puzzle."""
        self.status_label.config(text="Shuffling...")
        self.set_buttons_enabled(False)
        
        # Make 100 random moves from the solved state to shuffle
        state = GOAL_STATE
        for _ in range(100):
            neighbors = get_neighbors(state)
            state = random.choice(neighbors)
            
        # Our A* solver can handle any solvable puzzle, but just in case:
        if not is_solvable(state):
             # This case is rare but good to handle.
             # Easiest way to fix: swap two tiles.
             state_list = [list(row) for row in state]
             state_list[0][0], state_list[0][1] = state_list[0][1], state_list[0][0]
             state = tuple(tuple(row) for row in state_list)

        self.update_board(state)
        self.status_label.config(text="Shuffled! Ready to solve.")
        self.set_buttons_enabled(True)

    def set_buttons_enabled(self, is_enabled):
        """Disables or enables the Shuffle and Solve buttons."""
        state = tk.NORMAL if is_enabled else tk.DISABLED
        self.shuffle_button.config(state=state)
        self.solve_button.config(state=state)

    def solve_and_animate(self):
        """Solves the current puzzle and animates the solution path."""
        self.set_buttons_enabled(False)
        self.status_label.config(text="Solving...")
        self.master.update_idletasks() # Show "Solving..." message

        # Run the A* solver
        solution_path, message = solve_puzzle(self.current_state)
        
        self.status_label.config(text=message)
        
        if solution_path:
            # We have a solution, now animate it
            # We use master.after() to avoid freezing the GUI
            self._animate_step(solution_path, 0)
        else:
            # No solution found (or already solved)
            self.set_buttons_enabled(True)
            
    def _animate_step(self, path, index):
        """
        Recursive helper function to show one step of the animation.
        This is the standard way to animate in Tkinter.
        """
        if index < len(path):
            # Show the current state
            state = path[index]
            self.update_board(state)
            
            # Schedule the next step after 400ms
            self.master.after(400, lambda: self._animate_step(path, index + 1))
        else:
            # Animation is finished
            self.status_label.config(text=f"Solved in {len(path) - 1} moves!")
            self.set_buttons_enabled(True)


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()