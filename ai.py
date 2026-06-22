from board import connect_board
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from minmax import minmax
class connect_dqn(gym.Env):
    def __init__(self):
        super(connect_dqn, self).__init__()
        self.board = connect_board()
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(6, 7), dtype=int
        )
        self.minmax = minmax()
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board_env = connect_board() 
        return self.board_env.get_board(), {}
    def step(self, action):
       
        is_val_move = self.board_env.drop_piece(column=action, player=1)
        
        if not is_val_move:
            return self.board_env.get_board(), -10, True, False, {}

        if self.board_env.check_winner(player=1):
            return self.board_env.get_board(), 1, True, False, {}
            
        if self.board_env.is_tie():
            return self.board_env.get_board(), 0, True, False, {}


        valid_moves = self.board_env.available_moves()
        
        opp_action = np.random.choice(valid_moves)
        #best_move = self.minmax.find_best_move(self.board_env, -1, 1)
        #self.board_env.drop_piece(best_move, player=-1)

        if self.board_env.check_winner(player=-1):
            return self.board_env.get_board(), -1, True, False, {}
            
        if self.board_env.is_tie():
            return self.board_env.get_board(), 0, True, False, {}

        return self.board_env.get_board(), 0, False, False, {}
    
        
