import tkinter as tk
from tkinter import font
import heapq
import random
from typing import List, Optional, Tuple

# --- A* Solver Logic (Copied and extended) ---

GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the empty space

GOAL_POSITIONS = {
    tile: (r, c)
    for r, row in enumerate(GOAL_STATE)
    for c, tile in enumerate(row)
}


def calculate_manhattan_distance(state: Tuple[Tuple[int, ...], ...]) -> int:
    distance = 0
    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0:
                goal_r, goal_c = GOAL_POSITIONS[tile]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance


def is_solvable(state_tuple: Tuple[Tuple[int, ...], ...]) -> bool:
    flat_list = [tile for row in state_tuple for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions % 2 == 0


def get_neighbors(state_tuple: Tuple[Tuple[int, ...], ...]) -> List[Tuple[Tuple[int, ...], ...]]:
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
    path = []
    while current_state in came_from:
        path.append(current_state)
        current_state = came_from[current_state]
    path.append(current_state)
    return path[::-1]


def solve_puzzle(initial_state_list):
    """
    Solves the 8-puzzle with A*.
    Returns (path or None, message, states_explored:int).
    """
    initial_state = tuple(tuple(row) for row in initial_state_list)

    if not is_solvable(initial_state):
        return None, "This puzzle is not solvable.", 0

    if initial_state == GOAL_STATE:
        return [initial_state], "Puzzle is already solved.", 0

    initial_h = calculate_manhattan_distance(initial_state)
    open_set = [(initial_h, initial_h, initial_state)]  # f, h, state
    came_from = {}
    g_score = {initial_state: 0}
    states_explored = 0
    visited = set()

    while open_set:
        _, _, current_state = heapq.heappop(open_set)
        if current_state in visited:
            continue
        visited.add(current_state)
        states_explored += 1

        if current_state == GOAL_STATE:
            path = reconstruct_path(came_from, current_state)
            return path, f"Solved in {len(path) - 1} moves!", states_explored

        for neighbor in get_neighbors(current_state):
            tentative_g_score = g_score[current_state] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current_state
                g_score[neighbor] = tentative_g_score
                h_score = calculate_manhattan_distance(neighbor)
                f_score = tentative_g_score + h_score
                heapq.heappush(open_set, (f_score, h_score, neighbor))

    return None, "No solution found.", states_explored


# --- Tkinter GUI Application ---


class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Solver (A*)")
        master.config(bg="#F3F4F6")
        self.current_state = GOAL_STATE
        self.tiles: List[List[Optional[tk.Label]]] = [[None for _ in range(3)] for _ in range(3)]

        # fonts & colors
        self.tile_font = font.Font(family="Inter", size=24, weight="bold")
        self.button_font = font.Font(family="Inter", size=11, weight="bold")
        self.colors = {
            "tile": "#3B82F6",    # blue-500
            "empty": "#9CA3AF",   # gray-400
            "text": "white",
            "bg": "#F3F4F6",
            "frame": "#4B5563"
        }

        # board frame
        self.board_frame = tk.Frame(master, bg=self.colors["frame"], bd=5, relief=tk.RIDGE, borderwidth=5)
        self.board_frame.pack(pady=14, padx=14)

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
                tile_label.bind("<Button-1>", lambda _event, r=r, c=c: self.on_tile_click(r, c))
                self.tiles[r][c] = tile_label

        # control frame
        self.control_frame = tk.Frame(master, bg=self.colors["bg"])
        self.control_frame.pack(pady=8)

        self.shuffle_button = tk.Button(
            self.control_frame, text="Shuffle", font=self.button_font,
            bg="#10B981", fg="white", command=self.shuffle_puzzle, padx=8, pady=5
        )
        self.shuffle_button.grid(row=0, column=0, padx=6)

        self.solve_button = tk.Button(
            self.control_frame, text="Solve", font=self.button_font,
            bg="#2563EB", fg="white", command=self.solve_and_prepare, padx=8, pady=5
        )
        self.solve_button.grid(row=0, column=1, padx=6)

        self.prev_button = tk.Button(self.control_frame, text="Prev", font=self.button_font,
                                     command=self.step_prev, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=2, padx=6)

        self.play_button = tk.Button(self.control_frame, text="Play", font=self.button_font,
                                     command=self.toggle_play, state=tk.DISABLED)
        self.play_button.grid(row=0, column=3, padx=6)

        self.next_button = tk.Button(self.control_frame, text="Next", font=self.button_font,
                                     command=self.step_next, state=tk.DISABLED)
        self.next_button.grid(row=0, column=4, padx=6)

        self.undo_button = tk.Button(self.control_frame, text="Undo", font=self.button_font,
                                     command=self.undo_move, state=tk.DISABLED)
        self.undo_button.grid(row=0, column=5, padx=6)

        self.reset_button = tk.Button(self.control_frame, text="Reset", font=self.button_font,
                                      command=self.reset_to_goal)
        self.reset_button.grid(row=0, column=6, padx=6)

        # speed slider
        speed_frame = tk.Frame(master, bg=self.colors["bg"])
        speed_frame.pack()
        tk.Label(speed_frame, text="Speed (ms):", bg=self.colors["bg"]).pack(side=tk.LEFT, padx=(6, 2))
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL, length=200, bg=self.colors["bg"])
        self.speed_scale.set(400)
        self.speed_scale.pack(side=tk.LEFT)

        # status & move count
        self.status_label = tk.Label(
            master,
            text="Click a tile to move it or 'Shuffle'.",
            font=("Inter", 12),
            bg=self.colors["bg"],
            fg="#4B5563"
        )
        self.status_label.pack(pady=(8, 2))

        self.move_count = 0
        self.move_count_label = tk.Label(master, text=f"Moves: {self.move_count}", bg=self.colors["bg"])
        self.move_count_label.pack()

        # internal state for solution stepping
        self.solution_path = None
        self.solution_index = 0
        self.playing = False
        self.play_after_id = None

        # undo stack
        self.undo_stack: List[Tuple[Tuple[Tuple[int, ...], ...], int]] = []

        # keyboard bindings
        master.bind("<Up>", lambda e: self.move_by_direction(1, 0))
        master.bind("<Down>", lambda e: self.move_by_direction(-1, 0))
        master.bind("<Left>", lambda e: self.move_by_direction(0, 1))
        master.bind("<Right>", lambda e: self.move_by_direction(0, -1))

        self.update_board(self.current_state)

    # ----- Board / UI helpers -----
    def update_board(self, state, highlight: Optional[Tuple[int, int]] = None):
        self.current_state = state
        for r in range(3):
            for c in range(3):
                tile_value = state[r][c]
                label = self.tiles[r][c]
                if label is None:
                    continue
                if tile_value == 0:
                    label.config(text="", bg=self.colors["empty"])
                else:
                    label.config(text=str(tile_value), bg=self.colors["tile"])

        if highlight is not None:
            self.flash_tile(highlight[0], highlight[1])

    def flash_tile(self, r, c):
        label = self.tiles[r][c]
        if not label:
            return
        orig = label.cget("bg")
        label.config(bg="#F59E0B")  # amber for flash
        self.master.after(180, lambda: label.config(bg=orig))

    def find_empty_tile(self, state) -> Tuple[int, int]:
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c
        return -1, -1

    def set_buttons_enabled(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.shuffle_button.config(state=state)
        self.solve_button.config(state=state)
        self.reset_button.config(state=state)

    # ----- User interactions -----
    def on_tile_click(self, r, c):
        if self.solve_button["state"] == tk.DISABLED and not self.playing:
            return

        empty_r, empty_c = self.find_empty_tile(self.current_state)
        is_adjacent = (abs(r - empty_r) == 1 and c == empty_c) or (r == empty_r and abs(c - empty_c) == 1)
        if not is_adjacent:
            self.status_label.config(text="Tile not movable.")
            return

        # push to undo stack
        self.undo_stack.append((self.current_state, self.move_count))
        self.undo_button.config(state=tk.NORMAL)

        new_state_list = [list(row) for row in self.current_state]
        new_state_list[r][c], new_state_list[empty_r][empty_c] = new_state_list[empty_r][empty_c], new_state_list[r][c]
        new_state_tuple = tuple(tuple(row) for row in new_state_list)

        self.move_count += 1
        self.move_count_label.config(text=f"Moves: {self.move_count}")
        self.update_board(new_state_tuple, highlight=(r, c))

        if new_state_tuple == GOAL_STATE:
            self.status_label.config(text=f"Congratulations! Solved in {self.move_count} moves.")
        else:
            self.status_label.config(text="Tile moved.")

    def move_by_direction(self, dr, dc):
        # move a tile into the empty cell based on arrow key: the direction is where the empty moves
        empty_r, empty_c = self.find_empty_tile(self.current_state)
        src_r, src_c = empty_r + dr, empty_c + dc
        if 0 <= src_r < 3 and 0 <= src_c < 3:
            self.on_tile_click(src_r, src_c)

    def undo_move(self):
        if not self.undo_stack:
            return
        state, prev_count = self.undo_stack.pop()
        self.move_count = prev_count
        self.move_count_label.config(text=f"Moves: {self.move_count}")
        self.update_board(state)
        if not self.undo_stack:
            self.undo_button.config(state=tk.DISABLED)
        self.status_label.config(text="Undo performed.")

    def reset_to_goal(self):
        self.undo_stack.clear()
        self.move_count = 0
        self.move_count_label.config(text=f"Moves: {self.move_count}")
        self.update_board(GOAL_STATE)
        self.status_label.config(text="Reset to solved state.")
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.solution_path = None

    def shuffle_puzzle(self):
        self.status_label.config(text="Shuffling...")
        self.set_buttons_enabled(False)
        self.solution_path = None
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.master.update_idletasks()

        state = GOAL_STATE
        for _ in range(120):
            neighbors = get_neighbors(state)
            state = random.choice(neighbors)

        if not is_solvable(state):
            state_list = [list(row) for row in state]
            state_list[0][0], state_list[0][1] = state_list[0][1], state_list[0][0]
            state = tuple(tuple(row) for row in state_list)

        self.undo_stack.clear()
        self.move_count = 0
        self.move_count_label.config(text=f"Moves: {self.move_count}")
        self.update_board(state)
        self.status_label.config(text="Shuffled! Use clicks, arrows, or Solve.")
        self.set_buttons_enabled(True)
        self.undo_button.config(state=tk.DISABLED)

    # ----- Solver controls & animation/stepping -----
    def solve_and_prepare(self):
        self.set_buttons_enabled(False)
        self.status_label.config(text="Solving...")
        self.master.update_idletasks()

        path, message, explored = solve_puzzle(self.current_state)
        self.status_label.config(text=f"{message} (Explored {explored} states)")
        self.set_buttons_enabled(True)

        if path:
            self.solution_path = path
            self.solution_index = 0
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.play_button.config(state=tk.NORMAL)
            # show initial state (should be current), but ensure move count is correct
            self.move_count = 0
            self.move_count_label.config(text=f"Moves: {self.move_count}")
        else:
            self.solution_path = None
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.play_button.config(state=tk.DISABLED)

    def step_next(self):
        if not self.solution_path:
            return
        if self.solution_index < len(self.solution_path) - 1:
            self.solution_index += 1
            prev = self.solution_path[self.solution_index - 1]
            cur = self.solution_path[self.solution_index]
            moved = self._find_moved_tile(prev, cur)
            self.move_count = self.solution_index
            self.move_count_label.config(text=f"Moves: {self.move_count}")
            self.update_board(cur, highlight=moved)
            self.status_label.config(text=f"Step {self.solution_index}/{len(self.solution_path)-1}")
        else:
            self.status_label.config(text="Reached end of solution.")

    def step_prev(self):
        if not self.solution_path:
            return
        if self.solution_index > 0:
            self.solution_index -= 1
            cur = self.solution_path[self.solution_index]
            self.move_count = self.solution_index
            self.move_count_label.config(text=f"Moves: {self.move_count}")
            self.update_board(cur)
            self.status_label.config(text=f"Step {self.solution_index}/{len(self.solution_path)-1}")
        else:
            self.status_label.config(text="At start of solution.")

    def toggle_play(self):
        if not self.solution_path:
            return
        if self.playing:
            self.stop_play()
        else:
            self.start_play()

    def start_play(self):
        self.playing = True
        self.play_button.config(text="Pause")
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self._play_step()

    def stop_play(self):
        self.playing = False
        self.play_button.config(text="Play")
        if self.play_after_id:
            self.master.after_cancel(self.play_after_id)
            self.play_after_id = None
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)

    def _play_step(self):
        if not self.solution_path:
            self.stop_play()
            return
        if self.solution_index < len(self.solution_path) - 1:
            self.solution_index += 1
            prev = self.solution_path[self.solution_index - 1]
            cur = self.solution_path[self.solution_index]
            moved = self._find_moved_tile(prev, cur)
            self.move_count = self.solution_index
            self.move_count_label.config(text=f"Moves: {self.move_count}")
            self.update_board(cur, highlight=moved)
            self.status_label.config(text=f"Playing: {self.solution_index}/{len(self.solution_path)-1}")
            delay = max(50, int(self.speed_scale.get()))
            self.play_after_id = self.master.after(delay, self._play_step)
        else:
            self.status_label.config(text="Animation finished.")
            self.stop_play()

    def _find_moved_tile(self, prev_state, cur_state):
        # returns (r,c) of tile that moved into the empty in the new state (for highlight)
        for r in range(3):
            for c in range(3):
                if prev_state[r][c] != cur_state[r][c] and cur_state[r][c] != 0:
                    return (r, c)
        return None


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()