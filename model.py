from typing import Optional
from debut import Debut
import copy

class Field:
    def __init__(self, piece: Optional[str] = None, is_white: Optional[bool] = None):
        self.piece = piece
        self.is_white = None
        if self.piece is not None:
            self.is_white = is_white
        self.left_selected = False



    def __str__(self):
        return f"{self.piece}  w:{self.is_white}  sel:{self.left_selected}"

class Board:
    def __init__(self):
        self.init_board = self._create_initial_board()
        self.data = [row[:] for row in self.init_board]
        self.last_move = []

    def _create_initial_board(self):
        init_layout = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        return [[Field(piece, piece is not None and piece.isupper()) for piece in row] for row in init_layout]

    def get_selected(self):
        for r, row in enumerate(self.data):
            for c, item in enumerate(row):
                if item.left_selected:
                    return item, r, c
        return None, 0, 0


class Model:
    def __init__(self):
        self.debut: Debut or None = None
        self.__board = Board()
        self.white_move = True
        self.auto_move = False
        self.moves = []
        self.boards = []
        self.boards.append(copy.deepcopy(self.__board))
        self.shift = 0

    def help(self):
        if self.debut is None:
            return

        move = self.debut.get_move()
        if move is None:
            return
        r,c = self.get_from_from_notation(move)
        self.__board.data[r][c].left_selected = True


    def get_board(self):
        return self.__board
    def back(self):
        print(self.shift, "  ", self.moves, len(self.boards))

        if self.shift < len(self.moves):
            self.shift += 1

            print(self.shift, "  ", self.moves)

            self.__board = copy.deepcopy(self.boards[-(self.shift + 1)])
            self.white_move = not self.white_move


    def next(self):
        if self.shift > 0:
            self.shift -= 1
            self.__board = copy.deepcopy(self.boards[-(self.shift + 1)])
            self.white_move = not self.white_move




    def reset_board(self):
        self.__board = Board()
        self.white_move = True
        self.moves.clear()
        self.boards.clear()
        self.boards.append(self.__board)

    def left_click(self, row, col):

        field_to = self.__board.data[row][col]
        if field_to.left_selected:
            field_to.left_selected = False
            return True

        field_from, r, c = self.__board.get_selected()
        print(field_from, r, c)



        if field_from is not None:
            if field_to.is_white == self.white_move:
                field_to.left_selected = True
                field_from.left_selected = False
                return True

            # Проверка на рокировку
            if field_from.piece in {"K", "k"} and c == 4 and row in [0,7] and r in [0,7]:
                print("K")
                move = ""
                if col == 6:
                    print(1)
                    move = "0-0"
                elif col == 2:
                    print(2)
                    move = "0-0-0"

                if "0" in move:
                    if self.debut is not None:
                        if self.debut.check_move(move):
                            self.debut.pop_move()
                            if self.try_castling(field_from, row, col):
                                if col == 6:
                                    self.__board.last_move = [(row, col), (row, col - 1)]
                                else:
                                    self.__board.last_move = [(row, col), (row, col + 1)]
                                self.white_move = not self.white_move
                                self.auto_move = True
                                return True
                        else:
                            field_from.left_selected = False
                            return True
                    else:

                        if self.try_castling(field_from, row, col):
                            self.white_move = not self.white_move
                            if col == 6:
                                self.__board.last_move = [(row, col), (row, col - 1)]
                            else:
                                self.__board.last_move = [(row, col), (row, col + 1)]
                            self.save_move(move)
                            return True


            print("general")
            # Обычный ход
            move = self.coords_to_notation(r,c,row,col)

            print(self.moves)

            make_move = self.debut and self.debut.check_move(move) or self.debut is None

            print(field_to.is_white, self.white_move)

            if make_move:
                if self.debut is not None:
                    self.debut.pop_move()
                    self.auto_move = True
                self.__board.data[row][col] = field_from
                self.__board.last_move = [(row, col), (r,c)]
                field_from.left_selected = False
                self.__board.data[r][c] = Field()
                self.white_move = not self.white_move
                self.save_move(move)

                print("moving....")
                return True
            else:
                field_from.left_selected = False
                return True

        print("selected!!!")
        # Подсветка выбранной фигуры
        if field_to.piece is not None and field_to.is_white == self.white_move:
            print("selected")
            self.__board.data[row][col].left_selected = True
            return True

        return False
    def save_move(self,move):
        if self.debut is None:
            if self.shift > 0:
                del self.moves[-self.shift:]
                del self.boards[-self.shift:]

            self.shift = 0

            self.moves.append(copy.deepcopy(move))
            self.boards.append(copy.deepcopy(self.__board))

    def moves_to_text(self):
        result = ""
        for i, m in enumerate(self.moves):
            if i % 2 == 0 and i > 0:
                result += "\n"
            result += m + " "
        return result.rstrip()

    def try_castling(self, king_field, row, col):
        if king_field.piece == "K":
            # Рокировка белых (без проверок)
            if col == 6:  # Короткая рокировка
                self.perform_castling(7, 4, 7, 7, 5, 6)
            elif col == 2:  # Длинная рокировка
                self.perform_castling(7, 4, 7, 0, 3, 2)
            return True
        elif king_field.piece == "k":
            # Рокировка черных (без проверок)
            if col == 6:  # Короткая рокировка
                self.perform_castling(0, 4, 0, 7, 5, 6)
            elif col == 2:  # Длинная рокировка
                self.perform_castling(0, 4, 0, 0, 3, 2)
            return True
        return False

    def perform_castling(self, king_row, king_col, rook_row, rook_col, new_rook_col, new_king_col):
        """Перемещает короля и ладью при рокировке"""
        self.__board.data[king_row][king_col], self.__board.data[rook_row][rook_col] = Field(), Field()
        self.__board.data[king_row][new_king_col] = Field("K" if self.white_move else "k", self.white_move)
        self.__board.data[rook_row][new_rook_col] = Field("R" if self.white_move else "r", self.white_move)



    def load_debut(self, filename):
        self.debut = Debut(filename=filename)
        if self.debut.colour == "black":
            self.auto_move = True
    def reset_debut(self):
        self.debut = None
    def make_debut_move(self, callback):
        if not self.auto_move:
            return
        move = self.debut.get_move()
        if move is None:
            return
        self.make_move_from_notation(move)
        callback()
        self.auto_move = False


    def coords_to_notation(self, from_row, from_col, to_row, to_col):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        from_col_letter = columns[from_col]
        to_col_letter = columns[to_col]
        from_row_number = 8 - from_row  # Переводим индекс строки в шахматную нотацию
        to_row_number = 8 - to_row

        return f"{from_col_letter}{from_row_number}{to_col_letter}{to_row_number}"

    def get_from_from_notation(self, notation):
        if "0-0" in notation:
            if self.white_move:
                return 7, 4
            else:
                return 0, 4

        columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        from_col = columns[notation[0]]
        from_row = 8 - int(notation[1])
        return from_row, from_col

    def make_move_from_notation(self, notation):
        print("make_move_from_notation")

        if "0-0-0" in notation:
            if self.white_move:
                self.__board.data[7][4].left_selected = True
                self.left_click(7,2)
            else:
                self.__board.data[0][4].left_selected = True
                self.left_click(0, 2)
        elif "0-0" in notation:
            if self.white_move:
                self.__board.data[7][4].left_selected = True
                self.left_click(7, 6)
            else:
                self.__board.data[0][4].left_selected = True
                self.left_click(0, 6)
        else:

            columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

            from_col = columns[notation[0]]
            from_row = 8 - int(notation[1])  # Переводим шахматную нотацию в индекс строки
            to_col = columns[notation[2]]
            to_row = 8 - int(notation[3])

            self.__board.data[from_row][from_col].left_selected = True
            self.left_click(to_row, to_col)




