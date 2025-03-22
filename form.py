import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
import os
from datetime import datetime
import re

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Form:
    def __init__(self, db_file='db.db', table_name='clients'):
        """
        Формочка для створення клієнтів.

        :param db_file: Str, назва файлу бази даних (за замовчуванням db.db)
        :param table_name: Str, назва таблиці, до якої будемо записувати/видаляти дані (за замовчуванням 'clients')
        """
        self.db_file = db_file
        self.table_name = table_name
        self.client = None  # потенційний клієнт

        # основне вікно
        self.window = tk.Tk()
        self.window.title("Тут ви можете працювати з клієнтськими даними")
        self.center_window(500, 300)
        self.window.config(bg="lightblue")

        # лейбли та поля вводу
        self.create_widgets()

    # лейблики та поля вводу
    label_font = ("Arial", 11, "bold")
    label_color = "#4B8BD4"  # приємний синій колір

    def create_widgets(self):
        # загальні налаштування для лейблів та полів вводу
        self.last_name_label, self.last_name_entry = self.create_label_entry(0, "Прізвище:")
        self.first_name_label, self.first_name_entry = self.create_label_entry(1, "Ім'я:")
        self.middle_name_label, self.middle_name_entry = self.create_label_entry(2, "По батькові:")
        self.birth_date_label, self.birth_date_entry = self.create_label_entry(4, "Дата народження:", entry_width=10)
        self.death_date_label, self.death_date_entry = self.create_label_entry(5, "Дата смерті:", entry_width=10)

        # специфічний для статі combobox
        self.gender_label = tk.Label(self.window, text="Стать:", fg=self.label_color, font=self.label_font,
                                     bg="lightblue", anchor="e")
        self.gender_label.grid(row=3, column=0, pady=5, sticky="e")
        self.gender_combobox = ttk.Combobox(self.window, values=["чоловік", "жінка"], width=40, state="readonly")
        self.gender_combobox.set("чоловік")
        self.gender_combobox.grid(row=3, column=1, pady=5, sticky="ew")

        # вік
        self.age_label = tk.Label(self.window, text="Вік:", fg=self.label_color, font=self.label_font, bg="lightblue",
                                  anchor="e")
        self.age_label.grid(row=4, column=2, pady=5, sticky="e")
        self.age_value_label = tk.Label(self.window, text="0", fg=self.label_color, font=self.label_font,
                                        bg="lightblue")
        self.age_value_label.grid(row=4, column=3, pady=5, sticky="w")

        # комбобокс для імпорту
        self.import_option_label = tk.Label(self.window, text="Імпорт з:", fg=self.label_color, font=self.label_font,
                                            bg="lightblue", anchor="e")
        self.import_option_label.grid(row=6, column=0, pady=5, sticky="e")
        self.import_option = ttk.Combobox(self.window, values=["з форми", "з csv"], width=37, justify="center")
        self.import_option.set("з форми")
        self.import_option.grid(row=6, column=1, pady=5, sticky="ew")

        # кнопки для дій
        self.create_button(7, "Створення", self.create_client)
        self.create_button(8, "Пошук", self.search_client)
        self.create_button(9, "Видалення", self.delete_client)

        # Встановлення розміру колонок
        self.window.grid_columnconfigure(0, weight=1)  # Розтягуємо колонку для лейблів
        self.window.grid_columnconfigure(1, weight=1)  # Розтягуємо колонку з полями вводу
        self.window.grid_columnconfigure(2, weight=1)  # Розтягуємо колонку для кнопок

    def create_label_entry(self, row, label_text, entry_width=40, label_color=None, label_font=None):
        label = tk.Label(self.window, text=label_text, fg=label_color, font=label_font, bg="lightblue", anchor="e")
        label.grid(row=row, column=0, pady=5, sticky="e")
        entry = tk.Entry(self.window, width=entry_width)
        entry.grid(row=row, column=1, pady=5, sticky="ew")
        return label, entry

    def create_button(self, row, text, command):
        button = tk.Button(self.window, text=text, command=command, width=20, bg="white",
                           activebackground="lightgray", relief="flat", bd=2, highlightthickness=0,
                           font=("Arial", 10, "bold"), pady=5)
        button.grid(row=row, column=0, pady=5, padx=5, sticky="ew")
        return button

    def calculate_age(self, event=None):
        """вік"""
        birth_date_text = self.birth_date_entry.get()
        death_date_text = self.death_date_entry.get()  # отримуємо дату смерті

        # Обробляємо дату народження
        birth_date = process_date(birth_date_text)
        if not birth_date:
            self.age_value_label.config(text="-")
            return  # якщо дата народження невірна, не обчислюємо вік

        birth_date = datetime.strptime(birth_date, "%d.%m.%Y")

        # Якщо дата смерті є, то використовуємо її для розрахунку віку
        if death_date_text:
            death_date = process_date(death_date_text)
            if not death_date:
                self.age_value_label.config(text="-")
                return  # якщо дата смерті невірна, не обчислюємо вік
            death_date = datetime.strptime(death_date, "%d.%m.%Y")
            # Вік на дату смерті
            age = death_date.year - birth_date.year - (
                    (death_date.month, death_date.day) < (birth_date.month, birth_date.day))
        else:
            # Якщо дати смерті немає, обчислюємо вік на поточний день
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        self.age_value_label.config(text=str(age))

    def remember_client(self):
        """Запам'ятовуємо дані клієнта з форми"""
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        gender = self.gender_combobox.get()
        birth_date = self.birth_date_entry.get()
        death_date = self.death_date_entry.get()

        self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

    def create_client(self):
        # створення клієнта в бд + перевірка на обов'язкові поля
        missing_fields = []

        # Перевірка обов'язкових полів (все, крім "Дата смерті")
        if not self.last_name_entry.get():
            missing_fields.append(self.last_name_entry)
            self.last_name_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.last_name_entry.config(highlightbackground="lightblue",
                                        highlightthickness=1)  # Відновлюємо нормальний стиль

        if not self.first_name_entry.get():
            missing_fields.append(self.first_name_entry)
            self.first_name_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.first_name_entry.config(highlightbackground="lightblue", highlightthickness=1)

        if not self.middle_name_entry.get():
            missing_fields.append(self.middle_name_entry)
            self.middle_name_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.middle_name_entry.config(highlightbackground="lightblue", highlightthickness=1)

        if not self.gender_combobox.get():
            missing_fields.append(self.gender_combobox)
            self.gender_combobox.config(highlightbackground="red", highlightthickness=2)
        else:
            self.gender_combobox.config(highlightbackground="lightblue", highlightthickness=1)

        if not self.birth_date_entry.get():
            missing_fields.append(self.birth_date_entry)
            self.birth_date_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.birth_date_entry.config(highlightbackground="lightblue", highlightthickness=1)

        # Якщо є незаповнені обов'язкові поля
        if missing_fields:
            print("Будь ласка, заповніть всі обов'язкові поля!")
            return  # Якщо є незаповнені поля, зупиняємо виконання методу

        # Якщо всі обов'язкові поля заповнені, запам'ятовуємо клієнта
        self.remember_client()

        # Додаємо клієнта в базу даних
        self.client.add_one_client(self.db_file, self.table_name)

        print(f"Створено клієнта: {self.client}")

    def search_client(self):
        # Спочатку запам'ятовуємо дані клієнта з форми
        self.remember_client()

        # Шукаємо клієнта в базі даних за допомогою методу find_clients
        clients = self.client.find_clients(self.db_file, self.table_name, export_to_csv=False)

        # Якщо клієнтів знайдено, створюємо нове вікно для відображення результатів
        if clients:
            # Створюємо нове вікно для результатів пошуку
            result_window = tk.Toplevel(self.window)
            result_window.title("Знайдені клієнти")
            result_window.geometry("500x400")

            # Створюємо Text widget для відображення всіх клієнтів
            result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue", fg="#4B8BD4",
                                  font=("Arial", 10))
            result_text.pack(padx=10, pady=10)

            # Для кожного знайденого клієнта додаємо інформацію в текстове поле
            for client_id, client in clients.items():
                # Обчислюємо вік клієнта
                birth_date = datetime.strptime(client.birth_date, "%d.%m.%Y")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

                # Форматуємо текст для кожного клієнта
                client_text = f"{client.first_name} {client.last_name} {client.middle_name} - {age} років\n" \
                              f"Стать: {client.gender}\n" \
                              f"Дата народження: {client.birth_date}\n" \
                              f"Дата смерті: {client.death_date}\n\n"

                result_text.insert(tk.END, client_text)

            # Додаємо кнопку для закриття вікна
            close_button = tk.Button(result_window, text="Закрити", command=result_window.destroy)
            close_button.pack(pady=5)

        else:
            print("Клієнт не знайдений!")

    def delete_client(self):
        # Запам'ятовуємо клієнта та шукаємо його в базі
        self.remember_client()
        clients = self.client.find_clients(self.db_file, self.table_name)

        # Якщо клієнта знайдено, видаляємо його
        if clients:
            self.client.delete_one_client(self.db_file, self.table_name)
            print(f"Клієнта {self.client.last_name} {self.client.first_name} видалено!")
        else:
            print("Клієнт не знайдений!")

    def center_window(self, width, height):
        """Центрує вікно на екрані"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')


# Запуск програми
form = Form()
form.window.mainloop()















