import numpy as np

class backtracking_solver:
    def __init__(self, board, shape):
        self.board = board
        self.solution = np.zeros(shape)
    
    def solve(self):
        if self.place_queen(0):
            return self.solution
        else:
            return None  # No valid solution found
    
    def place_queen(self, row):
        if row >= self.solution.shape[0]:
            return True
        
        for col in range(self.solution.shape[0]):
            if self.is_valid(row, col):
                self.solution[row, col] = 1
                if self.place_queen(row + 1):
                    return True
                self.solution[row, col] = 0
        
        return False
    
    def is_valid(self, row, col):
        # Check for queens in the same column
        if np.sum(self.solution[:, col]) > 0:
            return False
        
        # Check for queens in the same row
        if np.sum(self.solution[row, :]) > 0:
            return False
        
        # Check for queens adjacent diagonally
        if row > 0 and col > 0 and self.solution[row - 1, col - 1] == 1:
            return False
        if row > 0 and col < 8 and self.solution[row - 1, col + 1] == 1:
            return False
        if row < 8 and col > 0 and self.solution[row + 1, col - 1] == 1:
            return False
        if row < 8 and col < 8 and self.solution[row + 1, col + 1] == 1:
            return False
        
        return self.is_color_valid(row, col)

    def is_color_valid(self, row, col):
        colores = self.board[self.solution == 1]
        colors1 = set(colores)
        colors2 = set(colores)
        colors1.add(self.board[row, col])
        if len(colors1) == len(colors2):
            return False
        else:
            return True