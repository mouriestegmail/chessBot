class Debut:
    def __init__(self, filename):
        self.file_path = filename
        self.moves = []
        try:
            with open(self.file_path, 'r') as file:
                i = 0
                for line_number, line in enumerate(file, start=1):
                    if i == 0:
                        self.colour = line.strip()
                        print(f"Opening by  {self.colour}")
                        i += 1
                        continue
                    i += 1
                    line = line.lower()
                    words_in_line = line.strip().split()  # Разбиваем строку на слова
                    self.moves.extend(words_in_line)  # Добавляем слова в общий массив
        except FileNotFoundError:
            print(f"Файл '{self.file_path}' не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        for i in range(len(self.moves)):
            if "0-0" in self.moves[i]:
                if i % 2 == 0:
                    self.moves[i] = "e1"+self.moves[i]
                else:
                    self.moves[i] = "e8" + self.moves[i]

    def pop_move(self):
        return self.moves.pop(0)
    def get_move(self):
        return self.moves[0]

    def check_move(self, move):
        if len(self.moves) == 0:
            return False
        print(move, self.moves[0])
        return move in self.moves[0]