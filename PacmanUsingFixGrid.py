from collections import deque

# === Fixed Initial Grid (manually defined) ===
grid = [
    ['P', ' ', '#', ' ', ' ', ' ', '#', ' ', 'F', ' '],
    [' ', '#', ' ', '#', ' ', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', ' ', '#', ' ', '#', '#', ' ', '#', ' '],
    ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' '],
    [' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', 'F'],
    ['#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    [' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#', ' '],
    [' ', 'F', ' ', ' ', '#', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ']
]
 
width = len(grid[0])
height = len(grid)

# === Find Pac-Man and Food positions ===
food_positions = set()
for y in range(height):
    for x in range(width):
        if grid[y][x] == 'F':
            food_positions.add((x, y))
        elif grid[y][x] == 'P':
            pacman_position = (x, y)

# === Directions: Up, Right, Down, Left ===
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


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


# === Main Loop ===
print("Initial Grid:")
print_grid()

step = 0
while food_positions:
    path = bfs(pacman_position) # type: ignore
    if not path:
        print("No path to remaining food!")
        break

    for next_pos in path[1:]:
        grid[pacman_position[1]][pacman_position[0]] = ' ' # type: ignore
        pacman_position = next_pos

        if pacman_position in food_positions:
            food_positions.remove(pacman_position)

        grid[pacman_position[1]][pacman_position[0]] = 'P'

        print(f"Step: {step}")
        print_grid()
        step += 1

print("All food are finished!")
