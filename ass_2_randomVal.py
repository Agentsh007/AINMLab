from collections import deque
import random

# Grid parameters
width = 10
height = 10
num_food = 5
wall_percentage = 0.20

# Initialize grid
grid = [[' ' for _ in range(width)] for _ in range(height)]

# Random walls
num_walls = int(height * width * wall_percentage)
wall_positions = set()
while len(wall_positions) < num_walls:
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    if (x, y) != (0, 0):
        wall_positions.add((x, y))
for x, y in wall_positions:
    grid[y][x] = '#'

# Random food
food_positions = set()
while len(food_positions) < num_food:
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    if (x, y) != (0, 0) and (x, y) not in wall_positions:
        food_positions.add((x, y))

for x, y in food_positions:
    grid[y][x] = 'F'

# Pacman start
pacman_position = (0, 0)
grid[pacman_position[1]][pacman_position[0]] = 'P'

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left


def print_grid():
    for row in grid:
        print(' '.join(row))
    print()


def bfs(start):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Found food
        if (x, y) in food_positions:
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != '#':
                queue.append(((nx, ny), path + [(x, y)]))

    return None


# --- Game loop ---
print("Initial Grid:")
print_grid()

step = 0
while food_positions:
    path = bfs(pacman_position)
    if not path:
        print("No path to remaining food!")
        break

    # Move step by step toward food
    for next_pos in path[1:]:
        # Clear previous
        grid[pacman_position[1]][pacman_position[0]] = ' '
        pacman_position = next_pos

        # Eat food if found
        if pacman_position in food_positions:
            food_positions.remove(pacman_position)

        grid[pacman_position[1]][pacman_position[0]] = 'P'

        print(f"Step: {step}")
        print_grid()
        step += 1

print("All food are finished!")
