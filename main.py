from board import connect_board
from minmax import minmax
def main():
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
