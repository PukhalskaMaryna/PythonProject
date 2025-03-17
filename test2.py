import tkinter as tk
from tkinter import messagebox
import json
import os


# Функції для роботи з файлом BD.json

def load_data_from_file():
    """Завантажує дані з файлу BD.json"""
    if os.path.exists("BD.json"):
        with open("BD.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return []


def save_data_to_file(data):
    """Зберігає дані у файл BD.json"""
    with open("BD.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Клас для основної форми
class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Головне меню")

        # Розміщення кнопок у два ряди
        self.add_button = tk.Button(self.root, text="Додати", command=self.open_add_form)
        self.edit_button = tk.Button(self.root, text="Змінити", command=self.open_edit_form)
        self.delete_button = tk.Button(self.root, text="Видалити", command=self.open_delete_form)

        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.edit_button.grid(row=0, column=1, padx=10, pady=10)
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.grid(row=1, column=0, columnspan=3, pady=10)

    def open_add_form(self):
        self.open_form("add")

    def open_edit_form(self):
        self.open_form("edit")

    def open_delete_form(self):
        self.open_form("delete")

    def open_form(self, action):
        form = FormWindow(self.root, action)
        self.root.wait_window(form.top)  # Чекаємо закриття форми

    def exit_program(self):
        self.root.quit()  # Закриває головне вікно та завершує програму


# Клас для форми, де відбуваються введення даних
class FormWindow:
    def __init__(self, parent, action):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Форма: {action.capitalize()} запис")

        self.action = action

        self.name_label = tk.Label(self.top, text="Ім'я:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.top)
        self.name_entry.grid(row=0, column=1)

        self.year_label = tk.Label(self.top, text="Рік:")
        self.year_label.grid(row=1, column=0)
        self.year_entry = tk.Entry(self.top)
        self.year_entry.grid(row=1, column=1)

        self.gender_label = tk.Label(self.top, text="Стать:")
        self.gender_label.grid(row=2, column=0)

        # Випадаючий список для вибору статі
        self.gender_var = tk.StringVar()
        self.gender_dropdown = tk.OptionMenu(self.top, self.gender_var, "Ч", "Ж")
        self.gender_var.set("Ч")  # За замовчуванням Ч
        self.gender_dropdown.grid(row=2, column=1)

        # Розміщення кнопок Enter та Exit поряд
        self.button_frame = tk.Frame(self.top)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.submit_button = tk.Button(self.button_frame, text="Enter", command=self.submit_form, bg="green",
                                       fg="white")
        self.submit_button.grid(row=0, column=0, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_form, bg="red", fg="white")
        self.exit_button.grid(row=0, column=1, padx=10)

    def submit_form(self):
        name = self.name_entry.get()
        year = self.year_entry.get()
        gender = self.gender_var.get()

        if not name or not year or not gender:
            self.show_error("ERROR", "Будь ласка, заповніть всі поля.")
            return

        # Перевірка та перетворення року на ціле число
        try:
            year = int(year)
        except ValueError:
            self.show_error("ERROR", "Рік має бути числом.")
            return

        # Завантажуємо дані з файлу
        data = load_data_from_file()

        # Залежно від дії, додамо, змінимо або видалимо записи
        if self.action == "add":
            data.append({"name": name, "year": year, "gender": gender})
            save_data_to_file(data)
            self.show_success("ОК", "Запис додано.")
        elif self.action == "edit":
            updated = False
            for record in data:
                if record["name"].lower() == name.lower():
                    record["year"] = year
                    record["gender"] = gender
                    updated = True
            if updated:
                save_data_to_file(data)
                self.show_success("ОК", "Запис оновлено.")
            else:
                self.show_error("ERROR", "Запис не знайдено.")
        elif self.action == "delete":
            data = [record for record in data if record["name"].lower() != name.lower()]
            save_data_to_file(data)
            self.show_success("ОК", "Запис(и) видалено.")

        # Закриваємо форму
        self.top.destroy()

    def exit_form(self):
        self.top.destroy()  # Закриває поточну форму

    def show_success(self, title, message):
        messagebox.showinfo(title, message, icon='info', background='green')

    def show_error(self, title, message):
        messagebox.showerror(title, message, icon='error', background='red')



if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()
