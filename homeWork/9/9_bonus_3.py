def factorial(num):
    """
    Обчислює факторіал числа num.

    :param num: Ціле число.
    :return: Факторіал числа num.
    """
    if num == 0:
        return 1
    else:
        return num * factorial(num - 1)

# Перевірка
assert factorial(5) == 120