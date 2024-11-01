import os
import tkinter as tk
from time import sleep

from PIL import Image, ImageTk
from debut import *

directory_path = "./data"
dir_name = ""
file_name = ""
debut = None
start_field = None
start_colour = None
start_piece = None

directories = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

# Начальная расстановка фигур
initial_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# Текущая расстановка фигур
board = [row[:] for row in initial_board]

root = tk.Tk()
root.title("Шахматная доска")



square_size = 100

images = {
    "P": ImageTk.PhotoImage(Image.open("F/Pw.png").resize((square_size, square_size))),
    "R": ImageTk.PhotoImage(Image.open("F/Rw.png").resize((square_size, square_size))),
    "N": ImageTk.PhotoImage(Image.open("F/Nw.png").resize((square_size, square_size))),
    "B": ImageTk.PhotoImage(Image.open("F/Bw.png").resize((square_size, square_size))),
    "Q": ImageTk.PhotoImage(Image.open("F/Qw.png").resize((square_size, square_size))),
    "K": ImageTk.PhotoImage(Image.open("F/Kw.png").resize((square_size, square_size))),
    "p": ImageTk.PhotoImage(Image.open("F/Pb.png").resize((square_size, square_size))),
    "r": ImageTk.PhotoImage(Image.open("F/Rb.png").resize((square_size, square_size))),
    "n": ImageTk.PhotoImage(Image.open("F/Nb.png").resize((square_size, square_size))),
    "b": ImageTk.PhotoImage(Image.open("F/Bb.png").resize((square_size, square_size))),
    "q": ImageTk.PhotoImage(Image.open("F/Qb.png").resize((square_size, square_size))),
    "k": ImageTk.PhotoImage(Image.open("F/Kb.png").resize((square_size, square_size))),
}

canvas = tk.Canvas(root, width=square_size * 8 + 40, height=square_size * 8 + 40)
canvas.grid(row=0, column=0)

root.geometry("+500+50")

is_flipped = False

# Списки для хранения координат всех подсвеченных клеток и выбранной фигуры
highlighted_squares = []  # Для правого клика
selected_square = None  # Для левого клика на фигуру

highlight_color = "#FF6347"  # Охряный цвет для правой кнопки
selected_color = "#228B22"  # Тёмно-зелёный цвет для левой кнопки


# Функция для добавления/удаления подсветки клетки при правом клике
def highlight_square(event):
    global selected_square  # Сброс тёмно-зелёной подсветки
    selected_square = None  # Убираем выбранную фигуру при правом клике

    col = (event.x - 20) // square_size
    row = (event.y - 20) // square_size
    if 0 <= col < 8 and 0 <= row < 8:
        display_row = 7 - row if is_flipped else row
        display_col = 7 - col if is_flipped else col
        # Если клетка уже подсвечена, убираем её из списка; иначе добавляем
        if (display_row, display_col) in highlighted_squares:
            highlighted_squares.remove((display_row, display_col))
        else:
            highlighted_squares.append((display_row, display_col))

        draw_board()  # Перерисовываем доску с обновлённой подсветкой


