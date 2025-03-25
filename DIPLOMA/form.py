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
        формочка для створення клієнтів

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
        self.label_font = ("Comic Sans MS", 10)
        self.help_text_font = ("Comic Sans MS", 9)
        self.submit_font = ("Comic Sans MS", 20, "bold")
        self.label_color = "white"
        self.submit_color = "white"
        self.window_bg_color = "#161F30"

        # основне вікно
        self.window = tk.Tk()
        self.window.title("ТУТ МОЖЕ БУТИ ВАША РЕКЛАМА")
        self.center_window(500, 285)  # Збільшили висоту вікна
        self.window.config(bg=self.window_bg_color)
        # img = Image.open('duck.png')
        # img.save('client.ico', format='ICO')
        self.window.iconbitmap('client.ico')

        # лівий для кнопок і правий для основного контенту
        self.frame_left = tk.Frame(self.window, bg=self.window_bg_color)
        self.frame_left.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.frame_left.grid_columnconfigure(1, minsize=100)
        self.frame_right = tk.Frame(self.window, bg=self.window_bg_color)
        self.frame_right.grid(row=0, column=1, sticky="nsew")

        # правому фреймі зверху фрейм для підказок
        self.top_frame = tk.Frame(self.frame_right, bg=self.window_bg_color,height=50)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.center_frame = tk.Frame(self.frame_right, bg=self.window_bg_color)
        self.center_frame.grid(row=1, column=0, sticky="nsew")

        # у лівому фреймі
        # елементи в верхньому фреймі
        self.help_text = tk.Label(self.top_frame, text="", fg="#FEDC24", font=self.help_text_font,
                                  bg=self.window_bg_color, anchor="e", height=2)
        self.help_text.grid(row=0, column=0, pady=1, sticky="w")
        # картинка для кнопок
        photo = ImageTk.PhotoImage(Image.open('del.bmp').resize((50, 50)))

        self.submit_button = tk.Button(self.frame_left,
                                       text="+", fg=self.submit_color, compound="center",
                                       font=self.submit_font,
                                       command=self.create_client, image=photo,
                                       activebackground=self.window_bg_color, bd=0,
                                       highlightthickness=0, pady=0, bg=self.window_bg_color)
        self.submit_button.grid(row=0, column=0, pady=0, padx=5, sticky="nsew")
        self.submit_button.bind("<Enter>", lambda event: self.help_text.config(text=f"Кнопка створення клієнта\n Можна записати із форми або із файла"))
        self.submit_button.bind("<Leave>", lambda event: self.help_text.config(text=""))

        self.submit_button = tk.Button(self.frame_left,
                                       text="?", fg=self.submit_color, compound="center",
                                       font=self.submit_font,
                                       command=self.search_client, image=photo,
                                       activebackground=self.window_bg_color, bd=0,
                                       highlightthickness=0, pady=0, bg=self.window_bg_color)
        self.submit_button.grid(row=1, column=0, pady=0, padx=1, sticky="nsew")
        self.submit_button.bind("<Enter>", lambda event: self.help_text.config(text=f"Пошук клієнта\n При пошуку автоматично створюється файл"))
        self.submit_button.bind("<Leave>", lambda event: self.help_text.config(text=""))

        self.submit_button = tk.Button(self.frame_left,
                                       text="–", fg=self.submit_color, compound="center",
                                       font=self.submit_font,
                                       command=self.delete_client, image=photo,
                                       activebackground=self.window_bg_color, bd=0,
                                       highlightthickness=0, pady=0, bg=self.window_bg_color)
        self.submit_button.grid(row=2, column=0, pady=0, padx=1, sticky="nsew")
        self.submit_button.bind("<Enter>", lambda event: self.help_text.config(text="Видалення клієнта"))
        self.submit_button.bind("<Leave>", lambda event: self.help_text.config(text=""))

        self.submit_button = tk.Button(self.frame_left,
                                       text="А", fg=self.submit_color, compound="center",
                                       font=self.submit_font,
                                       command=self.auto_fill, image=photo,
                                       activebackground=self.window_bg_color, bd=0,
                                       highlightthickness=0, pady=0, bg=self.window_bg_color)
        self.submit_button.grid(row=3, column=0, pady=0, padx=1, sticky="nsew")
        self.submit_button.bind("<Enter>", lambda event: self.help_text.config(text="Автозаповнення форми"))
        self.submit_button.bind("<Leave>", lambda event: self.help_text.config(text=""))

        self.submit_button = tk.Button(self.frame_left,
                                       text="О", fg=self.submit_color, compound="center",
                                       font=self.submit_font,
                                       command=self.clear_entries, image=photo,
                                       activebackground=self.window_bg_color, bd=0,
                                       highlightthickness=0, pady=0, bg=self.window_bg_color)
        self.submit_button.grid(row=4, column=0, pady=0, padx=1, sticky="nsew")
        self.submit_button.bind("<Enter>", lambda event: self.help_text.config(text="Очищення форми"))
        self.submit_button.bind("<Leave>", lambda event: self.help_text.config(text=""))

        # елементи в правому фреймі
        self.last_name_label = tk.Label(self.center_frame, text="Прізвище:", fg=self.label_color, font=self.label_font,
                                        bg=self.window_bg_color, anchor="e")
        self.last_name_label.grid(row=1, column=0, pady=1, sticky="ew")
        self.last_name_entry = tk.Entry(self.center_frame, width=20, font=self.label_font)
        self.last_name_entry.grid(row=1, column=1, pady=1, sticky="ew")

        self.first_name_label = tk.Label(self.center_frame, text="Ім'я:", fg=self.label_color, font=self.label_font,
                                         bg=self.window_bg_color, anchor="e")
        self.first_name_label.grid(row=2, column=0, pady=1, sticky="ew")
        self.first_name_entry = tk.Entry(self.center_frame, width=20, font=self.label_font)
        self.first_name_entry.grid(row=2, column=1, pady=1, sticky="ew")

        self.middle_name_label = tk.Label(self.center_frame, text="По батькові:", fg=self.label_color,
                                          font=self.label_font,
                                          bg=self.window_bg_color, anchor="e")
        self.middle_name_label.grid(row=3, column=0, pady=1, sticky="ew")
        self.middle_name_entry = tk.Entry(self.center_frame, width=20, font=self.label_font)
        self.middle_name_entry.grid(row=3, column=1, pady=1, sticky="ew")

        self.client_count_label = tk.Label(self.center_frame, text="Кількість клієнтів:", fg=self.label_color,
                                           font=self.label_font, bg=self.window_bg_color, anchor="e")
        self.client_count_label.grid(row=0, column=0, pady=1, sticky="ew")
        self.client_count_value_label = tk.Label(self.center_frame, text="0", fg=self.label_color, font=self.label_font,
                                                 bg=self.window_bg_color)
        self.client_count_value_label.grid(row=0, column=1, pady=1, sticky="w")

        self.gender_label = tk.Label(self.center_frame, text="Стать:", fg=self.label_color, font=self.label_font,
                                     bg=self.window_bg_color, anchor="e")
        self.gender_label.grid(row=4, column=0, pady=1, sticky="ew")

        # комбобокс
        self.gender_combobox = ttk.Combobox(self.center_frame, background="black",
                                            values=["чоловік", "жінка", ""],
                                            width=12, state="readonly")
        self.gender_combobox.set("")
        self.gender_combobox.grid(row=4, column=1, pady=1, sticky="w")

        # дати ДН і ДС
        self.birth_date_label = tk.Label(self.center_frame, text="Дата народження:", fg=self.label_color,
                                         font=self.label_font, bg=self.window_bg_color, anchor="e")
        self.birth_date_label.grid(row=5, column=0, pady=1, sticky="e")
        self.birth_date_entry = tk.Entry(self.center_frame, width=15,
                                         highlightbackground="white", highlightthickness=1)
        self.birth_date_entry.grid(row=5, column=1, pady=1, sticky="w")
        self.birth_date_entry.bind("<KeyRelease>", self.calculate_age) # оновлення віку

        self.death_date_label = tk.Label(self.center_frame, text="Дата смерті:", fg=self.label_color,
                                         font=self.label_font,
                                         bg=self.window_bg_color, anchor="e")
        self.death_date_label.grid(row=6, column=0, pady=1, sticky="e")
        self.death_date_entry = tk.Entry(self.center_frame, width=15)
        self.death_date_entry.grid(row=6, column=1, pady=1, sticky="w")
        self.death_date_entry.bind("<KeyRelease>", self.calculate_age) # оновлення віку

        self.age_label = tk.Label(self.center_frame, text="Вік:", fg=self.label_color, font=self.label_font,
                                  bg=self.window_bg_color, anchor="e")
        self.age_label.grid(row=7, column=0, pady=1, sticky="e")
        self.age_value_label = tk.Label(self.center_frame, text="0", fg=self.label_color, font=self.label_font,
                                        bg=self.window_bg_color)
        self.age_value_label.grid(row=7, column=1, pady=1, sticky="w")

        # чекбокс
        self.import_option_var = tk.BooleanVar()
        self.import_option_var.set(True)
        self.import_option = tk.Checkbutton(self.frame_left, text="із форми", variable=self.import_option_var,
                                            onvalue=True, offvalue=False, justify="center", fg="white",
                                            bg=self.window_bg_color, activebackground=self.window_bg_color,
                                            selectcolor=self.window_bg_color, indicatoron=True)
        self.import_option.grid(row=0, column=1, padx=1, pady=1, sticky="w")

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
        self.calculate_age() # вік

    def on_close(self):
        """при закритті вікна закривається і з'єднання до бд"""
        self.db.close_connection()
        self.window.destroy()

    def count_rows(self):
        """кількості клієнтів в бд"""
        return self.db.count_rows(self.table_name)

    def update_client_count(self):
        """оновлення к-ті в бд"""
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
        birth_date = process_date(birth_date)
        death_date = self.death_date_entry.get()
        death_date = process_date(death_date)

        self.client = Client(last_name, first_name, middle_name, gender, birth_date, death_date)

    def create_client(self):

        # якщо вибрано "з форми"
        if self.import_option_var.get():
            # створення клієнта в бд + перевірка на обов'язкові поля
            missing_fields = []

            # поле дата смерті не є обов'язковим
            if not self.last_name_entry.get():
                missing_fields.append(self.last_name_entry)
                self.last_name_entry.config(highlightbackground="red", highlightthickness=2)
                self.last_name_entry.after(400, self.reset)

            if not self.first_name_entry.get():
                missing_fields.append(self.first_name_entry)
                self.first_name_entry.config(highlightbackground="red", highlightthickness=2)
                self.first_name_entry.after(400, self.reset)

            if not self.middle_name_entry.get():
                missing_fields.append(self.middle_name_entry)
                self.middle_name_entry.config(highlightbackground="red", highlightthickness=2)
                self.middle_name_entry.after(400, self.reset)

            if not self.gender_combobox.get() or self.gender_combobox.get() == " ":
                missing_fields.append(self.gender_combobox)
                self.gender_combobox.set("!!!!!!!!!!!!!")
                self.gender_combobox.after(400, self.reset)

            if not self.birth_date_entry.get():
                missing_fields.append(self.birth_date_entry)
                self.birth_date_entry.config(highlightbackground="red", highlightthickness=2)
                self.birth_date_entry.after(400, self.reset)

            if missing_fields:
                return

            self.remember_client() # запам'ятовуємо клієнта
            self.client.add_one_client(self.db, self.table_name) # додаємо клієнта у бд

            # повідомлення
            messagebox.showinfo("Новий клієнт", "Успішно створено клієнта!")
            self.update_client_count()
            self.clear_entries()
        else:
            # відкриваємо вікно для введення назви файлу
            def import_from_csv():
                my_file_name = self.file_name_entry.get()  # отримуємо введену назву файлу

                # чи існує файл
                if not os.path.isfile(my_file_name):
                    messagebox.showerror("Помилка", "Файл не знайдено!")
                    return  # Зупиняємо подальше виконання, якщо файл не знайдений

                Client.add_client_from_csv(self.db, self.table_name, my_file_name)  # викликаємо метод для імпорту

                # повідомленням про успішний імпорт
                messagebox.showinfo("Імпорт з CSV", "Успішно імпортовано клієнтів!")
                # Очищаємо поля вводу
                self.clear_entries()
                # Оновлюємо кількість клієнтів
                self.update_client_count()

            # створюємо нове вікно для введення назви файлу
            file_window = tk.Toplevel(self.window)
            file_window.title("Вибір файлу для імпорту")
            file_window.geometry("400x150")
            file_window.config(bg=self.window_bg_color)

            # Центруємо вікно на екрані
            window_width = 400
            window_height = 150
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            file_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

            # блокуємо основне вікно
            file_window.grab_set()

            # лейбл для поля вводу назви файлу
            file_label = tk.Label(file_window, text="Введіть назву файлу:", font=self.label_font,
                                  fg=self.label_color, bg=self.window_bg_color)
            file_label.pack(padx=10, pady=10)

            # поле вводу для назви файлу, за замовчуванням "import_clients.csv"
            self.file_name_entry = tk.Entry(file_window, width=40)
            self.file_name_entry.insert(0, "import_clients.csv")  # значення за замовчуванням
            self.file_name_entry.pack(padx=10, pady=5)

            # кнопка для підтвердження імпорту
            import_button = tk.Button(file_window, text="ІМПОРТ", command=import_from_csv,
                                      width=15, fg="black", compound="center",
                                      font="black", pady=5,
                                      activebackground="white", bd=3,
                                      highlightthickness=0, bg="white",
                                        highlightbackground = self.label_color,
                                      highlightcolor = self.label_color)
            import_button.pack(pady=10)

            # обробник закриття вікна, щоб зняти блокування основного вікна
            def on_close_file_window():
                file_window.grab_release()  # Відновлюємо взаємодію з основним вікном
                file_window.destroy()  # Закриваємо вікно

            # підключаємо обробник події закриття вікна
            file_window.protocol("WM_DELETE_WINDOW", on_close_file_window)

    def reset(self):
        self.first_name_entry.config(highlightbackground="", highlightthickness=0)
        self.middle_name_entry.config(highlightbackground="", highlightthickness=0)
        self.last_name_entry.config(highlightbackground="", highlightthickness=0)
        if self.gender_combobox.get() == '!!!!!!!!!!!!!':
            self.gender_combobox.set("")
        self.birth_date_entry.config(highlightbackground="", highlightthickness=0)

    def search_client(self):
        self.remember_client()
        clients = self.client.find_clients(self.db, self.table_name, export_to_csv=True)

        # Вікно для результатів пошуку
        result_window = tk.Toplevel(self.window)
        result_window.title("Знайдені клієнти")

        # Визначаємо розміри вікна
        window_width = 600
        window_height = 400
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        result_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")  # Центруємо вікно
        result_window.config(bg=self.window_bg_color)

        # таблиця результатів
        my_table = ttk.Treeview(result_window, columns=(
        "Прізвище", "Ім'я", "По батькові", "Стать", "Вік", "Дата народження", "Дата смерті"), show="headings")
        my_table.heading("Прізвище", text="Прізвище")
        my_table.heading("Ім'я", text="Ім'я")
        my_table.heading("По батькові", text="По батькові")
        my_table.heading("Стать", text="Стать")
        my_table.heading("Вік", text="Вік")
        my_table.heading("Дата народження", text="Дата народження")
        my_table.heading("Дата смерті", text="Дата смерті")

        my_table.column("Прізвище", width=100)
        my_table.column("Ім'я", width=100)
        my_table.column("По батькові", width=100)
        my_table.column("Стать", width=50)
        my_table.column("Вік", width=40)
        my_table.column("Дата народження", width=100)
        my_table.column("Дата смерті", width=100)

        # Вставляємо знайдені дані у таблицю
        if clients:
            for client_id, client in clients.items():
                birth_date = datetime.strptime(client.birth_date, "%d.%m.%Y")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

                my_table.insert("", tk.END, values=(
                    client.last_name,
                    client.first_name,
                    client.middle_name,
                    client.gender,
                    str(age),
                    client.birth_date,
                    client.death_date
                ))
        else:
            my_table.insert("", tk.END, values=("Не знайдено", "", "", "", "", "", ""))

        my_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        close_button = tk.Button(result_window, text="ЗАКРИТИ", command=result_window.destroy,
                                 width=15, fg="black", compound="center",
                                 font="black", pady=5,
                                 activebackground="white", bd=3,
                                 highlightthickness=0, bg="white",
                                 highlightbackground=self.label_color,
                                 highlightcolor=self.label_color)
        close_button.pack(pady=10)

    def delete_client(self):
        # Показуємо підтвердження перед видаленням
        confirm = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити?")

        if confirm:
            self.remember_client()
            clients = self.client.find_clients(self.db, self.table_name, export_to_csv=False)

            if clients:
                self.client.delete_client(self.db, self.table_name)
                self.clear_entries()
                self.update_client_count()
                messagebox.showinfo("Видалення клієнта", "Успішно видалено!")
            else:
                messagebox.showwarning("Помилка", "Клієнтів для видалення не знайдено!")
        else:
            messagebox.showinfo("Скасовано", "Видалення відмінено")

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
        self.age_value_label.config(text="0")
        self.gender_combobox.set("")