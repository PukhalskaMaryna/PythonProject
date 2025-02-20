import tkinter as tk  # Імпортуємо бібліотеку Tkinter

# Створюємо головне вікно
root = tk.Tk()

# Налаштування головного вікна
root.title("Моє перше вікно")  # Задаємо заголовок вікна
root.geometry("300x250")  # Задаємо розміри вікна (ширина x висота)

# Функція для обробки натискання кнопки
def on_button_click():
    label.config(text="Обожнюю")  # Вивести текст "Обожнюю" у label
    # Малюємо сердечко на Canvas
    canvas.create_oval(50, 50, 100, 100, fill="red", outline="red")  # Ліва половина сердечка
    canvas.create_oval(100, 50, 150, 100, fill="red", outline="red")  # Правая половина сердечка
    canvas.create_polygon(50, 75, 150, 75, 100, 150, fill="red", outline="red")  # Нижня частина сердечка

# Створюємо кнопку
button = tk.Button(root, text="Натисни мене", command=on_button_click)  # Створюємо кнопку
button.pack(pady=10)  # Додаємо кнопку в вікно

# Створюємо Label для тексту
label = tk.Label(root, text="")
label.pack()

# Створюємо Canvas для малювання
canvas = tk.Canvas(root, width=200, height=150)
canvas.pack(pady=10)

# Запускаємо головний цикл
root.mainloop()


# сворене .exe зі своєю іконкою
# pyinstaller --onefile --windowed --icon="C:\Users\pukhalsk\Downloads\ico_4bn_4.ico" create_exe.py
