import numpy as np
from scipy.signal import convolve2d

class minmax:
    def __init__(self, connect_board):
        self.connect_board=connect_board
    # evalulates board and returns it's "score"
    def eval(self, turn, board):
        

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
        player_mask = (board.get_board() == turn).astype(int)
        enemy_mask = (board.get_board() == enemy_turn).astype(int)
        empty_mask = (board.get_board() == 0).astype(int)


        center_column = board.get_board()[:, 3]
        player_center_count = np.sum(center_column == turn)
        enemy_center_count = np.sum(center_column == enemy_turn)
        
        score += player_center_count * 1
        score -= enemy_center_count * 1


        for i in kernel:
            player_conv = convolve2d(player_mask, i, mode="valid")
            enemy_conv = convolve2d(enemy_mask, i, mode="valid")
            empty_conv = convolve2d(empty_mask, i, mode="valid")

            # check if player has three peices in a row
            has_three_pieces= (player_conv == 3)
            has_one_empty_space = (empty_conv == 1)
            is_unblocked_threat = has_three_pieces & has_one_empty_space
            threat_count = np.sum(is_unblocked_threat)
            score+=threat_count*100
            

            # check if enemy has three peices in a row
            has_three_pieces= (enemy_conv == 3)
            has_one_empty_space = (empty_conv == 1)
            is_unblocked_threat = has_three_pieces & has_one_empty_space
            threat_count = np.sum(is_unblocked_threat)
            score-=threat_count*1000
        return score
    
    def find_best_move(self, board, player, depth):
        best_score = -float("inf")
        best_move = None

        for i in board.available_moves():
            temp_board = board.copy()
            temp_board.drop_piece(i, player)
            score = self.minmax(False, temp_board, depth - 1, player)

            if score > best_score:
                best_score = score
                best_move = i

        return best_move

    def minmax(self, isMax, board, depth, player):
        if player == 1:
            enemy=2
        else:
            enemy=1
        if board.check_winner(player):
            return 100000 + depth
        if board.check_winner(enemy):
            return -100000 - depth
        if board.is_tie():
            return 0
        if depth==0:
            return self.eval(player, board )
        if isMax:
            best_score = -float("inf")

            for i in board.available_moves():
                temp_board = board.copy()
                temp_board.drop_piece(i, player)
                score = self.minmax(False, temp_board, depth - 1, player)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in board.available_moves():
                temp_board = board.copy()
                temp_board.drop_piece(i, enemy)
                score = self.minmax(True, temp_board, depth - 1, player)
                best_score = min(score, best_score)
            return best_score





                



        

















        


        







