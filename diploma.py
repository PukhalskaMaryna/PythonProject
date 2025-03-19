# import dearpygui.dearpygui as dpg
import sqlite3
import csv
import os
from datetime import datetime
import re

class DB:
    def __init__(self, db_file_name='db.db'):

        """
        Клас для роботи з базою даних.

        :param db_file_name: Str, path-like object, назва файлу бд, за замовчуванням db.db
        :param conn: незадаваємий параметр, який в собі містить інфу, чи є конект, по замовчуванню конекта нема
        """
        self.db_file_name = db_file_name
        self.conn = None

    def __str__(self):
        return f"База даних: {self.db_file_name}"

    def delete_db(self):
        """
        Видалення файлу бд
        https://www.geeksforgeeks.org/python-os-path-exists-method/
        """
        if os.path.exists(self.db_file_name):
            os.remove(self.db_file_name)

    def open_connection(self):
        """
        Підключення до бд
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
        Закриття з'єднання з бд
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.close
        """
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        """
        Метод запиту до бази даних
        https://docs.python.org/3/library/sqlite3.html#cursor-objects

        :param query: str, SQL-запит
        :param params: tuple, параметри для запиту
        :return: list, turtle, результат виконання запиту список кортежів
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

    def create_table(self, table, fields):
        """
        Створення таблиці з зазначеними полями.

        :param table: Str, назва таблиці
        :param fields: str, рядок з полями та їх типами
        приклад:
        fields = 'title TEXT NOT NULL, year INTEGER NOT NULL, director TEXT'
        """

        fields = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + fields # id як PRIMARY KEY
        self.execute_query(f"CREATE TABLE IF NOT EXISTS {table} ({fields})")

    def drop_table(self, table):
        """
        Видалені таблиці

        :param table: Str, назва таблиці
        """
        self.execute_query(f"DROP TABLE IF EXISTS {table}")

    def insert_into_table(self, table, row):
        """
        Метод для вставки одного рядка

        :param table: Str, назва таблиці бд, в яку додаємо дані
        :param row: tuple, значення для одного рядка по кожному полю, крім id
            приклад, ("Пухальська", "Марина", "Ж", "21.10.1983")
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            result = self.execute_query(f"SELECT MAX(id) FROM {table}")
            next_id = 1 if not result or result[0][0] is None else result[0][0] + 1

            # передаємо значення як параметри в SQL-запит
            query = f"INSERT INTO {table} (id, last_name, first_name, middle_name, gender, birth_date) VALUES (?, ?, ?, ?, ?, ?)"
            self.execute_query(query, (next_id, *row))
        except sqlite3.Error as sql_error:
            print(f"Помилка insert_into_table: {sql_error}")

    def delete_from_table(self, table, conditions):
        """
        Метод видалення

        :param table: Str, назва таблиці бд, з якої видаляємо дані
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

            self.execute_query(f"DELETE FROM {table} WHERE {condition_clause}", tuple(params))
        except sqlite3.Error as sql_error:
            print(f"Помилка delete_from_table: {sql_error}")

    def truncate_table(self, table_name):
        """
        Очищення всіх даних

        :param table_name: str, назва таблиці, яку потрібно очистити
        """
        if not self.conn:
            print("Не встановлено підключення")
            return None

        try:
            self.execute_query(f"DELETE FROM {table_name}")
        except sqlite3.Error as sql_error:
            print(f"Помилка truncate_table: {sql_error}")

    def count_rows(self, table_name):
        """
        Підрахунок кількості рядків у таблиці.

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

#################################################################
db1 = DB('db.db')

# print(db1)
db1.open_connection()
db1.drop_table('clients')
db1.create_table('clients',"last_name TEXT,first_name TEXT, middle_name TEXT, gender TEXT, birth_date DATE")

# my_table = 'clients'
# cnt_rows = db1.count_rows(my_table)
# db1.insert_into_table('clients', (cnt_rows + 1,"Пухальська2", "Марина"))


#################################################################

