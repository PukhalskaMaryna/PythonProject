import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageTk
from DIPLOMA.db import DB
from DIPLOMA.tras_date import process_date
from DIPLOMA.client import Client

class Form:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Дипломна робота")
        self.window.geometry("600x400")

        # Ініціалізація полів вводу
        self.last_name_entry = tk.Entry(self.window)
        self.first_name_entry = tk.Entry(self.window)
        self.middle_name_entry = tk.Entry(self.window)
        self.birth_date_entry = tk.Entry(self.window)
        self.death_date_entry = tk.Entry(self.window)
        self.gender_combobox = tk.Combobox(self.window, values=["Чоловік", "Жінка", "Інше"])

        # Розміщення елементів на формі
        self.last_name_entry.grid(row=0, column=1)
        self.first_name_entry.grid(row=1, column=1)
        self.middle_name_entry.grid(row=2, column=1)
        self.birth_date_entry.grid(row=3, column=1)
        self.death_date_entry.grid(row=4, column=1)
        self.gender_combobox.grid(row=5, column=1)

        # Створення кнопок
        self.create_button_with_image(self.create_client, image_path='create.png', button_frame=self.top_frame)
        self.create_button_with_image(self.search_client, image_path='find.png', button_frame=self.top_frame)
        self.create_button_with_image(self.delete_client, image_path='delete.png', button_frame=self.top_frame)

    def create_button_with_image(self, command, image_path, button_frame):
        # Створення кнопки з зображенням
        button_image = tk.PhotoImage(file=image_path)
        button = tk.Button(button_frame, image=button_image, command=command)
        button.image = button_image
        button.grid(row=0, column=0)

def remember_client(self):
    """створює Клієнта з даних форми"""
    # Перевірка, чи всі поля створено
    if not all([self.last_name_entry, self.first_name_entry, self.middle_name_entry, self.birth_date_entry]):
        print("Не всі поля ініціалізовані!")
        return

    last_name = self.last_name_entry.get()
    first_name = self.first_name_entry.get()
    middle_name = self.middle_name_entry.get()

    # Перевірка на комбо-бокс
    gender = self.gender_combobox.get() if self.gender_combobox else ""

    birth_date = self.birth_date_entry.get()
    birth_date = process_date(birth_date) if birth_date else None
    death_date = self.death_date_entry.get()
    death_date = process_date(death_date) if death_date else None

    if not birth_date:  # Якщо дата народження не заповнена або неправильна
        print("Невірна або відсутня дата народження!")
        return

    self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

def create_client(self):
    # Перевірка заповнених обов'язкових полів
    missing_fields = []

    if not self.last_name_entry.get():
        missing_fields.append(self.last_name_entry)
        self.last_name_entry.config(highlightbackground="red", highlightthickness=2)
    else:
        self.last_name_entry.config(highlightbackground="lightblue", highlightthickness=1)

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
        self.gender_combobox.config(background="red")
    else:
        self.gender_combobox.config(background="white")

    if not self.birth_date_entry.get():
        missing_fields.append(self.birth_date_entry)
        self.birth_date_entry.config(highlightbackground="red", highlightthickness=2)
    else:
        self.birth_date_entry.config(highlightbackground="lightblue", highlightthickness=1)

    # Якщо є незаповнені обов'язкові поля, не продовжуємо
    if missing_fields:
        return

    # Запам'ятовуємо клієнта
    self.remember_client()
    print(self.client)
    # Додаємо клієнта у БД
    self.client.add_one_client(self.db, self.table_name)

    # Вікно про успішне створення клієнта
    success_window = tk.Toplevel(self.window)
    success_window.title("Новий клієнт")
    success_window.geometry("300x150")
    success_label = tk.Label(success_window, text="Успішно створено клієнта!", font=self.label_font, fg=self.fg_label_color, bg="lightblue")
    success_label.pack(padx=20, pady=20)
    close_button = tk.Button(success_window, text="Закрити", command=success_window.destroy, width=15, bg="white", activebackground="lightgray", relief="flat", bd=2, highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
    close_button.pack(pady=10)
    self.update_client_count()
    self.clear_entries()

def search_client(self):
    if not self.client:
        print("Клієнт не був створений!")
        return

    self.remember_client()
    clients = self.client.find_clients(self.db, self.table_name, export_to_csv=True)

    # Вікно для результатів пошуку
    result_window = tk.Toplevel(self.window)
    result_window.title("Знайдені клієнти")
    result_window.geometry("500x300")
    result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue", fg="#4B8BD4", font=("Arial", 10))
    result_text.pack(padx=10, pady=10)
    close_button = tk.Button(result_window, text="Закрити", command=result_window.destroy)
    close_button.pack(pady=5)

    # Якщо клієнтів знайдено
    if clients:
        # Додаємо інформацію в текстове поле
        for client_id, client in clients.items():
            birth_date = datetime.strptime(client.birth_date, "%d.%m.%Y")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            client_text = f"{client.last_name} {client.first_name} {client.middle_name} - {age} р.\n" \
                          f"Стать: {client.gender}\n" \
                          f"Дата народження: {client.birth_date}\n" \
                          f"Дата смерті: {client.death_date}\n\n"

            result_text.insert(tk.END, client_text)
    else:
        result_text.insert(tk.END, 'Не знайдено!')

    self.clear_entries()

def delete_client(self):
    self.remember_client()
    clients = self.client.find_clients(self.db, self.table_name, export_to_csv=False)

    # Вікно для результатів пошуку
    result_window = tk.Toplevel(self.window)
    result_window.title("Видалені клієнти")
    result_window.geometry("500x400")
    result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue", fg="#4B8BD4", font=("Arial", 10))
    result_text.pack(padx=10, pady=10)
    close_button = tk.Button(result_window, text="Закрити", command=result_window.destroy)
    close_button.pack(pady=5)

    if clients:
        self.client.delete_client(self.db, self.table_name)
        result_text.insert(tk.END, f"Видалено!")
        self.clear_entries()
        self.update_client_count()
    else:
        result_text.insert(tk.END, f"Клієнта для видалення не знайдено!")