# Функция для выбора фигуры при нажатии левой кнопкой или сброса всех подсветок
def select_piece(event):
    rows = ['a','b','c','d','e','f','g','h']
    global selected_square
    global start_field
    global start_colour
    global start_piece

    col = (event.x - 20) // square_size
    row = (event.y - 20) // square_size

    if 0 <= col < 8 and 0 <= row < 8:
        display_row = 7 - row if is_flipped else row
        display_col = 7 - col if is_flipped else col
        piece = board[display_row][display_col]

        if piece != " ":
            colour = "while" if piece.isupper() else "black"
        else:
            colour = None



        # Проверка на наличие фигуры



        flag = piece != " "
        if flag:

            if start_colour is not None and start_colour != colour:
                flag = False

        if flag:
        # if piece != " " or (start_colour is not None and start_colour == colour):
            is_white_piece = piece.isupper()

            # Условие: если нажали повторно на ту же клетку, то снимаем выделение
            if selected_square == (display_row, display_col):
                selected_square = None
            # Проверяем ограничение по цвету и назначаем подсветку, если цвета совпадают
            elif (is_flipped and not is_white_piece) or (not is_flipped and is_white_piece):
                selected_square = (display_row, display_col)
                start_field = f'{rows[display_col]}{7-display_row+1}'
                start_colour = "while" if piece.isupper() else "black"
                start_piece = piece

            else:
                selected_square = None
                start_field = None
                start_colour = None
                start_piece = None
        else:
            # Если нажали на пустую клетку, убираем выделение

            if start_field is not None:
                field = f'{rows[display_col]}{7-display_row+1}'
                move = start_field + field

                if start_piece == "K":
                    if field == "g1":
                        move = "e10-0"
                    if field == "c1":
                        move = "e10-0-0"
                if start_piece == "k":
                    if field == "g8":
                        move = "e80-0"
                    if field == "c8":
                        move = "e80-0-0"

                if debut.check_move(move):
                    make_move_from_code(debut.pop_move())
                    root.after(1000, lambda: make_move_from_code(debut.pop_move()))

            start_colour = None
            start_field = None


            selected_square = None
            highlighted_squares.clear()

    draw_board()  # Перерисовываем доску с обновлённой подсветкой


# Обновленная функция для отрисовки доски с учётом всех подсвеченных клеток
def draw_board():
    canvas.delete("all")
    colors = ["#F0D9B5", "#B58863"]
    for row in range(8):
        for col in range(8):
            display_row = 7 - row if is_flipped else row
            display_col = 7 - col if is_flipped else col

            # Подсвечиваем выбранную фигуру тёмно-зелёным или клетки правого клика охряным
            if (display_row, display_col) == selected_square:
                color = selected_color
            elif (display_row, display_col) in highlighted_squares:
                color = highlight_color
            else:
                color = colors[(row + col) % 2]

            canvas.create_rectangle(20 + col * square_size, 20 + row * square_size,
                                    20 + (col + 1) * square_size, 20 + (row + 1) * square_size, fill=color)

            # Отображаем фигуру, если она есть на данной клетке
            piece = board[display_row][display_col]
            if piece != " ":
                canvas.create_image(20 + col * square_size, 20 + row * square_size, anchor=tk.NW, image=images[piece])


# Привязка функций к кнопкам мыши
canvas.bind("<Button-3>", highlight_square)  # Подсветка при правом клике
canvas.bind("<Button-1>", select_piece)  # Подсветка фигуры при левом клике


def flip_board():
    global is_flipped
    is_flipped = not is_flipped
    draw_board()

def reset_board():
    global board
    board = [row[:] for row in initial_board]
    draw_board()

def notation_to_coordinates(move):
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    start_col, start_row = columns[move[0]], 8 - int(move[1])
    end_col, end_row = columns[move[2]], 8 - int(move[3])
    return (start_row, start_col), (end_row, end_col)

def castle(move):

    """Функция для выполнения рокировки"""
    if move == "e10-0-0":  # Длинная рокировка белых
        if board[7][4] == "K" and board[7][0] == "R":  # Проверяем, что король и ладья на нужных позициях
            board[7][4] = " "   # Убираем короля с начальной позиции
            board[7][0] = " "   # Убираем ладью с начальной позиции
            board[7][2] = "K"   # Ставим короля на новую позицию
            board[7][3] = "R"   # Ставим ладью на новую позицию
            print("Длинная рокировка белых выполнена")
            return True
    elif move == "e10-0":  # Короткая рокировка белых
        if board[7][4] == "K" and board[7][7] == "R":
            board[7][4] = " "
            board[7][7] = " "
            board[7][6] = "K"
            board[7][5] = "R"
            print("Короткая рокировка белых выполнена")
            return True
    elif move == "e80-0-0":  # Длинная рокировка черных
        if board[0][4] == "k" and board[0][0] == "r":
            board[0][4] = " "
            board[0][0] = " "
            board[0][2] = "k"
            board[0][3] = "r"
            print("Длинная рокировка черных выполнена")
            return True
    elif move == "e80-0":  # Короткая рокировка черных
        if board[0][4] == "k" and board[0][7] == "r":
            board[0][4] = " "
            board[0][7] = " "
            board[0][6] = "k"
            board[0][5] = "r"
            print("Короткая рокировка черных выполнена")
            return True
    return False  # Возвращаем False, если команда не соответствует рокировке

