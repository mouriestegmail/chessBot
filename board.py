import tkinter as tk
from PIL import Image, ImageTk
from model import *
import os
from tkinter import filedialog

class Board:
    def __init__(self, model: Model):
        self.start_field = None
        self.start_colour = None
        self.start_piece = None
        self.selected_square = None
        self.debut = None
        self.directory_path = "./data"
        self.is_recording = False  # Флаг состояния записи

        self.root = tk.Tk()
        self.root.title("Шахматная доска")

        self.square_size = 70
        size = self.square_size

        self.images = {
            "P": ImageTk.PhotoImage(Image.open("F/Pw.png").resize((size, size))),
            "R": ImageTk.PhotoImage(Image.open("F/Rw.png").resize((size, size))),
            "N": ImageTk.PhotoImage(Image.open("F/Nw.png").resize((size, size))),
            "B": ImageTk.PhotoImage(Image.open("F/Bw.png").resize((size, size))),
            "Q": ImageTk.PhotoImage(Image.open("F/Qw.png").resize((size, size))),
            "K": ImageTk.PhotoImage(Image.open("F/Kw.png").resize((size, size))),
            "p": ImageTk.PhotoImage(Image.open("F/Pb.png").resize((size, size))),
            "r": ImageTk.PhotoImage(Image.open("F/Rb.png").resize((size, size))),
            "n": ImageTk.PhotoImage(Image.open("F/Nb.png").resize((size, size))),
            "b": ImageTk.PhotoImage(Image.open("F/Bb.png").resize((size, size))),
            "q": ImageTk.PhotoImage(Image.open("F/Qb.png").resize((size, size))),
            "k": ImageTk.PhotoImage(Image.open("F/Kb.png").resize((size, size))),
        }

        self.canvas = tk.Canvas(self.root, width=size * 8 + 40, height=size * 8 + 40)
        self.canvas.grid(row=0, column=0)

        self.root.geometry("+500+50")
        self.is_flipped = False
        self.model = model
        self.choice_var = tk.StringVar()

        # Добавляем кнопки управления под доской
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, pady=10)

        self.flip_button = tk.Button(self.control_frame, text="Повернуть доску", command=self.flip_board)
        self.flip_button.grid(row=0, column=0, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Начальное положение", command=self.reset_board)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.record_button = tk.Button(self.control_frame, text="Сохранить", command=self.toggle_recording)
        self.record_button.grid(row=0, column=2, padx=5)

        self.canvas.bind("<Button-1>", self.on_left_button_click)  # Подсветка фигуры при левом клике

        # Список для кнопок каталога и файлов
        self.directory_buttons = []
        self.file_buttons = []

        # Области для кнопок каталогов и файлов
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.file_button_frame = tk.Frame(self.root)
        self.file_button_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

        # Загружаем каталоги
        self.load_directories()

    def toggle_recording(self):
        """Переключает состояние записи."""

        if len(self.model.moves) == 0:
            return



        file_path = filedialog.asksaveasfilename(
            initialdir="./data",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Сохранить файл как"
        )
        if file_path:

            color = self.confirmation_dialog()

            try:
                with open(file_path, "w") as file:
                    file.write(color + "\n")
                    file.write(self.model.moves_to_text())
                print(f"Запись в файл '{file_path}' завершена.")
            except Exception as e:
                print(f"Ошибка записи в файл: {e}")

    def confirmation_dialog(self):
        # Окно с вопросом после выбора файла
        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Какой цвет?")

        # Функции для обработки выбора
        def choose_black():
            self.choice_var.set("black")
            confirmation_window.destroy()

        def choose_white():
            self.choice_var.set("white")
            confirmation_window.destroy()

        # Кнопки для выбора цвета
        button_black = tk.Button(confirmation_window, text="Чёрный", command=choose_black)
        button_black.pack(side="left", padx=20, pady=10)

        button_white = tk.Button(confirmation_window, text="Белый", command=choose_white)
        button_white.pack(side="right", padx=20, pady=10)
        self.root.wait_variable(self.choice_var)
        return self.choice_var.get()

    def load_directories(self):
        """Создаем кнопки для каждого каталога."""
        directories = [name for name in os.listdir(self.directory_path)
                       if os.path.isdir(os.path.join(self.directory_path, name))]
        for dir_name in directories:
            button = tk.Button(self.button_frame, text=dir_name, width=20)
            button.config(command=lambda name=dir_name: self.on_directory_button_click(name))
            button.pack(pady=5)
            self.directory_buttons.append(button)

    def load_files(self, selected_directory):
        """Создаем кнопки для файлов в выбранном каталоге."""
        # Очищаем текущие кнопки файлов
        for widget in self.file_button_frame.winfo_children():
            widget.destroy()
        self.file_buttons.clear()

        # Получаем путь к выбранному каталогу
        selected_path = os.path.join(self.directory_path, selected_directory)
        files = [f for f in os.listdir(selected_path) if os.path.isfile(os.path.join(selected_path, f))]

        # Создаем кнопки для каждого файла
        for file_name in files:
            button = tk.Button(self.file_button_frame, text=file_name, width=20)
            button.config(command=lambda name=file_name: self.on_file_button_click(selected_directory, name))
            button.pack(pady=5)
            self.file_buttons.append(button)

    def on_directory_button_click(self, directory_name):
        """Обработчик для выбора каталога."""
        print(f"Выбран каталог: {directory_name}")
        self.load_files(directory_name)
        self.model.reset_debut()

    def on_file_button_click(self, directory_name, file_name):
        print(f"Выбран файл: {file_name} из каталога {directory_name}")
        file_path = os.path.join(self.directory_path, directory_name, file_name)
        self.model.load_debut(file_path)
        self.model.debut.colour = "black"
        if (self.model.debut.colour == "white" and not self.is_flipped) or \
                (self.model.debut.colour == "black" and self.is_flipped):
            self.flip_board()

        self.reset_board()

        self.root.after(1000, lambda: self.model.make_debut_move(self.draw_board))

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]
        selected_color = "#228B22"
        for r, row in enumerate(self.model.board):
            for c, item in enumerate(row):
                display_row = 7 - r if self.is_flipped else r
                display_col = 7 - c if self.is_flipped else c
                color = selected_color if item.left_selected else colors[(display_row + display_col) % 2]
                size = self.square_size

                self.canvas.create_rectangle(
                    20 + display_col * size, 20 + display_row * size,
                    20 + (display_col + 1) * size, 20 + (display_row + 1) * size,
                    fill=color
                )

                if item.piece is not None:
                    self.canvas.create_image(
                        20 + display_col * size, 20 + display_row * size,
                        anchor=tk.NW, image=self.images[item.piece]
                    )

        for i in range(8):
            letter = chr(ord('a') + (7 - i if self.is_flipped else i))
            self.canvas.create_text(20 + i * size + size / 2, 8 * size + 30, text=letter, font=("Arial", 12))
            number = str(i + 1 if self.is_flipped else 8 - i)
            self.canvas.create_text(10, 20 + i * size + size / 2, text=number, font=("Arial", 12))

    def make_move(self, move: str):
        pass

    def on_left_button_click(self, event):
        size = self.square_size
        col = (event.x - 20) // size
        row = (event.y - 20) // size
        if 0 <= col < 8 and 0 <= row < 8:
            model_row = 7 - row if self.is_flipped else row
            model_col = 7 - col if self.is_flipped else col
            if self.model.left_click(model_row, model_col):
                self.draw_board()
                self.root.after(2000, lambda: self.model.make_debut_move(self.draw_board))

    def flip_board(self):
        self.is_flipped = not self.is_flipped
        self.draw_board()

    def reset_board(self):
        self.model.reset_board()
        self.draw_board()
