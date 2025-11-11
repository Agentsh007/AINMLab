

from collections import deque
import random


height = 10
width = 10

num_of_foods = 20
walls_percent = .2

num_of_walls = height* width* walls_percent

grid = [[' ' for _ in range(width)]for _ in range(height)] 

def print_grid():
    for row in grid:
        print(' '.join(row))
    print()
 


wall_positions = set()

while len(wall_positions) < num_of_walls:
    x,y = random.randint(0, width-1), random.randint(0, height-1)
    if (x,y)!=(0,0) and (x,y) not in wall_positions:
        wall_positions.add((x,y))
        grid[y][x] = '#'

food_positions = set()

while len(food_positions) < num_of_foods:
    x,y = random.randint(0, width-1), random.randint(0, height-1)
    if (x,y) != (0,0) and (x,y) not in wall_positions:
        food_positions.add((x,y))
        grid[y][x] = 'F'
directions = [(-1,0),(1,0),(0,1),(0,-1)]
pacman_pos = (0,0)

def bfs(start_pos):
    queue = deque()
    visited = set()
    queue.append((start_pos, []))
    while queue:
        (x,y), path = queue.popleft()
        
        if (x,y) in visited:
            continue
        visited.add((x,y))
        
        if (x,y) in food_positions:
            return path + [(x,y)]
        
        for dx,dy in directions:
            nx,ny = x+dx, y+dy
            if 0<=ny<=height-1 and 0<=nx<= height-1 and grid[ny][nx]!='#':
                queue.append(((nx,ny), path+[(x,y)]))
    return None       
step = 0
while food_positions:
    path = bfs(pacman_pos)
    if not path:
        print("No path found.")
        break
    for next_pos in path[1:]:
        grid[pacman_pos[1]][pacman_pos[0]] = ' '
        pacman_pos = next_pos
        if pacman_pos in food_positions:
            food_positions.remove(pacman_pos)
        grid[pacman_pos[1]][pacman_pos[0]] = 'P'
        print(f"step: {step}")
        print_grid()
        step+=1
    print("All foods are successfully eaten.")    
 