def make_move_from_code(move):
    if castle(move):  # Проверяем, является ли команда рокировкой
        draw_board()  # Перерисовываем доску после рокировки
        return
    try:
        (start_row, start_col), (end_row, end_col) = notation_to_coordinates(move)
        piece = board[start_row][start_col]

        if piece == " ":
            print("Нет фигуры на начальной позиции.")
            return
        board[start_row][start_col] = " "
        board[end_row][end_col] = piece
        draw_board()
        print(f"Ход выполнен: {move}")
    except (IndexError, KeyError, ValueError):
        print("Некорректный ход. Попробуйте снова.")


def make_move(event=None):
    global debut
    move = move_entry.get()

    if debut.check_move(move):
        make_move_from_code(debut.pop_move())
        root.after(1000, lambda: make_move_from_code(debut.pop_move()))

        move_entry.delete(0, tk.END)
    else:
        print("something went wrong")


input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, pady=10)
move_entry = tk.Entry(input_frame, width=10)
move_entry.grid(row=0, column=0)

flip_button = tk.Button(input_frame, text="Перевернуть доску", command=flip_board)
flip_button.grid(row=0, column=1)

reset_button = tk.Button(input_frame, text="Начальная расстановка", command=reset_board)
reset_button.grid(row=0, column=2)

move_entry.bind("<Return>", make_move)

button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

file_button_frame = tk.Frame(root)
file_button_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

buttons = []
file_buttons = []

def on_directory_button_click(directory_name):
    global dir_name
    dir_name = directory_path + "/" + directory_name
    print(f"Нажата кнопка каталога: {directory_name}")

def highlight_button(selected_button):
    for button in buttons:
        button.config(bg="SystemButtonFace")
    selected_button.config(bg="lightblue")
    root.title(selected_button.cget("text"))
    update_file_buttons(selected_button.cget("text"))
    on_directory_button_click(selected_button.cget("text"))

def update_file_buttons(selected_directory):
    for widget in file_button_frame.winfo_children():
        widget.destroy()
    file_buttons.clear()
    selected_path = os.path.join(directory_path, selected_directory)
    files = [f for f in os.listdir(selected_path) if os.path.isfile(os.path.join(selected_path, f))]
    for file_name in files:
        create_file_button(file_name)

def on_file_button_click(file):
    global file_name
    global debut
    file_name = dir_name + "/" + file
    debut = Debut(file_name)

    reset_board()

    if (debut.colour == "white" and is_flipped) or (debut.colour == "black" and not is_flipped):

        flip_board()


    if debut.colour == "black":
        root.after(1000, lambda: make_move_from_code(debut.pop_move()))

def highlight_file_button(selected_file_button):
    for button in file_buttons:
        button.config(bg="SystemButtonFace")
    selected_file_button.config(bg="lightgreen")

def create_file_button(file_name):
    file_button = tk.Button(file_button_frame, text=file_name, width=20)
    file_button.config(command=lambda: [highlight_file_button(file_button), on_file_button_click(file_name)])
    file_button.pack(pady=5)
    file_buttons.append(file_button)

for dir_name in directories:
    button = tk.Button(button_frame, text=dir_name, width=20)
    button.config(command=lambda b=button: highlight_button(b))
    button.pack(pady=5)
    buttons.append(button)

draw_board()

root.mainloop()
