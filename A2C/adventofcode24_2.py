import math
from typing import Tuple


class Plane:
    def __init__(self, point: Tuple[float, float, float], normal: Tuple[float, float, float]):
        """
        Ініціалізує площину, задану точкою та нормальним вектором.

        :param point: Точка на площині (x, y, z).
        :param normal: Нормальний вектор до площини (nx, ny, nz).
        """
        self.point = point
        self.normal = normal

    def __repr__(self):
        return f"Plane(Point: {self.point}, Normal: {self.normal})"

    def multiply_sets(self, other: "Plane") -> "Line":
        """
        Знаходить пряму перетину двох площин, якщо така існує.

        :param other: Інша площина.
        :return: Об'єкт класу Line, що представляє пряму перетину двох площин.
        :raises ValueError: Якщо площини паралельні і не перетинаються.
        """
        # Визначення напрямного вектора прямої перетину (векторний добуток нормалей площин)
        normal1 = self.normal
        normal2 = other.normal

        # Визначаємо вектор, що є вектором напрямку прямої перетину
        cross_product = (
            normal1[1] * normal2[2] - normal1[2] * normal2[1],  # x
            normal1[2] * normal2[0] - normal1[0] * normal2[2],  # y
            normal1[0] * normal2[1] - normal1[1] * normal2[0]  # z
        )

        # Якщо вектор напрямку прямої перетину нульовий, то площини паралельні або однакова, перетину немає
        if cross_product == (0, 0, 0):
            raise ValueError("Площини паралельні або однакові, перетину немає.")

        # Знаходимо точку перетину двох площин
        # Виписуємо рівняння площин:
        #   A1*x + B1*y + C1*z = D1  (для першої площини)
        #   A2*x + B2*y + C2*z = D2  (для другої площини)
        # Розв'язуємо систему лінійних рівнянь для визначення точки перетину

        x1, y1, z1 = self.point
        x2, y2, z2 = other.point

        # Параметри площин
        A1, B1, C1 = self.normal
        A2, B2, C2 = other.normal

        # Розв'язуємо рівняння для визначення параметра t
        denominator = A1 * B2 - B1 * A2
        if denominator == 0:
            raise ValueError("Не можна знайти точку перетину, перевірте площини.")

        # Для спрощення розв'язку, припустимо, що точка перетину буде на прямій
        t = ((x1 - x2) * B2 - (y1 - y2) * A2) / denominator

        # Тепер знаходимо точку на прямій перетину
        intersection_point = (x1 + t * A1, y1 + t * B1, z1 + t * C1)

        # Повертаємо об'єкт типу Line для прямої перетину
        direction = cross_product  # напрямний вектор для прямої перетину
        return Line(intersection_point, direction)

    def intersection_with_line(self, line: "Line") -> Tuple[float, float, float]:
        """
        Знаходить точку перетину площини та прямої, якщо така є.

        :param line: Об'єкт класу Line, що представляє пряму.
        :return: Точка перетину площини та прямої.
        :raises ValueError: Якщо пряма паралельна площині або не перетинається з нею.
        """
        # Напрямний вектор прямої
        line_direction = line.direction
        # Точка на прямій
        line_point = line.point

        # Нормаль площини
        normal = self.normal

        # Перевіряємо, чи пряма паралельна площині
        dot_product = sum([line_direction[i] * normal[i] for i in range(3)])
        if dot_product == 0:
            raise ValueError("Пряма паралельна площині і не перетинається з нею.")

        # Розв'язуємо для параметра t (відстань по прямій до точки перетину)
        x0, y0, z0 = self.point
        x1, y1, z1 = line_point

        t = ((x0 - x1) * normal[0] + (y0 - y1) * normal[1] + (z0 - z1) * normal[2]) / dot_product

        # Знаходимо точку перетину на прямій
        intersection_point = line.get_parametric_equation(t)
        return intersection_point

    def are_parallel(self, other: "Plane") -> bool:
        """
        Перевіряє, чи є дві площини паралельними.

        :param other: Інша площина.
        :return: True, якщо площини паралельні, False, якщо не паралельні.
        """
        # Площини паралельні, якщо їх нормальні вектори лінійно залежні
        normal1 = self.normal
        normal2 = other.normal
        return normal1[0] * normal2[1] == normal1[1] * normal2[0] and normal1[0] * normal2[2] == normal1[2] * normal2[
            0] and normal1[1] * normal2[2] == normal1[2] * normal2[1]

    def is_parallel_to_line(self, line: "Line") -> bool:
        """
        Перевіряє, чи є площина паралельною прямій.

        :param line: Пряма, яку перевіряємо на паралельність з площиною.
        :return: True, якщо площина паралельна прямій, False, якщо не паралельна.
        """
        normal = self.normal
        direction = line.direction
        dot_product = sum([normal[i] * direction[i] for i in range(3)])
        return dot_product == 0


