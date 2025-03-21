import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
import os
from datetime import datetime
import re

class DB:
    def __init__(self, db_file_name: str = 'db.db'):

        """
        бд

        :param db_file_name: Str, path-like object, назва файлу бд, за замовчуванням db.db
        :param conn: незадаваємий параметр, який в собі містить інфу, чи є конект, початково конект відсутній
        """
        self.db_file_name = db_file_name
        self.conn = None

    def __str__(self):
        return f"База даних: {self.db_file_name}"

    def delete_db(self):
        """
        delete бд
        https://www.geeksforgeeks.org/python-os-path-exists-method/
        """
        if os.path.exists(self.db_file_name):
            os.remove(self.db_file_name)

    def open_connection(self):
        """
        open бд
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Error
        Важливо, що навіть якщо цей метод викликати на нестворену бд, тобто фактично файл з бд не існує,
        то файл успішно створиться і конект буде з новоствореним файлом
        """
        try:
            self.conn = sqlite3.connect(self.db_file_name)
            return self.conn
        except sqlite3.Error as sql_error:
            print(f"Не вдалося підключитися до бд: {sql_error}")
            return None

    def close_connection(self):
        """
        close з'єднання з бд
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.close
        """
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, params: tuple = ()):
        """
        створення запиту до бд
        https://docs.python.org/3/library/sqlite3.html#cursor-objects

        :param query: str, SQL-запит
        :param params: tuple, параметри для запиту
        :return: list, tuple, результат виконання запиту список кортежів
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            my_cursor = self.conn.cursor()  # курсор
            my_cursor.execute(query, params)  # виклик за запитом
            self.conn.commit()  # commit
            result = my_cursor.fetchall()  # результат запиту у вигляді списку кортежів, кортеж - рядок із таблиці
            my_cursor.close()  # закриваємо курсор
            return result
        except sqlite3.Error as sql_error:
            print(f"Помилка execute_query: {sql_error}")
            return None

    def create_table(self, table_name: str, field_with_type: str):
        """
        створення таблички

        :param table_name: Str, назва таблички
        :param field_with_type: str, рядок з полями та їх типами
        приклад:
        fields = 'title TEXT NOT NULL, year INTEGER NOT NULL, director TEXT'
        """

        fields = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + field_with_type # id як PRIMARY KEY
        self.execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})")

    def drop_table(self, table_name: str):
        """
        дроп таблиці

        :param table_name: Str, назва таблиці
        """
        self.execute_query(f"DROP TABLE IF EXISTS {table_name}")

    def insert_into_table(self, table_name: str, row = tuple()):
        """
        вставка 1 рядка

        :param table_name: Str, назва таблиці бд, в яку додаємо дані
        :param row: tuple, значення для одного рядка по кожному полю, крім id
            приклад, ("Пухальська", "Марина", "Ж", "21.10.1983")
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            result = self.execute_query(f"SELECT MAX(id) FROM {table_name}")
            next_id = 1 if not result or result[0][0] is None else result[0][0] + 1

            columns_result = self.execute_query(f"PRAGMA table_info({table_name})") #список полів таблиці
            columns = [column[1] for column in columns_result]

            query = f"INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join("?" for _ in columns)})"
            self.execute_query(query, (next_id, *row))
        except sqlite3.Error as sql_error:
            print(f"Помилка insert_into_table: {sql_error}")

    def delete_from_table(self, table_name: str, conditions: dict):
        """
        видалення рядка\рядків

        :param table_name: Str, назва таблиці бд, з якої видаляємо дані
        :param conditions: dict, словник з умовами видалення,
                приклад {'id': 1} або {'last_name': 'Пухальська', 'first_name': 'Марина'}
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            condition_strings = []
            params = []
            for column, value in conditions.items():
                condition_strings.append(f"{column} = ?")  # ['last_name = ?', 'first_name = ?']
                params.append(value)  # ['Пухальська', 'Марина']
            condition_clause = " AND ".join(condition_strings)  # 'last_name = ? AND first_name = ?'

            self.execute_query(f"DELETE FROM {table_name} WHERE {condition_clause}", tuple(params))
        except sqlite3.Error as sql_error:
            print(f"Помилка delete_from_table: {sql_error}")

    def truncate_table(self, table_name: str):
        """
        видалення всіх рядків таблиці в межах бд

        :param table_name: str, назва таблиці, яку потрібно очистити
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            self.execute_query(f"DELETE FROM {table_name}")
        except sqlite3.Error as sql_error:
            print(f"Помилка truncate_table: {sql_error}")

    def count_rows(self, table_name: str):
        """
        к-ть рядків у таблиці

        :param table_name: Str, назва таблиці в базі даних
        :return: кількість рядків в таблиці
        """
        if not self.conn:
            print("Не встановлено підключення")

        try:
            result = self.execute_query(f"SELECT COUNT(*) FROM {table_name}")
            if result:
                return result[0][0]
            return 0
        except sqlite3.Error as sql_error:
            print(f"Помилка count_rows: {sql_error}")


