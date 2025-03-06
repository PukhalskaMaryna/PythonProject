def calculator(num1, num2, operation):
    """
    Реалізує простий калькулятор для двох чисел.

    :param num1: Перше число.
    :param num2: Друге число.
    :param operation: Операція (додавання, віднімання, множення, ділення).
    :return: Результат операції.
    """
    operation_dict = {'add': num1 + num2,
            'subtract': num1 - num2,
            'multiply': num1 * num2,
            'divide': num1 / num2
            }

    return 0 if not operation in operation_dict else operation_dict[operation]

# Перевірка
assert calculator(5, 3, 'add') == 8
print('OK')