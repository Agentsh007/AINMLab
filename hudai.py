class ProblemSolver:
    def __init__(self, ):
        pass
    
    
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
    
    
    
    