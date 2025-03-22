import tkinter as tk
from tkinter import ttk,messagebox
import os
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageTk
from DIPLOMA.db import DB
from DIPLOMA.tras_date import process_date
from DIPLOMA.client import Client

class Form:
    def __init__(self, db_file='db.db', table_name='clients'):
        """
        Формочка для створення клієнтів.

        :param db_file: Str, назва файлу бази даних (за замовчуванням db.db)
        :param table_name: Str, назва таблиці, до якої будемо записувати/видаляти дані (за замовчуванням 'clients')
        """

        self.file_name_entry = None
        self.db_file = db_file
        self.table_name = table_name
        self.client = None  # потенційний клієнт
        self.db = DB(db_file)
        self.db.open_connection()

        # стилі для лейблів
        self.label_font = ("Arial", 11, "bold")
        self.label_color = "blue"
        self.window_bg_color = "lightblue"

        # основне вікно
        self.window = tk.Tk()
        self.window.title("Тут ви можете працювати з клієнтськими даними")
        self.center_window(600, 400)  # Збільшили висоту вікна
        self.window.config(bg=self.window_bg_color)

        # панель для кнопок у верхній частині
        # self.top_frame = tk.Frame(self.window, bg="lightgray")
        # self.top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=5)

        # лейблики та поля вводу
        self.client_count_label = tk.Label(self.window, text="Кількість клієнтів в бд:", fg=self.label_color,
                                           font=self.label_font, bg=self.window_bg_color, anchor="e")
        self.client_count_label.grid(row=1, column=0, pady=5, sticky="e")

        self.client_count_value_label = tk.Label(self.window, text="0", fg=self.label_color, font=self.label_font,
                                                 bg=self.window_bg_color)
        self.client_count_value_label.grid(row=1, column=1, pady=5, sticky="w")

        self.last_name_label = tk.Label(self.window, text="Прізвище:", fg=self.label_color, font=self.label_font,
                                        bg=self.window_bg_color, anchor="e")
        self.last_name_label.grid(row=2, column=0, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(self.window, width=40)
        self.last_name_entry.grid(row=2, column=1, pady=5, sticky="ew")

        self.first_name_label = tk.Label(self.window, text="Ім'я:", fg=self.label_color, font=self.label_font,
                                         bg=self.window_bg_color, anchor="e")
        self.first_name_label.grid(row=3, column=0, pady=5, sticky="e")
        self.first_name_entry = tk.Entry(self.window, width=40)
        self.first_name_entry.grid(row=3, column=1, pady=5, sticky="ew")

        self.middle_name_label = tk.Label(self.window, text="По батькові:", fg=self.label_color, font=self.label_font,
                                          bg=self.window_bg_color, anchor="e")
        self.middle_name_label.grid(row=4, column=0, pady=5, sticky="e")
        self.middle_name_entry = tk.Entry(self.window, width=40)
        self.middle_name_entry.grid(row=4, column=1, pady=5, sticky="ew")

        self.gender_label = tk.Label(self.window, text="Стать:", fg=self.label_color, font=self.label_font,
                                     bg=self.window_bg_color, anchor="e")
        self.gender_label.grid(row=5, column=0, pady=5, sticky="e")
        self.gender_combobox = ttk.Combobox(self.window, background="white", values=["чоловік", "жінка", ""], width=40, state="readonly")
        self.gender_combobox.set("")  # Завжди встановлюється значення за замовчуванням
        self.gender_combobox.grid(row=5, column=1, pady=5, sticky="ew")

        self.birth_date_label = tk.Label(self.window, text="Дата народження:", fg=self.label_color,
                                         font=self.label_font, bg=self.window_bg_color, anchor="e")
        self.birth_date_label.grid(row=6, column=0, pady=5, sticky="e")
        self.birth_date_entry = tk.Entry(self.window, width=10)
        self.birth_date_entry.grid(row=6, column=1, pady=5, sticky="ew")

        # При зміні дати народження автоматично оновлюємо вік
        self.birth_date_entry.bind("<KeyRelease>", self.calculate_age)

        self.death_date_label = tk.Label(self.window, text="Дата смерті:", fg=self.label_color, font=self.label_font,
                                         bg=self.window_bg_color, anchor="e")
        self.death_date_label.grid(row=7, column=0, pady=5, sticky="e")
        self.death_date_entry = tk.Entry(self.window, width=10)
        self.death_date_entry.grid(row=7, column=1, pady=5, sticky="ew")

        # При зміні дати смерті також оновлюємо вік
        self.death_date_entry.bind("<KeyRelease>", self.calculate_age)

        self.age_label = tk.Label(self.window, text="Вік:", fg=self.label_color, font=self.label_font,
                                  bg=self.window_bg_color, anchor="e")
        self.age_label.grid(row=8, column=2, pady=5, sticky="e")
        self.age_value_label = tk.Label(self.window, text="0", fg=self.label_color, font=self.label_font,
                                        bg=self.window_bg_color)
        self.age_value_label.grid(row=8, column=3, pady=5, sticky="w")

        # Переміщаємо import_option напроти кнопки "Створити" (рядок 9)
        self.import_option = ttk.Combobox(self.window, values=["з форми", "з csv"], width=37, justify="center")
        self.import_option.set("з форми")
        self.import_option.grid(row=9, column=1, pady=5, sticky="ew")

        # Кнопки
        self.submit_button = tk.Button(self.window, text="Створити", command=self.create_client, width=20,
                                       bg="white", activebackground="lightgray", relief="flat", bd=2,
                                       highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.submit_button.grid(row=9, column=0, pady=5, padx=5, sticky="ew")
        self.search_button = tk.Button(self.window, text="Знайти", command=self.search_client, width=20,
                                       bg="white", activebackground="lightgray", relief="flat", bd=2,
                                       highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.search_button.grid(row=10, column=0, pady=5, padx=5, sticky="ew")

        self.delete_button = tk.Button(self.window, text="Видалити", command=self.delete_client, width=20,
                                       bg="white", activebackground="lightgray", relief="flat", bd=2,
                                       highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.delete_button.grid(row=10, column=1, pady=5, padx=5, sticky="ew")
        # просто for fun :)
        self.auto_fun_button = tk.Button(self.window, text="Отримати щастя :)", width=15, command=self.create_smiley_window,
                                         bg="#FFFFCC", activebackground="#FFFFCC", relief="flat", bd=2,
                                         highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.auto_fun_button.grid(row=0, column=0, padx=5)
        # рандомне автозаповнення
        self.auto_fill_button = tk.Button(self.window, text="Автозаповнення", command=self.auto_fill, width=15,
                                          bg="white", activebackground="lightgray", relief="flat", bd=2,
                                          highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.auto_fill_button.grid(row=0, column=1, padx=5)
        # чистка форми
        self.clear_button = tk.Button(self.window, text="Очистка", command=self.clear_entries, width=15,
                                          bg="white", activebackground="lightgray", relief="flat", bd=2,
                                          highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        # при закритті форми закриваємо коннекшн
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_client_count()

        self.window.mainloop()

    def auto_fill(self):
        """автозаповнення"""
        last_names = ["Іваненко", "Петренко", "Коваленко", "Сидоренко", "Мельник"]
        first_names = ["Іван", "Олександр", "Марія", "Наталія", "Андрій"]
        middle_names = ["Іванович", "Олександрович", "Миколаївна", "Ігорівна", "Петрівна"]
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, random.choice(last_names))
        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, random.choice(first_names))
        self.middle_name_entry.delete(0, tk.END)
        self.middle_name_entry.insert(0, random.choice(middle_names))
        gender = random.choice(["чоловік", "жінка"])
        self.gender_combobox.set(gender)
        birth_dates = [
            "15.03.1985", "01.02.1990", "25.08.1975", "10.11.1980", "30.12.1970",
            "22.04.1965", "17.06.1958", "05.07.1995"
        ]
        death_dates = [
            "25.12.2020", "15.06.2022", "10.03.2019", "30.01.2021", "05.09.2023",
            "18.08.2022", "01.01.2018", "12.07.2021"
        ]
        birth_date = random.choice(birth_dates)
        self.birth_date_entry.delete(0, tk.END)
        self.birth_date_entry.insert(0, birth_date)
        death_date = random.choice(death_dates)
        self.death_date_entry.delete(0, tk.END)
        self.death_date_entry.insert(0, death_date)
        self.calculate_age() # перерахунок віку

    def on_close(self):
        """при закритті вікна закривається і з'єднання до бд"""
        self.db.close_connection()  # Закриваємо підключення до БД
        self.window.destroy()  # Закриваємо вікно

    def count_rows(self):
        """кількості клієнтів в бд"""
        return self.db.count_rows(self.table_name)

    def update_client_count(self):
        """Оновлює кількість клієнтів в базі даних та відображає на формі"""
        client_count = self.count_rows()
        self.client_count_value_label.config(text=str(client_count))

    def calculate_age(self, event=None):
        """вік"""
        birth_date_text = self.birth_date_entry.get()
        death_date_text = self.death_date_entry.get()  # отримуємо дату смерті

        # обробка ДН
        birth_date = process_date(birth_date_text)
        if not birth_date:
            self.age_value_label.config(text="-")
            return  # якщо дата народження невірна, не обчислюємо вік

        birth_date = datetime.strptime(birth_date, "%d.%m.%Y")

        # якщо є ДС
        if death_date_text:
            death_date = process_date(death_date_text)
            if not death_date:
                self.age_value_label.config(text="-")
                return  # якщо дата смерті невірна, не обчислюємо вік
            death_date = datetime.strptime(death_date, "%d.%m.%Y")
            age = death_date.year - birth_date.year - (
                        (death_date.month, death_date.day) < (birth_date.month, birth_date.day))
        else:
            # якщо ДС немає
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        self.age_value_label.config(text=str(age))

    def remember_client(self):
        """створює Клієнта з даних форми"""
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        gender = self.gender_combobox.get()
        birth_date = self.birth_date_entry.get()
        death_date = self.death_date_entry.get()

        self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

    def create_client(self):
        # якщо вибрано "з форми"
        if self.import_option.get() == "з форми":
            # створення клієнта в бд + перевірка на обов'язкові поля
            missing_fields = []

            # поле дата смерті не є обов'язковим
            if not self.last_name_entry.get():
                missing_fields.append(self.last_name_entry)
                self.last_name_entry.config(highlightbackground="red", highlightthickness=2)
            else:
                self.last_name_entry.config(highlightbackground="lightblue",
                                            highlightthickness=1)

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

            # Якщо є незаповнені обов'язкові поля
            if missing_fields:
                return

            # запам'ятовуємо клієнта
            self.remember_client()
            print(self.client)
            # додаємо клієнта у бд
            self.client.add_one_client(self.db, self.table_name)

            # повідомленням про успішне створення клієнта
            success_window = tk.Toplevel(self.window)
            success_window.title("Новий клієнт")
            success_window.geometry("300x150")
            window_width = 300
            window_height = 150
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            success_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
            success_label = tk.Label(success_window, text="Успішно створено клієнта!", font=self.label_font,
                                     fg=self.label_color, bg="lightblue")
            success_label.pack(padx=20, pady=20)
            close_button = tk.Button(success_window, text="Закрити", command=success_window.destroy, width=15,
                                     bg="white", activebackground="lightgray", relief="flat", bd=2,
                                     highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
            close_button.pack(pady=10)
            self.update_client_count()
            self.clear_entries()

        # якщо вибрано "з csv"
        # elif self.import_option.get() == "з csv":
        #     # відкриваємо вікно для введення назви файлу
        #     def import_from_csv():
        #         my_file_name = self.file_name_entry.get()  # отримуємо введену назву файлу
        #         Client.add_client_from_csv(self.db, self.table_name,my_file_name)  # викликаємо метод для імпорту
        #
        #         # повідомленням про успішний імпорт
        #         success_window2 = tk.Toplevel(self.window)
        #         success_window2.title("Імпорт з CSV")
        #         success_window2.geometry("300x150")
        #
        #         # Для того, щоб вікно було по центру екрана:
        #         window_width2 = 300
        #         window_height2 = 150
        #         screen_width2 = self.window.winfo_screenwidth()
        #         screen_height2 = self.window.winfo_screenheight()
        #         position_top2 = int(screen_height2 / 2 - window_height2 / 2)
        #         position_right2 = int(screen_width2 / 2 - window_width2 / 2)
        #         success_window2.geometry(f"{window_width2}x{window_height2}+{position_right2}+{position_top2}")
        #
        #         success_label2 = tk.Label(success_window2, text="Успішно імпортовано клієнтів!", font=self.label_font,
        #                                   fg=self.label_color, bg="lightblue")
        #         success_label2.pack(padx=20, pady=20)
        #         close_button2 = tk.Button(success_window2, text="Закрити", command=success_window2.destroy, width=15,
        #                                   bg="white", activebackground="lightgray", relief="flat", bd=2,
        #                                   highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
        #         close_button2.pack(pady=10)
        #         self.clear_entries()
        #         self.update_client_count()
        #
        #     # створюємо нове вікно для введення назви файлу
        #     file_window = tk.Toplevel(self.window)
        #     file_window.title("Вибір файлу для імпорту")
        #     file_window.geometry("400x150")
        #
        #     # лейбл для поля вводу назви файлу
        #     file_label = tk.Label(file_window, text="Введіть назву файлу:", font=self.label_font,
        #                           fg=self.label_color, bg="lightblue")
        #     file_label.pack(padx=10, pady=10)
        #
        #     # поле вводу для назви файлу, за замовчуванням "import_clients.csv"
        #     self.file_name_entry = tk.Entry(file_window, width=40)
        #     self.file_name_entry.insert(0, "import_clients.csv")  # значення за замовчуванням
        #     self.file_name_entry.pack(padx=10, pady=5)
        #
        #     # кнопка для підтвердження імпорту
        #     import_button = tk.Button(file_window, text="Імпортувати", command=import_from_csv,
        #                               width=20, bg="white", activebackground="lightgray",
        #                               relief="flat", bd=2, highlightthickness=0,
        #                               font=("Arial", 10, "bold"), pady=5)
        #     import_button.pack(pady=10)
        elif self.import_option.get() == "з csv":
            # відкриваємо вікно для введення назви файлу
            def import_from_csv():
                my_file_name = self.file_name_entry.get()  # отримуємо введену назву файлу

                # чи існує файл
                if not os.path.isfile(my_file_name):
                    messagebox.showerror("Помилка", "Файл не знайдено!")
                    return  # Зупиняємо подальше виконання, якщо файл не знайдений

                Client.add_client_from_csv(self.db, self.table_name, my_file_name)  # викликаємо метод для імпорту

                # повідомленням про успішний імпорт
                success_window2 = tk.Toplevel(self.window)
                success_window2.title("Імпорт з CSV")
                success_window2.geometry("300x150")

                # Для того, щоб вікно було по центру екрана:
                window_width2 = 300
                window_height2 = 150
                screen_width2 = self.window.winfo_screenwidth()
                screen_height2 = self.window.winfo_screenheight()
                position_top2 = int(screen_height2 / 2 - window_height2 / 2)
                position_right2 = int(screen_width2 / 2 - window_width2 / 2)
                success_window2.geometry(f"{window_width2}x{window_height2}+{position_right2}+{position_top2}")

                success_label2 = tk.Label(success_window2, text="Успішно імпортовано клієнтів!", font=self.label_font,
                                          fg=self.label_color, bg="lightblue")
                success_label2.pack(padx=20, pady=20)
                close_button2 = tk.Button(success_window2, text="Закрити", command=success_window2.destroy, width=15,
                                          bg="white", activebackground="lightgray", relief="flat", bd=2,
                                          highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
                close_button2.pack(pady=10)
                self.clear_entries()
                self.update_client_count()

            # створюємо нове вікно для введення назви файлу
            file_window = tk.Toplevel(self.window)
            file_window.title("Вибір файлу для імпорту")
            file_window.geometry("400x150")

            # лейбл для поля вводу назви файлу
            file_label = tk.Label(file_window, text="Введіть назву файлу:", font=self.label_font,
                                  fg=self.label_color, bg="lightblue")
            file_label.pack(padx=10, pady=10)

            # поле вводу для назви файлу, за замовчуванням "import_clients.csv"
            self.file_name_entry = tk.Entry(file_window, width=40)
            self.file_name_entry.insert(0, "import_clients.csv")  # значення за замовчуванням
            self.file_name_entry.pack(padx=10, pady=5)

            # кнопка для підтвердження імпорту
            import_button = tk.Button(file_window, text="Імпортувати", command=import_from_csv,
                                      width=20, bg="white", activebackground="lightgray",
                                      relief="flat", bd=2, highlightthickness=0,
                                      font=("Arial", 10, "bold"), pady=5)
            import_button.pack(pady=10)

    def search_client(self):
        self.remember_client()
        clients = self.client.find_clients(self.db, self.table_name,export_to_csv = True)
        # Вікно для результатів пошуку
        result_window = tk.Toplevel(self.window)
        result_window.title("Знайдені клієнти")
        result_window.geometry("500x300")
        result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue", fg="#4B8BD4",
                              font=("Arial", 10))
        result_text.pack(padx=10, pady=10)
        close_button = tk.Button(result_window, text="Закрити", command=result_window.destroy)
        close_button.pack(pady=5)

        # Якщо клієнтів знайдено
        if clients:
            # Додаємо інформацію в текстове поле
            for client_id, client in clients.items():
                # Обчислюємо вік клієнта
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
        clients = self.client.find_clients(self.db, self.table_name,export_to_csv = False)
        # вікно для результатів пошуку
        result_window = tk.Toplevel(self.window)
        result_window.title("Видалені клієнти")
        result_window.geometry("500x400")
        result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue",
                              fg="#4B8BD4", font=("Arial", 10))
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

    def center_window(self, width, height):
        """центрує вікно на екрані"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def clear_entries(self):
        """чистка форми"""
        self.last_name_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.birth_date_entry.delete(0, tk.END)
        self.death_date_entry.delete(0, tk.END)
        self.age_value_label.config(text="0")  # Очищаємо вік, якщо потрібно
        self.gender_combobox.set("")  # Встановлюємо значення за замовчуванням для комбобоксу

    @staticmethod
    def create_smiley_window():
        # Створюємо зображення для смайлика
        image = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(image)

        # Малюємо круг для обличчя смайлика
        draw.ellipse((50, 50, 250, 250), fill="yellow", outline="black", width=5)

        # Малюємо очі
        draw.ellipse((100, 100, 140, 140), fill="black")  # Ліве око
        draw.ellipse((160, 100, 200, 140), fill="black")  # Праве око

        # Малюємо посмішку (використовуємо arc для півкола)
        draw.arc((100, 150, 200, 230), start=0, end=180, fill="black", width=5)

        # Малюємо рожеві щічки
        draw.ellipse((70, 170, 110, 210), fill="pink")  # Ліва щічка
        draw.ellipse((190, 170, 230, 210), fill="pink")  # Права щічка

        # Потрібно конвертувати Image в формат, який Tkinter може відображати
        tk_image = ImageTk.PhotoImage(image)

        # Створюємо нове вікно для відображення смайлика
        smiley_window = tk.Toplevel()
        smiley_window.title("Смайлик")
        smiley_window.geometry("300x300")

        # Додаємо смайлик до вікна
        label = tk.Label(smiley_window, image=tk_image)
        label.pack()

        # Додаємо метод закриття вікна при натисканні кнопки
        def close_window():
            smiley_window.destroy()

        close_button = tk.Button(smiley_window, text="Закрити", command=close_window)
        close_button.pack(pady=10)

        # Необхідно зберігати об'єкт ImageTk, інакше він не буде відображатися
        label.image = tk_image