from board import connect_board
from minmax import minmax
from stable_baselines3 import DQN
from ai import connect_dqn
def main():
    play_ai("dqn_connect4_v2.zip", "AI")
 

def play_ai(model_name, first):
    game = connect_board()
    game_over = False
    model = DQN.load(model_name)

    HUMAN = -1
    AI = 1
    if first=="AI":
        current_turn = AI 
    else:
        current_turn = HUMAN


    
    while not game_over:
        print("\n \n")
        game.print_board()
        if current_turn == HUMAN:
            print("Which Collomn do you want to drop?")
            col=int(input())
            game.drop_piece(col, HUMAN)
            if game.check_winner(HUMAN):
                game.print_board()
                print("You beat the clankerr!")
                game_over = True
        elif current_turn == AI:
            obs = game.get_board()
            action, _ = model.predict(obs, deterministic=True)
            game.drop_piece(int(action), AI)
        if game.check_winner(AI):
            game.print_board()
            print("The Clanker won...")
            game_over = True
        if not game_over and game.is_tie():
            game.print_board()
            print("67, its a tie")
            game_over = True
        if current_turn == AI:
            current_turn=HUMAN
        else:
            current_turn=AI
        








def train_model(timesteps, model_name):
    new_env = connect_dqn()

    model = DQN.load("dqn_connect4")

    model.set_env(new_env)

    model.learn(total_timesteps=timesteps) 

    model.save(model_name)
def minmax_vs_human():
    board = connect_board()
    minmaxalg=minmax(board)
    while True:
        board.print_board()
        print("What move do you want to do?")
        move=int(input())
        print("\n")
        board.drop_piece(move, 1)



        if board.check_winner(1):
            print("\n")
            board.print_board()
            print("Player 1 Won!")
            break
        if board.is_tie():
            print("Tie Game!")
            break
        best_move=minmaxalg.find_best_move(board, 2, 5)
        board.drop_piece(best_move, 2)
        
        if board.check_winner(2):
            print("\n")
            board.print_board()
            print("Player 2 Won!")
            break
        

    
def play_self():
    board = connect_board()
    has_won=False
    minmaxalg=minmax(board)
    minmaxalg2=minmax(board)
    while True:
        print("\n")
        board.print_board()

        best_move=minmaxalg.find_best_move(board, 1, 2)
        board.drop_piece(best_move, 1)


        if board.check_winner(1):
            print("\n")
            board.print_board()
            print("Player 1 Won!")
            break
        if board.is_tie():
            print("Tie Game!")
            break
        best_move=minmaxalg2.find_best_move(board, 2, 5)
        board.drop_piece(best_move, 2)
        
        if board.check_winner(2):
            print("\n")
            board.print_board()
            print("Player 2 Won!")

            break



if __name__ == "__main__":
    main()
