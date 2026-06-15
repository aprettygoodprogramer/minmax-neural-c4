from board import connect_board

def main():
    print("Hello from minmax-neural-c4!")
    board = connect_board()
    board.print_board()
    board.drop_piece(3, 1)
    board.drop_piece(3, 1)
    board.drop_piece(3, 1)
    board.drop_piece(3, 1)
    print("\n")
    board.print_board()
    print(board.check_winner(1))



if __name__ == "__main__":
    main()
