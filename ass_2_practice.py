from collections import deque
import random

width=10
height=10
num_food=5
wall_percentange=0.20

grid=[[' 'for _ in range(width)]for _ in range(height)]

num_walls=int(height*width*wall_percentange)
wall_position=set()
while len(wall_position)<num_walls:
    x,y=random.randint(0,width-1),random.randint(0,height-1)
    if(x,y)!=(0,0):
        wall_position.add((x,y))
for x,y in wall_position:
    grid[y][x]='#'



food_positions = set()
while len(food_positions) <num_food:
    x, y = random.randint(0, width - 1), random.randint(0, height- 1)
    if (x, y) != (0, 0) and (x, y) not in wall_position:
        food_positions.add((x, y))

for x, y in food_positions:
    grid[y][x] = 'F'
    
#pacman position
pacman_position=(0,0)
grid[pacman_position[1]][pacman_position[0]] ='p'

directions=[(-1,0),(0,-1),(0,1),(1,0)]


   
def print_grid():
    for row in grid:
        print(' '.join(row))
        print()
print_grid()
#searching
def bfs(start):
    visited=set()
    queue=deque()
    queue.append((start,[]))
    while queue:
        (x,y) , path = queue.popleft()
        
        if (x,y) in visited:
            continue
        
        visited.add((x,y))
        
        if (x,y) in food_positions:
            return path + [(x,y)]
        
        for dx, dy in directions:
            nx , ny = x + dx ,y + dy
            if 0<= nx < width and 0<=ny <height:
                if grid[ny][nx] !='#':
                    queue.append(((nx,ny),path + [(x,y)]))
    return None
        


print("Initial Grid:")
print_grid()
step = 0

while food_positions:
    path = bfs(pacman_position)
    if not path or len(path)<2:
        print("No path to remaining food!")
        break
    next_pos = path[1]
    
    grid[pacman_position[1]][pacman_position[0]] = ' ' 
    pacman_position = next_pos
    
    if pacman_position in food_positions:
        food_positions.remove(pacman_position)
    grid[pacman_position[1]][pacman_position[0]]= 'P'
    
    print(f"${step}")
    step+=1
print("All food are finished")