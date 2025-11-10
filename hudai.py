class ProblemSolver:
    def __init__(self, start, x,y,goal):
        self.start = start
        self.start_x = x
        self.start_y = y
        self.goal = goal
        self.row_moves = [-1,1,0,0]
        self.col_moves = [0,0,-1,1]
    def solve(self,algorithm = 'bfs'):
        if algorithm == 'bfs':
            
    
    
if __name__ =='__main__':
    start_board = [
        [1,2,3],
        [4,0,5],
        [6,7,8]
    ]
    goal_board = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]
    x,y = 1,1
    problemsolve = ProblemSolver(start_board,x,y,goal_board)
    
    
    
    