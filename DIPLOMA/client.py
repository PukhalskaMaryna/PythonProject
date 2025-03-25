import csv
import os
from DIPLOMA.db import DB
from DIPLOMA.single_funcs import process_date

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
        return f"{self.last_name} {self.first_name} {self.middle_name} - {self.gender} - ДН {self.birth_date} - {'ДС' if self.death_date else ''} {self.death_date if self.death_date else 'живенький клієнт'}"

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

        result_sql = db.execute_query(f"SELECT * FROM {table}")  # Отримуємо всі записи

        clients = {}

        for row in result_sql:
            is_match = True  # Припускаємо, що клієнт підходить під умови

            # Перевірка прізвища
            if self.last_name:
                if self.last_name.lower() not in row[1].lower():  # Перевірка на часткові співпадіння
                    is_match = False

            # Перевірка імені
            if self.first_name:
                if self.first_name.lower() not in row[2].lower():  # Перевірка на часткові співпадіння
                    is_match = False

            # Перевірка по батькові
            if self.middle_name:
                if self.middle_name.lower() not in row[3].lower():  # Перевірка на часткові співпадіння
                    is_match = False

            # Перевірка статі
            if self.gender:
                if self.gender.lower() != row[4].lower():
                    is_match = False

            # Перевірка дати народження
            if self.birth_date:
                if self.birth_date != row[5]:  # Тут можна додати додаткову обробку дати
                    is_match = False

            # Перевірка дати смерті
            if self.death_date:
                if self.death_date != row[6]:  # Аналогічно
                    is_match = False

            # Якщо всі умови виконуються, додаємо клієнта
            if is_match:
                client_id = row[0]
                client = Client(
                    last_name=row[1],
                    first_name=row[2],
                    middle_name=row[3],
                    gender=row[4],
                    birth_date=row[5],
                    death_date=row[6]
                )
                clients.update({client_id: client})

        # Якщо потрібно експортувати в CSV
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