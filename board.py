import numpy as np
from scipy.signal import convolve2d
class connect_board:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
    def print_board(self):
        print(self.board)
    def drop_piece(self, column, player):
            empty_rows = np.where(self.board[:, column] == 0)[0]
    
            if len(empty_rows) > 0:
                lowest_row = empty_rows[-1]
                self.board[lowest_row, column] = player
                return True
            else:
                #column full
                return False
    def check_winner(self, player):
        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.array([[1], [1], [1], [1]])
        diagonal_down_kernel = np.eye(4)  
        diagonal_up_kernel = np.fliplr(np.eye(4))  
        player_mask = (self.board == player).astype(int)

        kernels=[horizontal_kernel, vertical_kernel, diagonal_down_kernel, diagonal_up_kernel]
        for i in kernels:
            if np.any(convolve2d(player_mask, i, mode='valid') == 4):
                return True
    

         
         
