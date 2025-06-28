def counter(func):
    cnt = 0
    def counter2(*args, **kwargs):
        nonlocal cnt
        cnt += 1
        #print(f"Функція викликана {cnt} разів")
        return cnt #func(*args, **kwargs)  # Не зобов'язує передавати параметри
    return counter2

@counter
def example_function():
    print("Inside the function")

example_function()  # Не передаємо параметри