class Client:
    def __init__(self, last_name="", first_name="", middle_name="", gender="", birth_date=None):
        """
        Ініціалізація об'єкта клієнта.

        :param last_name: Str, прізвище клієнта
        :param first_name: str, ім'я клієнта
        :param middle_name: str, по батькові клієнта
        :param gender: str, стать клієнта
        :param birth_date: дата народження клієнта
        """
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.gender = gender
        self.birth_date = birth_date

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} - {self.gender} - {self.birth_date}"

    def add_one_client(self, db=DB(), table=str()):
        """
        Додавання одного клієнта

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        :return: None
        """

        def is_valid_date(date_str):
            date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
            return not bool(re.match(date_pattern, date_str))

        if not is_valid_date(self.birth_date):
            correct_birth_date = self.birth_date
        else:
            try:
                correct_birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d").strftime("%d.%m.%Y")
            except ValueError:
                print(f"Помилка: невірний формат дати для клієнта {self.last_name}. Пропускаємо.")
                return

        row = (self.last_name, self.first_name, self.middle_name, self.gender, correct_birth_date)
        db.insert_into_table(table, row)

    @staticmethod
    def add_client_from_csv(db=DB(), table=str(), my_file_name='import_clients.csv'):
        """
        Додавання клієнтів із csv

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        :param my_file_name: назва csv для імпорту, за замовчуванням 'import_clients.csv'
        :return: None
        """

        def is_valid_date(date_str):
            date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
            return not bool(re.match(date_pattern, date_str))

        if not os.path.exists(my_file_name):
            print(f"Файл '{my_file_name}' відсутній")
            return

        with open(my_file_name, newline='', encoding='utf-8-sig') as csv_file:
            for row in csv.DictReader(csv_file):
                # а чи всі поля у файлі?
                if 'last_name' not in row or 'first_name' not in row or 'middle_name' not in row or 'gender' not in row or 'birth_date' not in row:
                    print("Невірний формат файлу")
                    continue

                if is_valid_date(row['birth_date']):
                    birth_date = row['birth_date']  # Залишаємо без змін, якщо дата вже у вірному форматі
                else:
                    try:
                        birth_date = datetime.strptime(row['birth_date'], "%d.%m.%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        print(
                            f"Помилка: невірний формат дати для клієнта {row['id']}. Пропускаємо.")
                        continue

                client = Client(row["last_name"], row["first_name"], row["middle_name"], row["gender"], birth_date)
                client.add_one_client(db, table)

    def find_clients(self, db=DB(), table=str(), export_to_csv=True):
        """
        Пошук клієнтів

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
            birth_date = datetime.strptime(self.birth_date, "%d.%m.%Y").strftime("%Y-%m-%d")
            conditions.append("birth_date = ?")
            params.append(birth_date)

        if not conditions:
            print("Вкажіть хоч 1 параметр для пошуку")
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
                birth_date=row[5]
            )
            client_id = row[0]
            clients.update({client_id: client})

        # csv
        if export_to_csv:
            file_name = 'found_clients.csv'
            i = 1
            while os.path.exists(file_name):  # якщо файл з такою назвою вже існує, додаємо цифру
                file_name = f'found_clients_{i}.csv'
                i += 1

            with open(file_name, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "last_name", "first_name", "middle_name", "gender", "birth_date"])
                for client_id, client in clients.items():
                    writer.writerow([client_id, client.last_name, client.first_name,
                                     client.middle_name, client.gender, client.birth_date])

        return clients

    def delete_client(self, db = DB(), table = str()):
        """
        Видалення клієнтів з таблиці на основі атрибутів цього клієнта.
        Використовує метод search_clients для пошуку клієнтів перед їх видаленням.

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        """
        clients_to_delete = self.find_clients(db, table, export_to_csv=False)

        if clients_to_delete:
            for client_id, client in clients_to_delete.items():
                conditions = {'id': client_id}
                db.delete_from_table(table, conditions)

#################################################################

cl1 = Client('Пухальська','Марина','Василівна','Ж','21.10.1983')
print(cl1)
cl2 = Client('Анкудінова',"Дар'я",'Сергіївна','Ж','01.11.2000')
print(cl2)
cl3 = Client('Пухальський',"Максим",gender='Ч',birth_date='21.10.1983')
print(cl3)

clients_table = 'clients'

db1.truncate_table(clients_table)

cl1.add_one_client(db1,clients_table)
cl2.add_one_client(db1,clients_table)
cl3.add_one_client(db1,clients_table)

cl1.find_clients(db1,clients_table)
Client(gender='Ж').find_clients(db1,clients_table)
Client(gender='Ч').find_clients(db1,clients_table)
Client(birth_date='21.10.1983',gender='Ж').find_clients(db1,clients_table)


print(db1.count_rows(clients_table))
Client(gender='Ж').delete_client(db1,clients_table)
print(db1.count_rows(clients_table))

Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')
Client.add_client_from_csv(db1, 'clients', 'found_clients_2.csv')
Client.add_client_from_csv(db1, 'clients', 'found_clients_1.csv')

print(db1.count_rows(clients_table))

db1.close_connection()
#################################################################


# # Клас для форми
# class Form:
#     def __init__(self):
#         self.client = Client()
#         self.conn = sqlite3.connect('bd.bd')
#
#     def open_file(self):
#         # Відкриття всіх клієнтів з бази
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM clients")
#         rows = cursor.fetchall()
#         result_message = self.client.save_to_csv(rows)  # Зберігаємо в CSV
#         dpg.set_value(content_label, result_message)
#
#     def search_client(self, sender, app_data):
#         # Отримуємо значення з полів форми
#         self.client.last_name = dpg.get_value(last_name_input)
#         self.client.first_name = dpg.get_value(first_name_input)
#         self.client.middle_name = dpg.get_value(middle_name_input)
#         self.client.gender = dpg.get_value(gender_choice)
#         self.client.birth_date = dpg.get_value(birth_date_picker)
#
#         # Пошук клієнтів у базі
#         results = self.client.search(self.conn)
#
#         # Збереження результатів у CSV
#         if results:
#             result_message = self.client.save_to_csv(results)
#             dpg.set_value(content_label, result_message)
#         else:
#             dpg.set_value(content_label, "Клієнтів не знайдено.")
#
#     def add_client(self, sender, app_data):
#         # Отримуємо значення з полів форми
#         self.client.last_name = dpg.get_value(last_name_input)
#         self.client.first_name = dpg.get_value(first_name_input)
#         self.client.middle_name = dpg.get_value(middle_name_input)
#         self.client.gender = dpg.get_value(gender_choice)
#         self.client.birth_date = dpg.get_value(birth_date_picker)
#
#         # Додаємо клієнта до бази даних
#         result_message = self.client.add_to_db(self.conn)
#         dpg.set_value(content_label, result_message)  # Вивести повідомлення про успіх
#
#     def delete_client(self, sender, app_data):
#         # Отримуємо значення з полів форми для пошуку
#         self.client.last_name = dpg.get_value(last_name_input)
#         self.client.first_name = dpg.get_value(first_name_input)
#         self.client.middle_name = dpg.get_value(middle_name_input)
#         self.client.gender = dpg.get_value(gender_choice)
#         self.client.birth_date = dpg.get_value(birth_date_picker)
#
#         # Видаляємо клієнта з бази
#         result_message = self.client.delete_from_db(self.conn)
#         dpg.set_value(content_label, result_message)
#
#
# # Створення основного вікна та елементів інтерфейсу
# def create_form():
#     form = Form()  # Створюємо об'єкт форми
#
#     dpg.create_context()
#
#     with dpg.handler_registry():
#         with dpg.window(label="Основне вікно", width=600, height=500):
#
#             # Кнопки з виправленим кольором
#             dpg.add_button(label="BD", callback=form.open_file, color=(0, 255, 0))  # Зелену
#             dpg.add_button(label="Find", callback=form.search_client, color=(0, 0, 255))  # Синій
#             dpg.add_button(label="Add", callback=form.add_client, color=(255, 165, 0))  # Оранжеву
#             dpg.add_button(label="Delete", callback=form.delete_client, color=(255, 0, 0))  # Червону
#
#             # Поля для вводу
#             dpg.add_text("Прізвище:")
#             global last_name_input
#             last_name_input = dpg.add_input_text(label="", width=200)
#
#             dpg.add_text("Ім'я:")
#             global first_name_input
#             first_name_input = dpg.add_input_text(label="", width=200)
#
#             dpg.add_text("По батькові:")
#             global middle_name_input
#             middle_name_input = dpg.add_input_text(label="", width=200)
#
#             # Вибір статі
#             dpg.add_text("Стать:")
#             global gender_choice
#             gender_choice = dpg.add_radio_button(items=["Чоловік", "Жінка"], default_value=0)
#
#             # Календар для вибору дати народження
#             dpg.add_text("Дата народження:")
#             global birth_date_picker
#             birth_date_picker = dpg.add_date_picker(default_value=datetime.date.today())
#
#             # Текст для виведення результату
#             global content_label
#             content_label = dpg.add_text("Вміст файлу з'явиться тут.", wrap=300, color=(255, 255, 255))
#
#     # Запуск основного циклу
#     dpg.create_viewport(title="Стильний інтерфейс", width=600, height=500)
#     dpg.setup_dearpygui()
#     dpg.show_viewport()
#     dpg.start_dearpygui()
#     dpg.destroy_context()
#
#
# create_form()



