from model import Model
from board import Board


def main():
    model = Model()

    board = Board(model=model)

    board.draw_board()

    board.root.mainloop()


if __name__ == "__main__":
    main()
