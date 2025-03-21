# import tkinter as tk
# from tkinter import ttk
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
                 , birth_date: datetime = None
                 , death_date: datetime = None):

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

        :param db: DB, підключення до бази даних
        :param table_name: str, назва таблиці
        :return: None
        """
        # ДН
        correct_birth_date = process_date(self.birth_date)
        if not correct_birth_date:
            print(f"Помилка: невірний формат дати народження для клієнта {self.last_name}. Пропускаємо.")
            return

        # ДС
        if self.death_date:
            correct_death_date = process_date(self.death_date)
            if correct_death_date is None:
                print(f"Помилка: невірний формат дати смерті для клієнта {self.last_name}. Пропускаємо.")
                return
        else:
            correct_death_date = None

        row = (self.last_name, self.first_name, self.middle_name, self.gender, correct_birth_date, correct_death_date)
        db.insert_into_table(table_name, row)

    @staticmethod
    def add_client_from_csv(db: DB, table_name: str, my_file_name: str = 'import_clients.csv'):
        """
        додаємо клієнтів із csv

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

                # Обробка дати народження
                birth_date = process_date(row['birth_date'])
                if birth_date is None:
                    print(f"Помилка: невірний формат дати для клієнта {row['id']}. Пропускаємо.")
                    continue

                # Обробка дати смерті (якщо є)
                if 'death_date' in row and row['death_date']:
                    death_date = process_date(row['death_date'])
                    if death_date is None:
                        print(f"Помилка: невірний формат дати смерті для клієнта {row['id']}. Пропускаємо.")
                        continue
                else:
                    death_date = None

                client = Client(row["last_name"], row["first_name"], row["middle_name"], row["gender"], birth_date, death_date)
                client.add_one_client(db, table_name)

    def find_clients(self, db: DB, table: str, export_to_csv: bool = True):
        """
        пошук клієнта

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        :param export_to_csv: bool, якщо True, експортує клієнтів у csv
        :return: list, список клієнтів, що відповідають умовам
        """
        conditions = []
        params = []

        if self.last_name:
            conditions.append("last_name = ?")
            params.append(self.last_name)
        if self.first_name:
            conditions.append("first_name = ?")
            params.append(self.first_name)
        if self.middle_name:
            conditions.append("middle_name = ?")
            params.append(self.middle_name)
        if self.gender:
            conditions.append("gender = ?")
            params.append(self.gender)
        if self.birth_date:
            birth_date = process_date(self.birth_date)
            if birth_date:
                conditions.append("birth_date = ?")
                params.append(birth_date)
        if self.death_date:
            death_date = process_date(self.death_date)
            if death_date:
                conditions.append("death_date = ?")
                params.append(death_date)

        if not conditions:
            print("Вкажіть хоча б 1 параметр для пошуку")
            return []

        condition_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {table} WHERE {condition_clause}"
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

        # csv
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

cl1 = Client('Пухальська','Марина','Василівна','Ж','21.10.1983')
print(cl1)
cl2 = Client('Анкудінова',"Дар'я",'Сергіївна','Ж','01.11.2000')
print(cl2)
cl3 = Client('Пухальський',"Максим",'Петрович',gender='Ч',birth_date='21.10.1983')
print(cl3)

clients_table = 'clients'
print(1)
db1.truncate_table(clients_table)
print(2)
cl1.add_one_client(db1,clients_table)
cl2.add_one_client(db1,clients_table)
cl3.add_one_client(db1,clients_table)
print(3)
cl1.find_clients(db1,clients_table)
Client(gender='Ж').find_clients(db1,clients_table)
Client(gender='Ч').find_clients(db1,clients_table)
Client(birth_date='21.10.1983',gender='Ж').find_clients(db1,clients_table)
print(4)

print(db1.count_rows(clients_table))
Client(gender='Ж').delete_client(db1,clients_table)
print(db1.count_rows(clients_table))

Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')
Client.add_client_from_csv(db1, 'clients', 'found_clients_2.csv')
Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')

print(db1.count_rows(clients_table))
print("УРА!!")
db1.close_connection()
#################################################################