# метод для обробки дат
def process_date(date_str: str):
    """
    обробка дати, приведення до потрібного формату

    :param date_str: Str, дата для обробки
    :return: str формату "dd.mm.yyyy" або None
    """

    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_str):
        return date_str
    # "yyyy-mm-dd"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        pass
    # "dd mm yyyy"
    if re.match(r'^\d{1,2} \d{1,2} \d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d %m %Y").strftime("%d.%m.%Y")
        except ValueError:
            return None
    # "dd/mm/yyyy"
    if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d.%m.%Y")
        except ValueError:
            return None
    # "d-m-yyyy"
    if re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%d.%m.%Y")
        except ValueError:
            return None

    return None


class Client:
    def __init__(self
                 , last_name: str = ''
                 , first_name: str = ''
                 , middle_name: str = ''
                 , gender: str = ''
                 , birth_date: str = ''
                 , death_date: str = ''):

        """
        клієнт

        :param last_name: Str, прізвище клієнта
        :param first_name: str, ім'я клієнта
        :param middle_name: str, по батькові клієнта
        :param gender: str, стать клієнта
        :param birth_date: дата народження клієнта
        :param death_date: дата смерті клієнта (необов'язково)
        """
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.gender = gender
        self.birth_date = birth_date
        self.death_date = death_date

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} - {self.gender} - {self.birth_date} - {self.death_date}"

    def add_one_client(self, db: DB, table_name: str):
        """
        додаємо 1 клієнта

        :param db: DB, підключення до бд
        :param table_name: str, назва таблиці
        :return: None
        """
        # ДН
        correct_birth_date = process_date(str(self.birth_date))
        if not correct_birth_date:
            print(f"Помилка: невірний формат ДН клієнта {self.last_name}, пропускаємо")
            return

        # ДС
        if self.death_date:
            correct_death_date = process_date(str(self.death_date))
            if correct_death_date is None:
                print(f"Помилка: невірний формат ДС клієнта {self.last_name}, пропускаємо")
                return
        else:
            correct_death_date = None

        row = (self.last_name, self.first_name, self.middle_name, self.gender, correct_birth_date, correct_death_date)
        db.insert_into_table(table_name, row)

    @staticmethod
    def add_client_from_csv(db: DB, table_name: str, my_file_name: str = 'import_clients.csv'):
        """
        додаємо клієнтів із csv, метод статичний, бо нема звернення до конкретного клієнта

        :param db: DB, підключення до бд
        :param table_name: str, назва таблиці
        :param my_file_name: назва csv для імпорту, за замовчуванням 'import_clients.csv'
        :return: None
        """
        if not os.path.exists(my_file_name):
            print(f"Файл '{my_file_name}' відсутній")
            return

        with open(my_file_name, newline='', encoding='utf-8-sig') as csv_file:
            for row in csv.DictReader(csv_file):
                if 'last_name' not in row or 'first_name' not in row or 'middle_name' not in row or 'gender' not in row or 'birth_date' not in row:
                    print("Невірний формат файлу")
                    continue

                # ДН
                birth_date = process_date(str(row['birth_date']))
                if birth_date is None:
                    print(f"Помилка: невірний формат дати для клієнта {row['id']}. Пропускаємо.")
                    continue

                # ДС
                if 'death_date' in row and row['death_date']:
                    death_date = process_date(str(row['death_date']))
                    if death_date is None:
                        print(f"Помилка: невірний формат дати смерті для клієнта {row['id']}. Пропускаємо.")
                        continue
                else:
                    death_date = None

                client = Client(row["last_name"], row["first_name"], row["middle_name"], row["gender"], birth_date, death_date)
                client.add_one_client(db, table_name)

    def find_clients(self, db: DB, table: str, export_to_csv: bool = True):
        """
        пошук клієнта за частковими збігами в прізвищі, імені, по батькові

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        :param export_to_csv: bool, якщо True, експортує клієнтів у csv
        :return: list, список клієнтів, що відповідають умовам
        """
        conditions = []
        params = []

        # Пошук за прізвищем
        if self.last_name:
            conditions.append("last_name LIKE ?")
            params.append(f"%{self.last_name}%")

        # Пошук за ім'ям
        if self.first_name:
            conditions.append("first_name LIKE ?")
            params.append(f"%{self.first_name}%")

        # Пошук за по батькові
        if self.middle_name:
            conditions.append("middle_name LIKE ?")
            params.append(f"%{self.middle_name}%")

        # Пошук за статтю
        if self.gender:
            conditions.append("gender = ?")
            params.append(self.gender)

        # Пошук за датою народження
        if self.birth_date:
            birth_date = process_date(self.birth_date)
            if birth_date:
                conditions.append("birth_date = ?")
                params.append(birth_date)

        # Пошук за датою смерті
        if self.death_date:
            death_date = process_date(self.death_date)
            if death_date:
                conditions.append("death_date = ?")
                params.append(death_date)

        # Якщо немає жодних умов для пошуку
        if not conditions:
            print("Вкажіть хоча б 1 параметр для пошуку")
            return []

        # Формуємо частину умови WHERE для SQL-запиту
        condition_clause = " AND ".join(conditions)

        # Формуємо запит
        query = f"SELECT * FROM {table} WHERE {condition_clause}"

        # Виконуємо запит до бази даних
        result = db.execute_query(query, tuple(params))

        clients = {}
        for row in result:
            client = Client(
                last_name=row[1],
                first_name=row[2],
                middle_name=row[3],
                gender=row[4],
                birth_date=row[5],
                death_date=row[6]  # Додаємо обробку дати смерті
            )
            client_id = row[0]
            clients.update({client_id: client})

        # Якщо потрібно експортувати дані в CSV
        if export_to_csv:
            file_name = 'found_clients.csv'
            i = 1
            while os.path.exists(file_name):
                file_name = f'found_clients_{i}.csv'
                i += 1

            with open(file_name, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "last_name", "first_name", "middle_name", "gender", "birth_date", "death_date"])
                for client_id, client in clients.items():
                    writer.writerow([client_id, client.last_name, client.first_name,
                                     client.middle_name, client.gender, client.birth_date, client.death_date])

        return clients

    def delete_client(self, db: DB, table_name: str):
        """
        видалення клієнтів
        використовує метод find_clients для пошуку клієнтів перед їх видаленням

        :param db: DB, підключення до бд
        :param table_name: str, назва таблиці
        """
        clients_to_delete = self.find_clients(db, table_name, export_to_csv=False)

        if clients_to_delete:
            for client_id, client in clients_to_delete.items():
                conditions = {'id': client_id}
                db.delete_from_table(table_name, conditions)