class Line:
    def __init__(self, point: Tuple, direction: Tuple):
        """
        Ініціалізує пряму, задану точкою та напрямним вектором.

        :param point: Точка на прямій (x, y, z).
        :param direction: Напрямний вектор прямої (dx, dy, dz).
        """
        self.point = point
        self.direction = direction

    def get_parametric_equation(self, t: int) -> Tuple[float, float, float]:
        """
        Отримує точку на прямій для певного значення параметра t.

        :param t: Ціле невід'ємне число, параметр прямої.
        :return: Точка (x, y, z) на прямій для даного t.
        """
        x = self.point[0] + t * self.direction[0]
        y = self.point[1] + t * self.direction[1]
        z = self.point[2] + t * self.direction[2]
        return (x, y, z)

    def __repr__(self):
        return f"Line(Point: {self.point}, Direction: {self.direction})"

    def are_parallel(self, other: "Line") -> bool:
        """
        Перевіряє, чи є дві прямі паралельними.

        :param other: Інша пряма.
        :return: True, якщо прямі паралельні, False, якщо не паралельні.
        """
        # Прямі паралельні, якщо їх напрямні вектори лінійно залежні
        direction1 = self.direction
        direction2 = other.direction
        return direction1[0] * direction2[1] == direction1[1] * direction2[0] and direction1[0] * direction2[2] == \
            direction1[2] * direction2[0] and direction1[1] * direction2[2] == direction1[2] * direction2[1]

    def are_skew(self, other: "Line") -> bool:
        """
        Перевіряє, чи є дві прямі мимобіжними.

        :param other: Інша пряма.
        :return: True, якщо прямі мимобіжні, False, якщо вони перетинаються або паралельні.
        """
        # Якщо прямі не паралельні та не перетинаються, вони мимобіжні
        try:
            self.multiply(other)
            return False  # Прямі перетинаються, тому не мимобіжні
        except ValueError:
            return True  # Прямі мимобіжні

    def find_plane(self, other: "Line") -> "Plane":
        """
        Знаходить площину, що проходить через дві прямі, якщо вони не мимобіжні.

        :param other: Інша пряма.
        :return: Об'єкт класу Plane, що представляє площину, яка проходить через ці дві прямі.
        :raises ValueError: Якщо прямі є паралельними або мимобіжними.
        """
        # Перевірка на паралельність
        if self.are_parallel(other):
            raise ValueError("Прямі паралельні, площина не визначена.")

        # Визначаємо вектор напрямку для кожної прямої
        direction1 = self.direction
        direction2 = other.direction

        # Векторний добуток напрямних векторів для знаходження нормалі площини
        normal = (
            direction1[1] * direction2[2] - direction1[2] * direction2[1],  # x
            direction1[2] * direction2[0] - direction1[0] * direction2[2],  # y
            direction1[0] * direction2[1] - direction1[1] * direction2[0]  # z
        )

        # Точка на площині, яку можна вибрати як точку з будь-якої з прямих
        point_on_plane = self.point

        # Повертаємо об'єкт класу Plane з отриманими параметрами
        return Plane(point_on_plane, normal)

def read_lines_from_file(file_path: str) -> list:
    """
    Читання файлу та створення об'єктів класу Line з кожного рядка.

    :param file_path: Шлях до текстового файлу.
    :return: Список об'єктів класу Line.
    """
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            # Читаємо кожен рядок, розділяючи числа через кому
            parts = line.strip().split(',')
            # Перетворюємо значення на числа з плаваючою комою
            x, y, z, dx, dy, dz = map(float, parts)
            # Створюємо об'єкт класу Line та додаємо його до списку
            lines.append(Line((x, y, z), (dx, dy, dz)))

    return lines


def find_first_non_skew(lines: list) -> Tuple[Line, Line]:
    """
    Знаходить першу пару прямих, які не є мимобіжними.

    :param lines: Список об'єктів класу Line.
    :return: Перша пара прямі, які не є мимобіжними, як кортеж з двох об'єктів Line.
    :raises ValueError: Якщо всі прямі мимобіжні.
    """
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if not lines[i].are_skew(lines[j]):
                return lines[i], lines[j]
    raise ValueError("Всі прямі є мимобіжними.")


