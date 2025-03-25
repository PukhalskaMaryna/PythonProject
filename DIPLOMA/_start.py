# опис того, з чого все починалось, кожен клас був початково створений, як порожній шаблон

#import бібліотеки

class DB:
    def __init__(self):
        """
        ініціалізуємо
        """
        pass

    def __str__(self):
        """
        вивід в принті
        """
        pass

    def delete_db(self):
        """
        метод для видалення бази даних, якщо вона існує
        """
        pass

    def open_connection(self):
        """
        відкриваємо з'єднання з базою даних, якщо файлу немає, він створюється
        """
        pass

    def close_connection(self):
        """
        закриваємо з'єднання з базою даних
        """
        pass

    def execute_query(self, query: str, params: tuple = ()):
        """
        виконання SQL-запиту до бази даних
        """
        pass

    def create_table(self, table_name: str, field_with_type: str):
        """
        створює таблицю в базі даних, якщо її ще немає
        """
        pass

    def drop_table(self, table_name: str):
        """
        видаляє таблицю з бази даних, якщо вона існує
        """
        pass

    def insert_into_table(self, table_name: str, row = tuple()):
        """
        додає новий рядок до вказаної таблиці
        """
        pass

    def delete_from_table(self, table_name: str, conditions: dict):
        """
        видаляє рядки з таблиці за заданими умовами
        """
        pass

    def truncate_table(self, table_name: str):
        """
        видаляє всі рядки з таблиці, залишаючи її порожньою
        """
        pass

    def count_rows(self, table_name):
        """
        повертає кількість рядків у вказаній таблиці
        """
        pass

    def print_all_rows(self, table_name: str):
        """
        виводить всі рядки з таблиці
        """
        pass
