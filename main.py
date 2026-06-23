from board import connect_board
from minmax import minmax
import os

from stable_baselines3 import DQN
from ai import connect_dqn
def main():
    print("Welcome, what do you want to do?")
    print("1: Train AI, 2: Play AI, 3: Play Minmax 4: Minmax vs Minmax 5: Train Self 6: AI vs AI")
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
    if option == "5":
        train_self_play(20, 500000, "rockhouse_v2")
    if option == "6":
        m1=input("What model do you want?: ")
        m2=input("Whats the seccond one?: ")
        who=int(input("Who first? 1 or 2?"))
        model_vs_model(m1, m2, who)

 

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
        




def model_vs_model(model_name1, model_name2, first):
    game = connect_board()
    game_over = False
    model1 = DQN.load(model_name1)
    model2 = DQN.load(model_name2)

    AI1=1
    AI2=-1
    if first==1:
        current_turn=AI1
    else:
        current_turn=AI2


    
    while not game_over:
        print("\n \n")
        game.print_board()
        if current_turn == AI1:
            obs = game.get_board()
            action, _ = model1.predict(obs, deterministic=True)
            game.drop_piece(int(action), AI1)


            if game.check_winner(AI1):
                print("\n")
                game.print_board()
                print("The First Clanker won!")
                game_over = True
        elif current_turn == AI2:
            obs = game.get_board()
            action, _ = model2.predict(obs, deterministic=True)
            game.drop_piece(int(action), AI2)
        if game.check_winner(AI2):
            game.print_board()
            print("The Seccond clanker won.")
            game_over = True

        if not game_over and game.is_tie():
            print("\n")
            game.print_board()
            print("67, its a tie")
            game_over = True
        if current_turn == AI1:
            current_turn=AI2
        else:
            current_turn=AI1
        




def train_model(timesteps, model_name, save_model_name):
    new_env = connect_dqn()

    file_path = model_name if model_name.endswith(".zip") else f"{model_name}.zip"

    if os.path.exists(file_path):
        print(f"Found existing model '{model_name}'. Loading to continue training...")
        model = DQN.load(model_name)
        model.set_env(new_env)
    else:
        print(f"Model '{model_name}' not found. Creating a BRAND NEW model...")
        model = DQN(
            "MlpPolicy",
            new_env,
            buffer_size=100000,
            learning_starts=10000,
            target_update_interval=1000,
            exploration_fraction=0.2,
            verbose=1,
        )

    model.learn(total_timesteps=timesteps)

    model.save(save_model_name)
def minmax_vs_human():
    board = connect_board()
    minmaxalg=minmax()
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
        best_move=minmaxalg.find_best_move(board, -1, 5)
        board.drop_piece(best_move, -1)
        
        if board.check_winner(-1):
            print("\n")
            board.print_board()
            print("Player -1 Won!")
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
        best_move=minmaxalg2.find_best_move(board, -1, 5)
        board.drop_piece(best_move, -1)
        
        if board.check_winner(-1):
            print("\n")
            board.print_board()
            print("Player 2 Won!")

            break


def train_self_play(generations, timesteps_per_generation, base_name):
    current_opponent = None 

    for gen in range(1, generations + 1):
        
        opponent_model = None
        if current_opponent is not None and os.path.exists(current_opponent):
            opponent_model = DQN.load(current_opponent)
        else:
            print(" No opponent found. ")

        env = connect_dqn(opponent_model=opponent_model)

        agent_name = f"{base_name}_gen_{gen}.zip"
        
        if gen > 1:
            model = DQN.load(current_opponent, env=env)
        else:
            print(f"makin new brain")
            model = DQN(
                "MlpPolicy",
                env,
                buffer_size=100000,
                learning_starts=10000,
                target_update_interval=1000,
                exploration_fraction=0.2,
                verbose=0, 
            )

        print(f"Training for {timesteps_per_generation} timesteps...")
        model.learn(total_timesteps=timesteps_per_generation)

        model.save(agent_name)
        current_opponent = agent_name
        
        print(f"Generation {gen} complete and saved as '{agent_name}'.")


if __name__ == "__main__":
    main()
