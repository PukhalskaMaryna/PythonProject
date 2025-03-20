import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
import os
from datetime import datetime
import re

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

        # Лейбли та поля вводу
        label_font = ("Arial", 11, "bold")
        label_color = "#4B8BD4"  # приємний синій колір

        # Лейбли (вирівняні по правому краю, з новим кольором)
        self.last_name_label = tk.Label(self.window, fg=label_color, text="Прізвище:", font=label_font, bg="lightblue",
                                        anchor="e")
        self.last_name_label.grid(row=0, column=0, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(self.window, width=40)
        self.last_name_entry.grid(row=0, column=1, pady=5, sticky="ew")

        self.first_name_label = tk.Label(self.window, text="Ім'я:", fg=label_color, font=label_font, bg="lightblue",
                                         anchor="e")
        self.first_name_label.grid(row=1, column=0, pady=5, sticky="e")
        self.first_name_entry = tk.Entry(self.window, width=40)
        self.first_name_entry.grid(row=1, column=1, pady=5, sticky="ew")

        self.middle_name_label = tk.Label(self.window, text="По батькові:", fg=label_color, font=label_font,
                                          bg="lightblue", anchor="e")
        self.middle_name_label.grid(row=2, column=0, pady=5, sticky="e")
        self.middle_name_entry = tk.Entry(self.window, width=40)
        self.middle_name_entry.grid(row=2, column=1, pady=5, sticky="ew")

        self.gender_label = tk.Label(self.window, text="Стать:", fg=label_color, font=label_font, bg="lightblue",
                                     anchor="e")
        self.gender_label.grid(row=3, column=0, pady=5, sticky="e")
        self.gender_entry = tk.Entry(self.window, width=40)
        self.gender_entry.grid(row=3, column=1, pady=5, sticky="ew")

        # Зменшити ширину для "Дати народження" та "Дати смерті" до 10
        self.birth_date_label = tk.Label(self.window, text="Дата народження:", fg=label_color, font=label_font,
                                         bg="lightblue", anchor="e")
        self.birth_date_label.grid(row=4, column=0, pady=5, sticky="e")
        self.birth_date_entry = tk.Entry(self.window, width=10)
        self.birth_date_entry.grid(row=4, column=1, pady=5, sticky="ew")
        self.birth_date_entry.bind("<KeyRelease>", self.calculate_age)  # Оновлюємо вік при введенні дати народження

        self.age_label = tk.Label(self.window, text="Вік:", fg=label_color, font=label_font, bg="lightblue", anchor="e")
        self.age_label.grid(row=4, column=2, pady=5, sticky="e")
        self.age_value_label = tk.Label(self.window, text="0", fg=label_color, font=label_font, bg="lightblue")
        self.age_value_label.grid(row=4, column=3, pady=5, sticky="w")

        self.death_date_label = tk.Label(self.window, text="Дата смерті:", fg=label_color, font=label_font,
                                         bg="lightblue", anchor="e")
        self.death_date_label.grid(row=5, column=0, pady=5, sticky="e")
        self.death_date_entry = tk.Entry(self.window, width=10)
        self.death_date_entry.grid(row=5, column=1, pady=5, sticky="ew")
        self.death_date_entry.bind("<KeyRelease>", self.calculate_age)  # Оновлюємо вік при введенні дати смерті

        # Списочок
        self.import_option_label = tk.Label(self.window, text="Імпорт з:", fg=label_color, font=label_font,
                                            bg="lightblue", anchor="e")
        self.import_option_label.grid(row=6, column=0, pady=5, sticky="e")
        self.import_option = ttk.Combobox(self.window, values=["з форми", "з csv"], width=37, justify="center")
        self.import_option.set("з форми")  # Встановити значення за замовчуванням
        self.import_option.grid(row=6, column=1, pady=5, sticky="ew")

        # Кнопки
        self.create_button = tk.Button(self.window, text="Створення", command=self.create_client, width=20, bg="white",
                                       activebackground="lightgray", relief="flat", bd=2, highlightthickness=0,
                                       font=("Arial", 10, "bold"), pady=5)
        self.create_button.grid(row=7, column=0, pady=5, padx=5, sticky="ew")

        self.search_button = tk.Button(self.window, text="Пошук", command=self.search_client, width=20, bg="white",
                                       activebackground="lightgray", relief="flat", bd=2, highlightthickness=0,
                                       font=("Arial", 10, "bold"), pady=5)
        self.search_button.grid(row=7, column=1, pady=5, padx=5, sticky="ew")

        self.delete_button = tk.Button(self.window, text="Видалення", command=self.delete_client, width=20, bg="white",
                                       activebackground="lightgray", relief="flat", bd=2, highlightthickness=0,
                                       font=("Arial", 10, "bold"), pady=5)
        self.delete_button.grid(row=7, column=2, pady=5, padx=5, sticky="ew")

        # Встановлення розміру колонок
        self.window.grid_columnconfigure(0, weight=1)  # Розтягуємо колонку для лейблів
        self.window.grid_columnconfigure(1, weight=1)  # Розтягуємо колонку з полями вводу
        self.window.grid_columnconfigure(2, weight=1)  # Розтягуємо колонку для кнопок

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

    def center_window(self, width, height):
        """відцентровка віконечка"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def remember_client(self):
        # Запам'ятовуємо дані клієнта з форми
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        gender = self.gender_entry.get()
        birth_date = self.birth_date_entry.get()
        death_date = self.death_date_entry.get()
        self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

    def create_client(self):
        self.remember_client()
        print(f"Створено клієнта: {self.client}")

    def search_client(self):
        # Пошук клієнтів
        print("Пошук клієнта...")

    def delete_client(self):
        # Видалення клієнта
        print("Видалення клієнта...")

    def run(self):
        self.window.mainloop()


# Запуск форми
form = Form()
form.run()














