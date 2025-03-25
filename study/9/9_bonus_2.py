def multiply_even_numbers(numbers: list):
    """
    Помножує всі парні числа у списку на 2.

    :param numbers: Список чисел.
    :return: Новий список з парними числами, помноженими на 2.
    """

    result = list(i * 2 for i in numbers if i % 2 == 0)

    return result


# Перевірка
assert multiply_even_numbers([1, 2, 3, 4, 5, 6]) == [4, 8, 12]