#################################################################
db1 = DB('db.db')

# print(db1)
db1.open_connection()
db1.drop_table('clients')
db1.create_table('clients',"last_name TEXT,first_name TEXT, middle_name TEXT, gender TEXT, birth_date DATE, death_date DATE")

# my_table = 'clients'
# cnt_rows = db1.count_rows(my_table)
# db1.insert_into_table('clients', (cnt_rows + 1,"Пухальська2", "Марина"))


#################################################################

cl1 = Client('Пухальська','Марина','Василівна','жінка','21.10.1983')
print(cl1)
cl2 = Client('Анкудінова',"Дар'я",'Сергіївна','жінка','25.04.1995')
print(cl2)
cl3 = Client('Пухальський',"Максим",'Петрович',gender='чоловік',birth_date='21.10.1983')
print(cl3)

clients_table = 'clients'

db1.truncate_table(clients_table)

cl1.add_one_client(db1,clients_table)
cl2.add_one_client(db1,clients_table)
cl3.add_one_client(db1,clients_table)

# cl1.find_clients(db1,clients_table)
# Client(gender='Ж').find_clients(db1,clients_table)
# Client(gender='Ч').find_clients(db1,clients_table)
# Client(birth_date='21.10.1983',gender='Ж').find_clients(db1,clients_table)

# print(db1.count_rows(clients_table))
# Client(gender='Ж').delete_client(db1,clients_table)
# print(db1.count_rows(clients_table))

# Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')
# Client.add_client_from_csv(db1, 'clients', 'found_clients_2.csv')
# Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')

