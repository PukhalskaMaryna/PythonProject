import sqlite3
import os

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
            self.open_connection()

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

        fields = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + field_with_type
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})"
        self.execute_query(query)

    def drop_table(self, table_name: str):
        """
        дроп таблиці

        :param table_name: Str, назва таблиці
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_query(query)

    def insert_into_table(self, table_name: str, row = tuple()):
        """
        вставка 1 рядка

        :param table_name: Str, назва таблиці бд, в яку додаємо дані
        :param row: tuple, значення для одного рядка по кожному полю, крім id
            приклад, ("Пухальська", "Марина", "Ж", "21.10.1983")
        """
        result = self.execute_query(f"SELECT MAX(id) FROM {table_name}")
        next_id = 1 if not result or result[0][0] is None else result[0][0] + 1

        columns_result = self.execute_query(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in columns_result]

        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
        self.execute_query(query, (next_id, *row))

    def delete_from_table(self, table_name: str, conditions: dict):
        """
        видалення рядка\рядків

        :param table_name: Str, назва таблиці бд, з якої видаляємо дані
        :param conditions: dict, словник з умовами видалення,
                приклад {'id': 1} або {'last_name': 'Пухальська', 'first_name': 'Марина'}
        """
        condition_strings = [f"{column} = ?" for column in conditions]
        params = list(conditions.values())
        condition_clause = " AND ".join(condition_strings)

        query = f"DELETE FROM {table_name} WHERE {condition_clause}"
        self.execute_query(query, tuple(params))

    def truncate_table(self, table_name: str):
        """
        видалення всіх рядків таблиці в межах бд

        :param table_name: str, назва таблиці, яку потрібно очистити
        """
        query = f"DELETE FROM {table_name}"
        self.execute_query(query)

    def count_rows(self, table_name):
        """
        к-ть рядків у таблиці

        :param table_name: Str, назва таблиці в базі даних
        :return: кількість рядків в таблиці
        """
        if not self.conn:
            self.open_connection()

        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        if result:
            count =  result[0][0]
            return count
        else:
            return 0

    # def print_all_rows(self, table_name: str):
    #     """
    #     Виводить всі рядки з вказаної таблиці в базі даних.
    #
    #     :param table_name: Str, назва таблиці в базі даних
    #     """
    #     query = f"SELECT * FROM {table_name}"
    #     result = self.execute_query(query)
    #
    #     if result:
    #         # Проходимо через всі рядки результату та виводимо кожен окремо
    #         for row in result:
    #             print(row)
    #     else:
    #         print(f"Таблиця {table_name} порожня або не існує.")