from board import connect_board
from minmax import minmax
from stable_baselines3 import DQN
from ai import connect_dqn
def main():
    print("Welcome, what do you want to do?")
    print("1: Train AI, 2: Play AI, 3: Play Minmax 4: Minmax vs Minmax")
    option=input()
    if option == "1":
        print("Which Model do you want to train? (Enter the file name)")
        model_name=input()
        print("What do you want this model to be saved as?")
        save_model_name=input()
        print("How long do you want the model to train (in timesteps, eg 50000)")
        timesteps = int(input())
        train_model(timesteps, model_name, save_model_name)
    if option == "2":
        print("What model do you want to play? (Enter the filename)")
        model_name=input()
        print("Who do you want to go first? (AI or Human)")
        first=input()
        play_ai(model_name, first)
    if option == "3":
        minmax_vs_human()
    if option == "4":
        play_self()
 

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
        








def train_model(timesteps, model_name, save_model_name):
    new_env = connect_dqn()

    model = DQN.load(model_name)

    model.set_env(new_env)

    model.learn(total_timesteps=timesteps) 

    model.save(save_model_name)
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
