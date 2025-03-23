import os
import re
import pandas as pd
from docx import Document


# Функція для обробки тексту з Word
def extract_numbers_from_word(doc_path):
    # Відкриваємо документ Word
    doc = Document(doc_path)

    # Створюємо список для збереження чисел
    numbers = []

    # Проходимо по кожному абзацу і шукаємо числа в дужках
    for para in doc.paragraphs:
        # Шукаємо всі числа в дужках за допомогою регулярних виразів
        numbers_in_para = re.findall(r'\((\d+)\)', para.text)
        numbers.extend(numbers_in_para)  # Додаємо знайдені числа в список

    return numbers


# Функція для запису даних у Excel
def save_to_excel(numbers, word_file_path):
    # Отримуємо ім'я файлу без розширення
    folder = os.path.dirname(word_file_path)
    file_name = os.path.splitext(os.path.basename(word_file_path))[0]

    # Перевіряємо, чи існує файл з таким ім'ям
    excel_file_path = os.path.join(folder, f"{file_name}.xlsx")
    counter = 1
    while os.path.exists(excel_file_path):
        excel_file_path = os.path.join(folder, f"{file_name}_{counter}.xlsx")
        counter += 1

    # Створюємо DataFrame з чисел, кожне в окремому стовпчику
    df = pd.DataFrame([numbers])

    # Записуємо DataFrame в Excel файл
    df.to_excel(excel_file_path, index=False, header=False)

    print(f"Файл збережено як: {excel_file_path}")


# Основна функція
def process_word_file(word_file_path):
    # Отримуємо числа з документа
    numbers = extract_numbers_from_word(word_file_path)

    # Якщо є числа, записуємо їх у Excel
    if numbers:
        save_to_excel(numbers, word_file_path)
    else:
        print("Чисел у документі не знайдено.")


# Введіть шлях до вашого файлу Word
word_file_path = input("Введіть шлях до файлу Word: ")
process_word_file(word_file_path)
