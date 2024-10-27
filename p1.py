import tkinter as tk
from PIL import Image, ImageTk

# Начальная расстановка фигур
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# Создаем главное окно
root = tk.Tk()
root.title("Шахматная доска")

# Размер клетки и изображения
square_size = 60

# Загрузка изображений фигур
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

# Рисуем доску
canvas = tk.Canvas(root, width=square_size * 8, height=square_size * 8)
canvas.pack()

# Функция для обновления доски на холсте
def draw_board():
    colors = ["#F0D9B5", "#B58863"]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            canvas.create_rectangle(col * square_size, row * square_size,
                                    (col + 1) * square_size, (row + 1) * square_size, fill=color)
            piece = board[row][col]
            if piece != " ":
                canvas.create_image(col * square_size, row * square_size, anchor=tk.NW, image=images[piece])

# Преобразование буквенно-цифровой нотации в координаты
def notation_to_coordinates(move):
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    start_col, start_row = columns[move[0]], 8 - int(move[1])
    end_col, end_row = columns[move[2]], 8 - int(move[3])
    return (start_row, start_col), (end_row, end_col)

# Функция для обработки хода и обновления доски
def make_move(event=None):
    move = move_entry.get()
    try:
        (start_row, start_col), (end_row, end_col) = notation_to_coordinates(move)
        piece = board[start_row][start_col]
        board[start_row][start_col] = " "
        board[end_row][end_col] = piece
        draw_board()
        move_entry.delete(0, tk.END)  # Очищаем поле ввода
    except (IndexError, KeyError, ValueError):
        print("Некорректный ход. Попробуйте снова.")

# Поле ввода
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
move_entry = tk.Entry(input_frame, width=10)
move_entry.grid(row=0, column=0)

# Привязываем клавишу Enter к функции make_move
move_entry.bind("<Return>", make_move)

# Начальная отрисовка доски
draw_board()

# Запуск GUI
root.mainloop()
