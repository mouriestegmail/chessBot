from typing import Optional
from debut import Debut

class Field:
    def __init__(self, piece: Optional[str] = None, is_white: Optional[bool] = None):
        self.piece = piece
        self.is_white = None
        if self.piece is not None:
            self.is_white = is_white
        self.left_selected = False


    def __str__(self):
        return f"{self.piece}  w:{self.is_white}  sel:{self.left_selected}"


class Model:
    def __init__(self):
        self.debut: Debut or None = None
        self.init_board = self._create_initial_board()
        self.board = [row[:] for row in self.init_board]
        self.white_move = True
        self.auto_move = False
        self.moves = []

        print(self.board[4][4])



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

    def reset_board(self):
        self.board = [row[:] for row in self.init_board]

        for r in self.board:
            for i in r:
                i.left_selected = False

        self.white_move = True
        self.moves.clear()

    def left_click(self, row, col):
        field_to = self.board[row][col]
        if field_to.left_selected:
            field_to.left_selected = False
            return True

        field_from, r, c = self.get_selected()
        print(field_from, r, c)



        if field_from is not None:
            if field_to.is_white == self.white_move:
                field_to.left_selected = True
                field_from.left_selected = False
                return True

            # Проверка на рокировку
            if field_from.piece in {"K", "k"} and c == 4 and row in [0,7] and r in [0,7]:
                print("K")
                if col == 6:
                    print(1)
                    move = "0-0"
                elif col == 2:
                    print(2)
                    move = "0-0-0"
                else:
                    field_from.left_selected = False

                    return True

                if self.debut is not None:
                    if self.debut.check_move(move):
                        self.debut.pop_move()
                        if self.try_castling(field_from, row, col):
                            self.white_move = not self.white_move
                            self.auto_move = True
                            return True
                    else:
                        field_from.left_selected = False
                        return True
                else:
                    if self.try_castling(field_from, row, col):
                        self.white_move = not self.white_move
                        self.save_move(move)
                        return True


            print("general")
            # Обычный ход
            move = self.coords_to_notation(r,c,row,col)

            self.save_move(move)

            print(self.moves)

            make_move = self.debut and self.debut.check_move(move) or self.debut is None

            print(field_to.is_white, self.white_move)

            if make_move:
                if self.debut is not None:
                    self.debut.pop_move()
                    self.auto_move = True
                self.board[row][col] = field_from
                field_from.left_selected = False
                self.board[r][c] = Field()
                self.white_move = not self.white_move

                print("moving....")
                return True
            else:
                field_from.left_selected = False
                return True

        # Подсветка выбранной фигуры
        if field_to.piece is not None and field_to.is_white == self.white_move:
            print("selected")
            self.board[row][col].left_selected = True
            return True

        return False
    def save_move(self,move):
        if self.debut is None:
            self.moves.append(move)

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
        self.board[king_row][king_col], self.board[rook_row][rook_col] = Field(), Field()
        self.board[king_row][new_king_col] = Field("K" if self.white_move else "k", self.white_move)
        self.board[rook_row][new_rook_col] = Field("R" if self.white_move else "r", self.white_move)

    def get_selected(self):
        for r, row in enumerate(self.board):
            for c, item in enumerate(row):
                if item.left_selected:
                    return item, r, c
        return None, 0, 0

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

    def make_move_from_notation(self, notation):
        print("make_move_from_notation")

        if "0-0-0" in notation:
            if self.white_move:
                self.board[7][4].left_selected = True
                self.left_click(7,2)
            else:
                self.board[0][4].left_selected = True
                self.left_click(0, 2)
        elif "0-0" in notation:
            if self.white_move:
                self.board[7][4].left_selected = True
                self.left_click(7, 6)
            else:
                self.board[0][4].left_selected = True
                self.left_click(0, 6)
        else:

            columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

            from_col = columns[notation[0]]
            from_row = 8 - int(notation[1])  # Переводим шахматную нотацию в индекс строки
            to_col = columns[notation[2]]
            to_row = 8 - int(notation[3])

            self.board[from_row][from_col].left_selected = True
            self.left_click(to_row, to_col)