# print(db1.count_rows(clients_table))
# print("УРА!!")
db1.close_connection()
#################################################################

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

        # ініціалізація змінних для лейблів та полів вводу
        self.last_name_label = None
        self.last_name_entry = None
        self.first_name_label = None
        self.first_name_entry = None
        self.middle_name_label = None
        self.middle_name_entry = None
        self.gender_label = None
        self.gender_combobox = None
        self.birth_date_label = None
        self.birth_date_entry = None
        self.death_date_label = None
        self.death_date_entry = None
        self.age_label = None
        self.age_value_label = None
        self.import_option_label = None
        self.import_option = None

        # стилі для лейблів
        self.label_font = ("Arial", 11, "bold")
        self.label_color = "#4B8BD4"  # приємний синій колір

        # основне вікно
        self.window = tk.Tk()
        self.window.title("Тут ви можете працювати з клієнтськими даними")
        self.center_window(500, 300)
        self.window.config(bg="lightblue")

        # лейбли та поля вводу
        self.create_widgets()

    def create_widgets(self):
        """Створення всіх елементів на формі."""
        # лейбли та поля вводу
        self.last_name_label, self.last_name_entry = self.create_label_entry(0, "Прізвище:")
        self.first_name_label, self.first_name_entry = self.create_label_entry(1, "Ім'я:")
        self.middle_name_label, self.middle_name_entry = self.create_label_entry(2, "По батькові:")
        self.birth_date_label, self.birth_date_entry = self.create_label_entry(4, "Дата народження:", entry_width=10)
        self.death_date_label, self.death_date_entry = self.create_label_entry(5, "Дата смерті:", entry_width=10)

        # специфічний для статі combobox
        self.gender_label = tk.Label(self.window, text="Стать:", fg=self.label_color, font=self.label_font,
                                     bg="lightblue",
                                     anchor="e")
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
                return

            # запам'ятовуємо клієнта
            self.remember_client()

            # додаємо клієнта у бд
            self.client.add_one_client(self.db_file, self.table_name)

            # повідомленням про успішне створення клієнта
            success_window = tk.Toplevel(self.window)
            success_window.title("Новий клієнт")
            success_window.geometry("300x150")
            success_label = tk.Label(success_window, text="Успішно створено клієнта!", font=self.label_font,
                                     fg=self.label_color, bg="lightblue")
            success_label.pack(padx=20, pady=20)
            close_button = tk.Button(success_window, text="Закрити", command=success_window.destroy, width=15,
                                     bg="white", activebackground="lightgray", relief="flat", bd=2,
                                     highlightthickness=0, font=("Arial", 10, "bold"), pady=5)
            close_button.pack(pady=10)


        # якщо вибрано "з csv"
        elif self.import_option.get() == "з csv":
            # відкриваємо вікно для введення назви файлу
            def import_from_csv():
                my_file_name = self.file_name_entry.get()  # отримуємо введену назву файлу
                self.client.add_client_from_csv(self.db_file, self.table_name,
                                                my_file_name)  # викликаємо метод для імпорту

            # створюємо нове вікно для введення назви файлу
            file_window = tk.Toplevel(self.window)
            file_window.title("Вибір файлу для імпорту")
            file_window.geometry("400x150")

            # лейбл для поля вводу назви файлу
            file_label = tk.Label(file_window, text="Введіть назву файлу:", font=self.label_font,
                                                fg=self.label_color,bg="lightblue")
            file_label.pack(padx=10, pady=10)

            # поле вводу для назви файлу, за замовчуванням "import_clients.csv"
            self.file_name_entry = tk.Entry(file_window, width=40)
            self.file_name_entry.insert(0, "import_clients.csv")  # значення за замовчуванням
            self.file_name_entry.pack(padx=10, pady=5)

            # кнопка для підтвердження імпорту
            import_button = tk.Button(file_window, text="Імпортувати", command=import_from_csv,
                                      width=20, bg="white",activebackground="lightgray",
                                      relief="flat", bd=2,highlightthickness=0,
                                      font=("Arial", 10, "bold"), pady=5)
            import_button.pack(pady=10)

    def search_client(self):
        # Спочатку запам'ятовуємо дані клієнта з форми
        self.remember_client()

        # Шукаємо клієнта в базі даних за допомогою методу find_clients
        clients = self.client.find_clients(self.db_file, self.table_name, export_to_csv=False)

        # клієнтів знайдено
        if clients:
            # Створюємо нове вікно для результатів пошуку
            result_window = tk.Toplevel(self.window)
            result_window.title("Знайдені клієнти")
            result_window.geometry("500x400")

            # Створюємо Text widget для відображення всіх клієнтів
            result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue",
                                                 fg="#4B8BD4",font=("Arial", 10))
            result_text.pack(padx=10, pady=10)

            # додаємо інформацію в текстове поле
            for client_id, client in clients.items():
                # Обчислюємо вік клієнта
                birth_date = datetime.strptime(client.birth_date, "%d.%m.%Y")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

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
        self.remember_client()
        clients = self.client.find_clients(self.db_file, self.table_name)

        if clients:
            self.client.delete_one_client(self.db_file, self.table_name)
            print(f"Клієнта {self.client.last_name} {self.client.first_name} видалено!")
        else:
            print("Клієнта не знайдено!")

    def center_window(self, width, height):
        """центрує вікно на екрані"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_right}+{position_top}')


# Запуск програми
form = Form()
form.window.mainloop()



