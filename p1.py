import os
import tkinter as tk
from PIL import Image, ImageTk

# Путь к каталогу с папками
directory_path = "d:/chess"

# Получаем список имен каталогов
directories = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

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

# Рисуем доску с размерами чуть больше, чтобы добавить подписи
canvas = tk.Canvas(root, width=square_size * 8 + 40, height=square_size * 8 + 40)
canvas.grid(row=0, column=0)

# Переменная для отслеживания переворота доски
is_flipped = False


def draw_board():
    canvas.delete("all")  # Очищаем все элементы на холсте перед перерисовкой
    colors = ["#F0D9B5", "#B58863"]

    # Отрисовываем доску в зависимости от направления
    for row in range(8):
        for col in range(8):
            # Рассчитываем строку и колонку в зависимости от переворота
            display_row = 7 - row if is_flipped else row
            display_col = 7 - col if is_flipped else col
            color = colors[(row + col) % 2]
            canvas.create_rectangle(20 + col * square_size, 20 + row * square_size,
                                    20 + (col + 1) * square_size, 20 + (row + 1) * square_size, fill=color)
            piece = board[display_row][display_col]
            if piece != " ":
                canvas.create_image(20 + col * square_size, 20 + row * square_size, anchor=tk.NW, image=images[piece])

    # Обновление подписей для строк и столбцов
    for i in range(8):
        # Отображаем номера и буквы в зависимости от переворота
        row_label = str(8 - i) if not is_flipped else str(i + 1)
        col_label = chr(97 + i) if not is_flipped else chr(104 - i)
        canvas.create_text(10, 20 + i * square_size + square_size / 2, text=row_label, font=("Arial", 12))
        canvas.create_text(20 + i * square_size + square_size / 2, 8 * square_size + 30, text=col_label,
                           font=("Arial", 12))

# Функция для переворота доски
def flip_board():
    global is_flipped
    is_flipped = not is_flipped
    draw_board()

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

# Поле ввода и кнопка переворота
input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, pady=10)
move_entry = tk.Entry(input_frame, width=10)
move_entry.grid(row=0, column=0)

flip_button = tk.Button(input_frame, text="Перевернуть доску", command=flip_board)
flip_button.grid(row=0, column=1)

# Привязываем клавишу Enter к функции make_move
move_entry.bind("<Return>", make_move)

# Панель с кнопками для каталогов
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

# Панель с кнопками для файлов внутри выбранного каталога
file_button_frame = tk.Frame(root)
file_button_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

# Списки для хранения кнопок
buttons = []
file_buttons = []

# Функция для подсветки выбранной кнопки каталога и обновления списка файлов
def highlight_button(selected_button):
    for button in buttons:
        button.config(bg="SystemButtonFace")  # Сбрасываем стиль всех кнопок
    selected_button.config(bg="lightblue")  # Подсвечиваем выбранную кнопку
    root.title(selected_button.cget("text"))  # Устанавливаем заголовок окна как текст кнопки
    update_file_buttons(selected_button.cget("text"))  # Обновляем список файлов в выбранном каталоге

# Функция для подсветки выбранной кнопки файла
def highlight_file_button(selected_file_button):
    for button in file_buttons:
        button.config(bg="SystemButtonFace")  # Сбрасываем стиль всех кнопок файлов
    selected_file_button.config(bg="lightgreen")  # Подсвечиваем выбранную кнопку файла

# Функция для обновления кнопок файлов в выбранном каталоге
def update_file_buttons(selected_directory):
    # Очищаем старые кнопки файлов
    for widget in file_button_frame.winfo_children():
        widget.destroy()
    file_buttons.clear()  # Очищаем список file_buttons

    # Путь к выбранному каталогу
    selected_path = os.path.join(directory_path, selected_directory)

    # Получаем список файлов в выбранном каталоге
    files = [f for f in os.listdir(selected_path) if os.path.isfile(os.path.join(selected_path, f))]

    # Создаем кнопки для каждого файла
    for file_name in files:
        create_file_button(file_name)

# Функция для создания кнопки файла с подсветкой
def create_file_button(file_name):
    file_button = tk.Button(file_button_frame, text=file_name, width=20)
    file_button.config(command=lambda b=file_button: highlight_file_button(b))
    file_button.pack(pady=5)
    file_buttons.append(file_button)

# Создаем кнопки для каждого каталога
for dir_name in directories:
    button = tk.Button(button_frame, text=dir_name, width=20)
    button.config(command=lambda b=button: highlight_button(b))  # Передаем текущую кнопку в лямбда-функцию
    button.pack(pady=5)
    buttons.append(button)

# Начальная отрисовка доски
draw_board()

# Запуск GUI
root.mainloop()
