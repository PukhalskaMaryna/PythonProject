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
    def __init__(self, db_file='db.db', table_name='clients'):
        """
        Формочка для створення клієнтів
        """

        self.db_file = db_file
        self.table_name = table_name
        self.db = DB(db_file)
        self.db.open_connection()
        self.client = None  # потенційний клієнт

        # Стилі
        self.label_font = ("Segoe UI", 10)
        self.fg_label_color = "#FF69B4"
        self.bg_label_color = "#2F353B"
        self.button_bg_color = "#FF69B4"
        self.button_active_bg_color = "#357ABD"
        self.button_config_active_bg_color = "white"
        self.window_bg_color = "#2F353B"

        # основне вікно
        self.window = tk.Tk()
        # self.window.title(f"НАРАЗІ БД НАЛІЧУЄ: 0 кл.")
        self.update_client_count()
        self.center_window(500, 230)  # Збільшено розмір вікна
        self.window.config(bg=self.window_bg_color)
        self.import_option_form = tk.BooleanVar()  # checkbox
        self.import_option_csv = tk.BooleanVar()

        # ініціалізація елементів
        self.last_name_entry = None
        self.first_name_entry = None
        self.middle_name_entry = None
        self.gender_combobox = None
        self.birth_date_entry = None
        self.death_date_entry = None
        self.age_value_label = None

        # Фрейм для основного контенту
        main_frame = tk.Frame(self.window, bg=self.window_bg_color)
        main_frame.pack(pady=1, padx=1, fill="both", expand=True)

        # Верхній фрейм (можна використати для заголовка або інформації)
        top_frame = tk.Frame(main_frame, bg=self.window_bg_color)
        top_frame.pack(side="top", padx=1, fill="x", pady=1)
        top_frame_1 = tk.Frame(top_frame, bg=self.window_bg_color)
        top_frame_1.pack(side="left", padx=1)
        top_frame_2 = tk.Frame(top_frame, bg=self.window_bg_color)
        top_frame_2.pack(side="left", padx=1, fill="x", expand=True)
        top_frame_3 = tk.Frame(top_frame, bg=self.window_bg_color)
        top_frame_3.pack(side="right", padx=1)
        top_frame_4 = tk.Frame(top_frame, bg=self.window_bg_color)
        top_frame_4.pack(side="right", padx=1)

        # Лівий фрейм для лейблів і кнопок
        left_frame = tk.Frame(main_frame, bg=self.window_bg_color, width=300)
        left_frame.pack(side="left", padx=1, fill="y")

        # Правий фрейм для полів вводу та кнопок
        right_frame = tk.Frame(main_frame, bg=self.window_bg_color, width=300)
        right_frame.pack(side="right", padx=1, fill="both", expand=True)

        # Нижній фрейм (для додаткових кнопок або інших елементів)
        bottom_frame = tk.Frame(self.window, bg=self.window_bg_color)
        bottom_frame.pack(side="bottom", pady=1, fill="x")
        bottom_frame_1 = tk.Frame(bottom_frame, bg=self.window_bg_color)
        bottom_frame_1.pack(side="left", padx=60)
        bottom_frame_2 = tk.Frame(bottom_frame, bg=self.window_bg_color)
        bottom_frame_2.pack(side="right", padx=60, fill="x", expand=True)

        # Лейбли та поля лівого фрейму
        self.create_label_and_entry("Прізвище:", left_frame)
        self.create_label_and_entry("Ім'я:", left_frame)
        self.create_label_and_entry("По батькові:", left_frame)

        # Лейбли та поля правого фрейму
        self.create_combobox("Стать:", ["чоловік", "жінка", ""], right_frame)
        self.create_label_and_entry("Дата народження:", right_frame)
        self.create_label_and_entry("Дата смерті:", right_frame)
        self.create_label_and_entry("Вік:", right_frame)

        # Кнопки нижнього фрейму
        self.create_button_with_image(self.clear_entries, image_path='clear.png', button_frame=bottom_frame_1)
        self.create_button_with_image(self.auto_fill, image_path='auto.png', button_frame=bottom_frame_2)
        # Кнопки верхнього фрейму
        self.create_button_with_image(self.create_client, image_path='create.png', button_frame=top_frame_1)
        self.create_button_with_image(self.search_client, image_path='find.png', button_frame=top_frame_4)
        self.create_button_with_image(self.delete_client, image_path='delete.png', button_frame=top_frame_3)
        # чекбокси верхнього фрейму
        self.create_checkboxes(top_frame_2)
        # Завершення
        self.window.protocol("WM_DELETE_WINDOW", self.on_close())
        self.update_client_count()

        self.window.mainloop()

    def create_checkboxes(self, frame):
        # Функція для обробки зміни стану чекбоксу "із форми"
        def on_import_option_form_change():
            if self.import_option_form.get():
                self.import_option_csv.set(False)

        # Чекбокс "із форми"
        import_option_checkbox = tk.Checkbutton(
            frame, text="із форми", variable=self.import_option_form,
            bg="#2F353B", fg="#FF69B4", command=on_import_option_form_change,
            highlightthickness=0, bd=0, activebackground="#2F353B", activeforeground="#FF69B4"
        )
        import_option_checkbox.pack(side="top", padx=1, pady=1)  # Використовуємо "top" для вертикального розташування

        # Функція для обробки зміни стану чекбоксу "із файлу"
        def on_import_option_csv_change():
            if self.import_option_csv.get():
                self.import_option_form.set(False)

        # Чекбокс "із файлу"
        import_option_csv_checkbox = tk.Checkbutton(
            frame, text="із файлу", variable=self.import_option_csv,
            bg="#2F353B", fg="#FF69B4", command=on_import_option_csv_change,
            highlightthickness=0, bd=0, activebackground="#2F353B", activeforeground="#FF69B4"
        )
        import_option_csv_checkbox.pack(side="top", padx=1, pady=1)  # Розміщуємо другий чекбокс під першим

        # За замовчуванням вибрано "із форми"
        self.import_option_form.set(True)  # "із форми" за замовчуванням
        self.import_option_csv.set(False)  # "із файлу" не вибрано

    # def create_button_with_image(self, command, image_path, button_frame):
    #     """
    #     Створення кнопки з зображенням
    #     """
    #     # Завантажуємо зображення
    #     image = Image.open(image_path)  # Шлях до зображення
    #     image = image.resize((100, 40))  # Можна змінити розмір зображення
    #     self.photo = ImageTk.PhotoImage(image)  # Конвертуємо в формат Tkinter
    #
    #     # Створюємо кнопку з зображенням та порожнім текстом
    #     button = tk.Button(button_frame, image=self.photo, command=command, activebackground=self.window_bg_color,
    #                        bd=0, highlightthickness=0, pady=0, bg=self.window_bg_color)
    #
    #     # Додаємо кнопку на фрейм
    #     button.pack(padx=10, pady=10, fill="x")
    #
    #     # Зберігаємо зображення у властивості кнопки для запобігання знищення
    #     button.image = self.photo  # Зберігаємо, щоб зображення не було видалено

    def create_button_with_image(self, command, image_path, button_frame):
        """
        Створення кнопки з зображенням
        """
        # Завантажуємо зображення
        image = Image.open(image_path)  # Шлях до зображення
        image = image.resize((100, 40))  # Можна змінити розмір зображення
        photo = ImageTk.PhotoImage(image)  # Конвертуємо в формат Tkinter

        # Створюємо кнопку з зображенням та порожнім текстом
        button = tk.Button(button_frame, image=photo, command=command, activebackground=self.window_bg_color,
                           bd=0, highlightthickness=0, pady=0, bg=self.window_bg_color)

        # Додаємо кнопку на фрейм
        button.pack(padx=10, pady=10, fill="x")

        # Зберігаємо зображення у властивості кнопки для запобігання знищення
        button.image = photo  # Зберігаємо, щоб зображення не було видалено

    def create_label_and_entry(self, text, form_frame):
        # Створюємо окремий фрейм для кожної пари лейбл + поле вводу
        row_frame = tk.Frame(form_frame, bg=self.window_bg_color)
        row_frame.pack(pady=1, fill="x")

        # Лейбл
        label = tk.Label(row_frame, text=text, fg=self.fg_label_color, font=self.label_font,
                         bg=self.bg_label_color, anchor="w")
        label.pack(side="left", padx=1)

        # Поля
        if text == "Вік:":
            entry = tk.Label(row_frame, text="0", fg=self.fg_label_color, font=self.label_font,bg=self.window_bg_color)
            entry.pack(side="left", padx=10)
        else:
            entry = tk.Entry(row_frame, width=15, font=("Segoe UI", 12, "bold"))
            entry.pack(side="right", padx=1, fill="x")

        # Присвоюємо елементи як атрибути
        if text == "Прізвище:":
            self.last_name_entry = entry
        elif text == "Ім'я:":
            self.first_name_entry = entry
        elif text == "По батькові:":
            self.middle_name_entry = entry
        elif text == "Дата народження:":
            self.birth_date_entry = entry
        elif text == "Дата смерті:":
            self.death_date_entry = entry
        elif text == "Вік:":
            self.age_value_label = entry

    def create_combobox(self, text, values, form_frame):
        # Створюємо окремий фрейм для кожної пари лейбл + комбобокс
        row_frame = tk.Frame(form_frame, bg=self.window_bg_color)
        row_frame.pack(pady=1, fill="x")

        # Лейбл
        label = tk.Label(row_frame, text=text, fg=self.fg_label_color, font=self.label_font,
                         bg=self.window_bg_color, anchor="w")
        label.pack(side="left", padx=1)

        # Комбобокс
        combobox = ttk.Combobox(row_frame, values=values, width=17, state="readonly", font=("Segoe UI", 10))
        combobox.set("")  # default value
        combobox.pack(side="right", padx=1, fill="x")
        self.gender_combobox = combobox

    def center_window(self, width, height):
        """
        Центрує вікно на екрані
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def update_client_count(self):
        """
        Оновлює кількість клієнтів на титульному рядку
        """
        client_count = self.db.count_rows(self.table_name)
        self.window.title(f"НАРАЗІ БД НАЛІЧУЄ: {client_count} кл.")

    def on_close(self):
        """
        Закриття вікна
        """
        self.db.close_connection()
        self.window.quit()

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

    def count_rows(self):
        """кількості клієнтів в бд"""
        return self.db.count_rows(self.table_name)

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

        self.age_value_label = str(age)

    def remember_client(self):
        """створює Клієнта з даних форми"""
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()

        # Перевіряємо, чи комбобокс не є None
        if self.gender_combobox:
            gender = self.gender_combobox.get()
        else:
            gender = ""

        birth_date = self.birth_date_entry.get()
        birth_date = process_date(birth_date)
        death_date = self.death_date_entry.get()
        death_date = process_date(death_date)

        self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

    def create_client(self):
        # якщо вибрано "з форми"
        if self.import_option_form.get() == "з форми":
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
                                     fg=self.fg_label_color, bg="lightblue")
            success_label.pack(padx=20, pady=20)
            close_button = tk.Button(success_window, text="Закрити", command=success_window.destroy, width=15,
                                     bg="white", activebackground="lightgray", relief="flat", bd=2,
                                     highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
            close_button.pack(pady=10)
            self.update_client_count()
            self.clear_entries()

        elif self.import_option_csv.get() == "з csv":
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
                                          fg=self.fg_label_color, bg="lightblue")
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
                                  fg=self.fg_label_color, bg="lightblue")
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

    # def center_wind(self, width, height):
    #     """центрує вікно на екрані"""
    #     screen_width = self.window.winfo_screenwidth()
    #     screen_height = self.window.winfo_screenheight()
    #     position_top = int(screen_height / 2 - height / 2)
    #     position_right = int(screen_width / 2 - width / 2)
    #     self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def clear_entries(self):
        """чистка форми"""
        self.last_name_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.birth_date_entry.delete(0, tk.END)
        self.death_date_entry.delete(0, tk.END)
        self.age_value_label = "0"
        self.gender_combobox.set("")

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