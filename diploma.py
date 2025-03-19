# import dearpygui.dearpygui as dpg
import sqlite3
import csv
import os

class DB:
    def __init__(self, db_file_name='db.db'):
        """
        Клас для роботи з базою даних

        :param db_file_name: str, назва файла бд, за замовчуванням db.db
        :param conn: підключення до б
        """
        self.db_file_name = db_file_name
        self.conn = None

    def __str__(self):
        return f"База даних: {self.db_file_name}"

    def delete_db(self):
        """
        Видалення файлу бд
        Перевіряється, чи існує файл, і якщо так, він видаляється.
        """
        if os.path.exists(self.db_file_name):
            os.remove(self.db_file_name)
            print(f"База даних {self.db_file_name} успішно видалена")
        else:
            print(f"База даних {self.db_file_name} не знайдена")

    def open_connection(self):
        """
        Підключення до бд
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
        """
        self.conn = sqlite3.connect(self.db_file_name)

    def close_connection(self):
        """Закриття з'єднання з бд"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("З'єднання з бд успішно закрите")
        else:
            print("З'єднання вже було закрите раніше")

    def create_table(self, table, fields):
        """
        Створення таблиці з зазначеними полями.

        :param table: Str, назва таблиці
        :param fields: dict, словник з полями та їх типами
        приклад:
        fields = {
                    'title': 'TEXT NOT NULL',
                    'year': 'INTEGER NOT NULL',
                    'director': 'TEXT',
                }
        """
        field_definitions = []
        for field, field_type in fields.items():
            field_definitions.append(f"{field} {field_type}")

        # Додаємо поле id як PRIMARY KEY
        field_definitions.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
        query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(field_definitions)})"
        self.execute_query(query)

    def drop_table(self, table):
        """
        Створення таблиці з зазначеними полями.

        :param table: Str, назва таблиці
        """
        query = f"DROP TABLE IF EXISTS {table}"
        self.execute_query(query)

    def insert_into_table(self, table, row):
        """
        Метод для вставки одного рядка

        :param table: Str, назва таблиці бд, в яку додаємо дані
        :param row: tuple, кортеж значень для одного рядка (без id)
        """
        if self.conn is None:
            print("Не встановлено підключення")
            return None

        try:
            my_cursor = self.conn.cursor()  # Створення курсора
            my_cursor.execute(f"SELECT MAX(id) FROM {table}")
            result = my_cursor.fetchone()
            next_id = result[0] + 1 if result[0] is not None else 1

            # Додаємо поле id до значень для вставки (row)
            row_with_id = (next_id,) + row

            my_cursor.execute(f"INSERT INTO {table} VALUES({', '.join(['?'] * len(row_with_id))})", row_with_id)
            self.conn.commit()  # Збереження змін
            my_cursor.close()  # Закриваємо курсор після завершення

        except sqlite3.Error as sql_error:
            print(f"Помилка виконання запиту: {sql_error}")
            # приклади помилок:
            # sqlite3.ProgrammingError - невірна к-ть полів
            # sqlite3.IntegrityError - якщо вставити значення в унікальне поле (у нас це id)
            # sqlite3.DatabaseError - проблема доступу до бд
            # sqlite3.DataError - спроба вставити невірний тип даних

    def delete_from_table(self, table, conditions):
        """
        Метод видалення

        :param table: Str, назва таблиці бд, з якої видаляємо дані
        :param conditions: dict, словник з умовами видалення,
                напр. {'id': 1} або {'last_name': 'Пухальська', 'first_name': 'Марина'}
        """
        if self.conn is None:
            print("Не встановлено підключення")
            return None

        try:
            my_cursor = self.conn.cursor()  # Створення курсора
            condition_strings = []
            params = []
            for column, value in conditions.items():
                condition_strings.append(f"{column} = ?")
                params.append(value)
            condition_clause = " AND ".join(condition_strings)
            query = f"DELETE FROM {table} WHERE {condition_clause}"
            my_cursor.execute(query, params)
            self.conn.commit()
            my_cursor.close()

        except sqlite3.Error as sql_error:
            print(f"Помилка виконання запиту: {sql_error}")

    def truncate_table(self, table_name):
        """
        Очищення всіх даних

        :param table_name: str, назва таблиці, яку потрібно очистити
        """
        if self.conn is None:
            print("Не встановлено підключення")
            return None

        try:
            my_cursor = self.conn.cursor()  # Створення курсора
            query = f"DELETE FROM {table_name}"  # SQL-запит для очищення таблиці
            my_cursor.execute(query)  # Виконання запиту
            self.conn.commit()  # Збереження змін
            my_cursor.close()  # Закриття курсора
            print(f"Таблиця {table_name} успішно очищена.")
        except sqlite3.Error as sql_error:
            print(f"Помилка виконання запиту: {sql_error}")

    def execute_query(self, query, params=()):
        """
        Метод запиту до бази даних
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute

        :param query: str, SQL-запит
        :param params: tuple, параметри для запиту
        :return: результат виконання запиту
        """
        if self.conn is None:
            print("Не встановлено підключення")
            return None

        try:
            cursor = self.conn.cursor()  # Створення курсора
            cursor.execute(query, params)  # Виконання запиту
            self.conn.commit()  # Збереження змін
            result = cursor.fetchall()  # Отримання результатів запиту
            cursor.close()  # Закриваємо курсор після завершення
            return result # Список кортежів-рядків бд
        except sqlite3.Error as sql_error:
            print(f"Помилка виконання запиту: {sql_error}")
            return None

    def count_rows(self, table_name):
        """
        Підрахунок кількості рядків у таблиці.

        :param table_name: Str, назва таблиці в базі даних
        :return: кількість рядків в таблиці
        """
        if self.conn is None:
            print("Не встановлено підключення")

        try:
            my_cursor = self.conn.cursor()  # Створення курсора
            query = f"SELECT COUNT(*) FROM {table_name}"  # SQL-запит для підрахунку рядків
            my_cursor.execute(query)  # Виконання запиту
            row_count = my_cursor.fetchone()[0]  # Отримуємо результат (кількість рядків)
            my_cursor.close()  # Закриваємо курсор після завершення
            return row_count
        except sqlite3.Error as sql_error:
            print(f"Помилка виконання запиту: {sql_error}")

#################################################################
db1 = DB('db.db')

# print(db1)
db1.open_connection()
db1.drop_table('clients')
db1.create_table('clients',{'last_name':'TEXT','first_name':'TEXT','middle_name':'TEXT','gender':'TEXT','birth_date':'DATE'})

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

    def add_client(self, db = DB(), table = str(), import_from_csv=True):
        """
        Додавання клієнта

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        :param import_from_csv: bool, якщо True, додає клієнтів з csv
        :return: None
        """
        if import_from_csv:
            with open('clients.csv', newline='', encoding='utf-8') as csvfile:
                for row in csv.DictReader(csvfile):
                    client_row = (
                        row["last_name"],
                        row["first_name"],
                        row["middle_name"],
                        row["gender"],
                        row["birth_date"]
                    )
                    db.insert_into_table(table, client_row)
        else:
            row = (self.last_name, self.first_name, self.middle_name, self.gender, self.birth_date)
            db.insert_into_table(table, row)

    def search_clients(self, db = DB(), table = str(), export_to_csv=True):
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
            conditions.append("birth_date = ?")
            params.append(self.birth_date)

        if not conditions:
            print("Не задано жодного параметра для пошуку.")
            return []

        condition_clause = " AND ".join(conditions)
        result = db.execute_query(f"SELECT * FROM {table} WHERE {condition_clause}", tuple(params))

        clients = {}
        for row in result:
            client = Client(
                last_name   =row[1],
                first_name  =row[2],
                middle_name =row[3],
                gender      =row[4],
                birth_date  =row[5]
            )
            client_id = row[0]
            clients.update({client_id: client})

        if export_to_csv: # експорт у csv
            file_name = 'found_clients.csv'
            i = 1
            while os.path.exists(file_name): #якщо файл з такою назвою є, то додає цифру
                file_name = f'found_clients_{i}.csv'
                i += 1

            with open(file_name, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["last_name", "first_name", "middle_name", "gender", "birth_date"])
                for client_id,client in clients.items():
                    writer.writerow([client_id, client.last_name, client.first_name
                                        , client.middle_name, client.gender,client.birth_date])
        return clients

    def delete_client(self, db = DB(), table = str()):
        """
        Видалення клієнтів з таблиці на основі атрибутів цього клієнта.
        Використовує метод search_clients для пошуку клієнтів перед їх видаленням.

        :param db: DB, підключення до бази даних
        :param table: str, назва таблиці
        """
        # Пошук клієнтів за атрибутами цього клієнта
        clients_to_delete = self.search_clients(db, table, export_to_csv=False)

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

cl1.add_client(db1,clients_table,False)
cl2.add_client(db1,clients_table,False)
cl3.add_client(db1,clients_table,False)

cl1.search_clients(db1,clients_table)
Client(gender='Ж').search_clients(db1,clients_table)
Client(gender='Ч').search_clients(db1,clients_table)
Client(birth_date='21.10.1983',gender='Ж').search_clients(db1,clients_table)


print(db1.count_rows(clients_table))
Client(gender='Ж').delete_client(db1,clients_table)
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
