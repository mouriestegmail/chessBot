###print('ya krytoy')
dir = 'D:/chess'



import os
import random


def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

directories = list_directories(dir)

# Запрос числа у пользователя
user_input = input(f"choose the opening (1-{len(directories)})  \n  {directories}")

# Преобразование введенного значения в число (например, в целое)
number = int(user_input) -1



# Вывод числа для проверки
print(directories[number])

dir = dir+'/' + directories[number]



def choose_random_file(directory):
    # Получаем список всех файлов в директории
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Проверяем, есть ли файлы в директории
    if not files:
        print("В директории нет файлов.")
        return None

    # Выбираем случайный файл
    random_file = random.choice(files)
    return random_file


chosen_file = dir+'/'+choose_random_file(dir)





def load_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = [line.strip().split(' ', 1) for line in file]
    return questions

def quiz(questions):
    score = 0
    for question, correct_answer in questions:
        user_answer = input(f"{question} ").strip()
        if user_answer.lower() == correct_answer.lower():
            score += 1
        else:
            print(f"Неправильно! Правильный ответ: {correct_answer}")
            print("Игра окончена.")
            break  # Завершаем игру при неверном ответе
    else:
        print(f"Ваш общий балл: {score} из {len(questions)}")
        return score  # Вернуть счёт только если игра не закончилась

questions = load_questions(chosen_file)
score = quiz(questions)

print(f"Ваш общий балл: {score} из {len(questions)}")









