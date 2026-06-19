import numpy as np
from scipy.signal import convolve2d

class minmax:
    def __init__(self, connect_board):
        self.connect_board=connect_board
    # evalulates board and returns it's "score"
    def eval(self, turn):
        board = self.connect_board.board

        if turn == 1:
            enemy_turn=2
        else:
            enemy_turn=1

        score=0

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.array([[1], [1], [1], [1]])
        diagonal_down_kernel = np.eye(4)  
        diagonal_up_kernel = np.fliplr(np.eye(4))  

        kernel=[horizontal_kernel, vertical_kernel, diagonal_down_kernel, diagonal_up_kernel]
        player_mask = (board == turn).astype(int)
        enemy_mask = (board == enemy_turn).astype(int)
        empty_mask = (board == 0).astype(int)


        center_column = board[:, 3]
        player_center_count = np.sum(center_column == turn)
        enemy_center_count = np.sum(center_column == enemy_turn)
        
        score += player_center_count * 3
        score -= enemy_center_count * 3


        for i in kernel:
            player_conv = convolve2d(player_mask, i, mode="valid")
            enemy_conv = convolve2d(enemy_mask, i, mode="valid")
            empty_conv = convolve2d(empty_mask, i, mode="valid")

            # check if player has three peices in a row
            has_three_pieces= (player_conv == 3)
            has_one_empty_space = (empty_conv == 1)
            is_unblocked_threat = has_three_pieces & has_one_empty_space
            threat_count = np.sum(is_unblocked_threat)
            score+=threat_count*10
            

            # check if enemy has three peices in a row
            has_three_pieces= (enemy_conv == 3)
            has_one_empty_space = (empty_conv == 1)
            is_unblocked_threat = has_three_pieces & has_one_empty_space
            threat_count = np.sum(is_unblocked_threat)
            score-=threat_count*10
        return score












        


        







