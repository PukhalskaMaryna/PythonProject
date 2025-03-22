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

print(db1.count_rows(clients_table))
# Client(gender='Ж').delete_client(db1,clients_table)
print(db1.count_rows(clients_table))

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
        self.gender_entry = None
        self.db_file = db_file
        self.table_name = table_name
        self.client = None  # потенційний клієнт

        # основне вікно
        self.window = tk.Tk()
        self.window.title("Тут ви можете працювати з клієнтськими даними")
        self.center_window(500, 300)
        self.window.config(bg="lightblue")

        # лейблики та поля вводу
        label_font = ("Arial", 11, "bold")
        label_color = "#4B8BD4"  # приємний синій колір

        # лейблики (вирівняні по правому краю, з новим кольором)
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

        # Заміна на combobox для вибору статі
        self.gender_options = ["чоловік", "жінка"]
        self.gender_combobox = ttk.Combobox(self.window, values=self.gender_options, width=40, state="readonly")
        self.gender_combobox.set("чоловік")  # Встановлюємо значення за замовчуванням
        self.gender_combobox.grid(row=3, column=1, pady=5, sticky="ew")

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
            self.first_name_entry.config(highlightbackground="lightblue",
                                         highlightthickness=1)  # Відновлюємо нормальний стиль

        if not self.middle_name_entry.get():
            missing_fields.append(self.middle_name_entry)
            self.middle_name_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.middle_name_entry.config(highlightbackground="lightblue",
                                          highlightthickness=1)  # Відновлюємо нормальний стиль

        if not self.gender_entry.get():
            missing_fields.append(self.gender_entry)
            self.gender_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.gender_entry.config(highlightbackground="lightblue",
                                     highlightthickness=1)  # Відновлюємо нормальний стиль

        if not self.birth_date_entry.get():
            missing_fields.append(self.birth_date_entry)
            self.birth_date_entry.config(highlightbackground="red", highlightthickness=2)
        else:
            self.birth_date_entry.config(highlightbackground="lightblue",
                                         highlightthickness=1)  # Відновлюємо нормальний стиль

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
                              f"Дата смерті: {client.death_date if client.death_date else 'Немає'}\n\n"

                # Додаємо інформацію про клієнта в текстове поле
                result_text.insert(tk.END, client_text)

            # Функція для експорту клієнтів у CSV файл
            def export_clients_to_csv():
                self.client.find_clients(self.db_file, self.table_name, export_to_csv=True)

            # Кнопка Імпорт для експорту у CSV
            import_button = tk.Button(result_window, text="Імпорт", command=export_clients_to_csv, width=20, bg="white",
                                      activebackground="lightgray", relief="flat", bd=2, highlightthickness=0,
                                      font=("Arial", 10, "bold"), pady=5)
            import_button.pack(pady=10)

            # Закриття вікна без експорту (параметр export_to_csv=False)
            result_window.protocol("WM_DELETE_WINDOW",
                                   lambda: self.client.find_clients(self.db_file, self.table_name, export_to_csv=False))

        else:
            # Якщо клієнтів не знайдено, виводимо повідомлення
            result_window = tk.Toplevel(self.window)
            result_window.title("Знайдені клієнти")
            result_window.geometry("300x150")
            label = tk.Label(result_window, text="Клієнтів не знайдено!", font=("Arial", 12), fg="red", bg="lightblue")
            label.pack(padx=20, pady=20)

    def delete_client(self):
        self.remember_client()

        # чи є клієнт
        if self.client:
            # delete_client класу Client
            self.client.delete_client(self.db_file, self.table_name)
            print(f"Клієнта {self.client.first_name} {self.client.last_name} видалено з бази даних.")

            # вікно для результатів
            result_window = tk.Toplevel(self.window)
            result_window.title("Видалені клієнти")
            result_window.geometry("500x400")

            result_text = tk.Text(result_window, width=60, height=15, wrap=tk.WORD, bg="lightblue", fg="#4B8BD4",
                                  font=("Arial", 10))
            result_text.pack(padx=10, pady=10)

            # додаємо інформацію про видаленого клієнта
            client_text = f"{self.client.first_name} {self.client.last_name} {self.client.middle_name} - Видалено\n" \
                          f"Стать: {self.client.gender}\n" \
                          f"Дата народження: {self.client.birth_date}\n" \
                          f"Дата смерті: {self.client.death_date if self.client.death_date else 'Немає'}\n\n"
            result_text.insert(tk.END, client_text)

            # закриття вікна
            result_window.protocol("WM_DELETE_WINDOW", result_window.destroy)

        else:
            # клієнта не знайдено
            result_window = tk.Toplevel(self.window)
            result_window.title("Видалення клієнта")
            result_window.geometry("300x150")
            label = tk.Label(result_window, text="Клієнтів для видалення не знайдено!", font=("Arial", 12), fg="red",
                             bg="lightblue")
            label.pack(padx=20, pady=20)

    def run(self):
        self.window.mainloop()


# Запуск форми
form = Form()
form.run()


