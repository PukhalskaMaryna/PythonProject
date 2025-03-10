def add_decorator(number):
    """
    Реалізує декоратор, який змінює поведінку функції, додаючи до результату функції число.

    :param number: Число для додавання.
    :return: Декоратор для додавання числа до результату функції.
    """
    def decorator(func,*args, **kwargs):
        def wrapper(*args, **kwargs):
            # Викликаємо оригінальну функцію і додаємо до її результату число
            result = func(*args, **kwargs)
            return result + number
        return wrapper
    return decorator

@add_decorator(5)
def example_function(x):
    return x * 2

# Перевірка
assert example_function(2) == 9  # 2 * 2 + 5 = 9
