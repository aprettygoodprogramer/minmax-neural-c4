from board import connect_board
from minmax import minmax
def main():
    print("Hello from minmax-neural-c4!")
    board = connect_board()
    for i in range(3):
        board.drop_piece(1, 1)
    
    minmaxalg=minmax(board)
    print(minmaxalg.eval(1))
    



if __name__ == "__main__":
    main()
