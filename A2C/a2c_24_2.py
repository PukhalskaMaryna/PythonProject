from typing import Tuple
import re

class Point:
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        точка

        :param x: Координата x точки.
        :param y: Координата y точки.
        :param z: Координата z точки.
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

class Plane:
    def __init__(self, point: Point, normal: Tuple[float, float, float]):
        """
        визначаємо площину, задану точкою та нормальним вектором.

        :param point: Точка на площині.
        :param normal: нормальний вектор до площини (nx, ny, nz).
        """
        self.point = point
        self.normal = normal

    def __str__(self):
        return f"Plane(Point: {self.point}, Normal: {self.normal})"

    def cross_with_plane(self, other: "Plane") -> "Line" or None:
        """
        пряма перетину площин

        :param other: Інша площина
        :return: Об'єкт класу Line, що представляє пряму перетину двох площин
        :raises ValueError: Якщо площини паралельні та не перетинаються
        """
        # Визначення напрямного вектора прямої перетину (векторний добуток нормалей площин)
        normal1 = self.normal
        normal2 = other.normal

        # Визначаємо вектор, що є вектором напрямку прямої перетину
        cross_product = (
            normal1[1] * normal2[2] - normal1[2] * normal2[1],
            normal1[2] * normal2[0] - normal1[0] * normal2[2],
            normal1[0] * normal2[1] - normal1[1] * normal2[0]
        )

        # Якщо вектор напрямку прямої перетину нульовий, то площини паралельні або однакова, перетину немає
        if cross_product == (0, 0, 0):
            return None

        # Витягуємо координати точок
        x1, y1, z1 = self.point.x, self.point.y, self.point.z
        x2, y2, z2 = other.point.x, other.point.y, other.point.z

        # Параметри площин
        a1, b1, c1 = self.normal
        a2, b2, c2 = other.normal

        # Розв'язуємо рівняння для визначення параметра t
        denominator = a1 * b2 - b1 * a2
        if denominator == 0:
            raise ValueError("не перетинаються")

        # точка перетину
        t = ((x1 - x2) * b2 - (y1 - y2) * a2) / denominator

        # Перевірка чи t є цілим числом
        if not t.is_integer():
            raise ValueError(f"Параметр t={t} не є цілим числом.")

        # Тепер знаходимо точку на прямій перетину
        intersection_point = Point(x1 + t * a1, y1 + t * b1, z1 + t * c1)

        # Перевірка чи точка має цілі координати
        if not (
                intersection_point.x.is_integer() and intersection_point.y.is_integer() and intersection_point.z.is_integer()):
            raise ValueError(f"Точка перетину {intersection_point} не має цілих координат.")

        # об'єкт Line для прямої перетину
        direction = cross_product
        return Line(intersection_point, direction)

    def is_parallel_to_line_or_all_line_on_plane(self, my_line: "Line") -> bool:
        """
        чи є площина паралельна до прямої

        :param my_line: Пряма, яку перевіряємо на паралельність з площиною
        :return: True, якщо площина паралельна прямій, False, якщо не паралельна
        """
        normal = self.normal
        direction = my_line.direction
        return sum([normal[i] * direction[i] for i in range(3)]) == 0

    def cross_with_line(self, my_line: "Line") -> Point or None:
        """
        точка перетину площини та прямої, якщо така є

        :param my_line: Об'єкт класу Line, що представляє пряму
        :return: Точка перетину площини та прямої або None
        """

        # параметри площини
        x1, y1, z1 = self.point.x,self.point.y,self.point.z
        nx, ny, nz = self.normal[0],self.normal[1],self.normal[2]

        # параметри прямої
        x2, y2, z2 = my_line.point.x,my_line.point.y,my_line.point.z
        dx, dy, dz = my_line.direction[0],my_line.direction[1],my_line.direction[2]

        # t
        t_num = nx * (x1 - x2) + ny * (y1 - y2) + nz * (z1 - z2)
        t_den = nx * dx + ny * dy + nz * dz

        # Якщо знаменник не дорівнює нулю, знайдемо t
        if t_den != 0:
            t = t_num / t_den

            x = x2 + t * dx
            y = y2 + t * dy
            z = z2 + t * dz

            my_point = Point(x,y,z)
        else:
            my_point = None

        return my_point

    def are_parallel(self, other: "Plane") -> bool:
        """
        чи є дві площини паралельними

        :param other: Інша площина.
        :return: True, якщо площини паралельні, False, якщо не паралельні.
        """
        # Площини паралельні, якщо їх нормальні вектори лінійно залежні
        normal1 = self.normal
        normal2 = other.normal
        return normal1[0] * normal2[1] == normal1[1] * normal2[0] and normal1[0] * normal2[2] == normal1[2] * normal2[0] and normal1[1] * normal2[2] == normal1[2] * normal2[1]


class Line:
    def __init__(self, point: Point, direction: Tuple[float, float, float]):
        """
        пряма, задана точкою та напрямним вектором

        :param point: Точка на прямій
        :param direction: Напрямний вектор прямої (dx, dy, dz)
        """
        self.point = point
        self.direction = direction

    def __str__(self):
        return f"Line(Point: {self.point}, Direction: {self.direction})"

    def __eq__(self, other):
        return (self.point == other.point) and (self.direction == other.direction)

    def get_point_in_moment_time(self, t: float) -> Point:
        """
        точка на прямій для певного значення параметра t

        :param t: Ціле невід'ємне число, параметр прямої
        :return: Точка (x, y, z) на прямій для даного t
        """
        x = self.point.x + t * self.direction[0]
        y = self.point.y + t * self.direction[1]
        z = self.point.z + t * self.direction[2]
        return Point(x, y, z)

    def location_with_other_line(self, other: "Line") -> int:
        """
        взаємне розташування 2-х прямих

        :param other: Інша пряма
        :return: int 1 - збігаються, 2 - паралельні, 3 - мимобіжні, 4 - є 1 точка перетину
        """
        x1, y1, z1 = self.point.x, self.point.y, self.point.z
        x2, y2, z2 = other.point.x, other.point.y, other.point.z


        u1, u2, u3 = self.direction
        v1, v2, v3 = other.direction

        if u1 * v2 == v1 * u2 and u2 * v3 == u3 * v2:
            if u2 * (x2 - x1) == u1 * (y2 - y1) and u2 * (z2 - z1) == u3 * (y2 - y1):
                return 1
            else:
                return 2
        elif det3x3(self.direction, other.direction, (x2-x1, y2-y1, z2-z1)) != 0:
            return 3
        else:
            return 4

    # def are_parallel(self, other: "Line") -> bool:
    #     """
    #     чи є дві прямі паралельними
    #
    #     :param other: Інша пряма.
    #     :return: True, якщо прямі паралельні, False, якщо не паралельні.
    #     """
    #     direction1 = self.direction
    #     direction2 = other.direction
    #     return direction1[0] * direction2[1] == direction1[1] * direction2[0] and direction1[0] * direction2[2] == \
    #         direction1[2] * direction2[0] and direction1[1] * direction2[2] == direction1[2] * direction2[1]
    #
    def multiply(self, other: "Line") -> Point or None:
        """
        знаходимо точку перетину

        :param other: Інша пряма
        :return: Точка перетину двох прямих, якщо вони не паралельні
        :raises ValueError: Якщо прямі паралельні
        """
        if self.location_with_other_line(other) in (1,2,3):
            return None

        # Напрямні вектори обох прямих
        a1, b1, c1 = self.direction
        a2, b2, c2 = other.direction

        # # Визначаємо визначник матриці для обчислення t1 і t2
        # det = a1 * b2 - a2 * b1 #8
        # if det == 0:
        #     return None

        # Визначаємо параметр t
        if a2 - a1 == 0 and b2 - b1 == 0 and c2 - c1 == 0:
            return None
        elif a2 - a1 != 0:
            t = (self.point.x - other.point.x) / (a2 - a1)
        elif b2 - b1 != 0:
            t = (self.point.y - other.point.y) / (b2 - b1)
        else:
            t = (self.point.z - other.point.z) / (c2 - c1)

        if int(t) != t:
            return None
        # Знаходимо точку перетину
        intersection_point = Point(int(self.point.x + t * a1), int(self.point.y + t * b1), int(self.point.z + t * c1))

        return intersection_point
    #
    # def are_skew(self, other: "Line") -> bool:
    #     """
    #     чи є прямі мимобіжні
    #
    #     :param other: Інша пряма.
    #     :return: True, якщо прямі мимобіжні, False, якщо вони перетинаються або паралельні.
    #     """
    #     try:
    #         self.multiply(other)
    #         return False
    #     except ValueError:
    #         return True

    def find_plane_with_another_line(self, other: "Line") -> Plane or None:
        """
        Пошук площини, яка проходить через цю пряму та іншу пряму.

        :param other: Інша пряма.
        :return: Площина, що проходить через ці дві прямі.
        :raises ValueError: Якщо прямі мимобіжні.
        """
        # Отримуємо напрямні вектори двох прямих
        direction1 = self.direction
        direction2 = other.direction
        print(direction1, direction2)
        # Перевіряємо, чи прямі мимобіжні
        if self.location_with_other_line(other) == 3:
            return None
        elif self.location_with_other_line(other) == 2:
            direction2 = (other.point.x- self.point.x, other.point.y - self.point.y, other.point.z - self.point.z)
        elif self.location_with_other_line(other) == 1:
            raise "Something went wrong"

        print(direction1, direction2)
        # Векторний добуток напрямних векторів для визначення нормалі площини
        normal = (
            direction1[1] * direction2[2] - direction1[2] * direction2[1],  # x
            direction1[2] * direction2[0] - direction1[0] * direction2[2],  # y
            direction1[0] * direction2[1] - direction1[1] * direction2[0]  # z
        )
        print(normal)
        point_on_plane = self.point

        # Повертаємо площину, що визначена цією точкою і нормаллю
        return Plane(point_on_plane, normal)

def read_lines_from_file(txt_file_name: str) -> list:
    """
    читання з файлу та створення об'єктів класу Line з кожного рядка

    :param txt_file_name: Шлях до текстового файлу.
    :return: Список об'єктів класу Line.
    """
    lines_list = []

    with open(txt_file_name, 'r') as file:
        for l in file:
            parts = re.split('[,@]', l.strip())
            x, y, z, dx, dy, dz = map(float, parts)
            point = Point(x, y, z)
            direction = (dx, dy, dz)
            lines_list.append(Line(point, direction))

    return lines_list

def find_first_non_skew(lines_list: list) -> list:
    """
    перша пара прямих, які не є мимобіжними

    :param lines_list: Список об'єктів класу Line
    :return: Перша пара прямих, які не є мимобіжними, як кортеж з двох об'єктів Line
    :raises ValueError: Якщо всі прямі мимобіжні
    """
    for i in range(len(lines_list)):
        for j in range(i + 1, len(lines_list)):
            if lines_list[i].location_with_other_line(lines_list[j]) != 3:
                return [lines_list[i], lines_list[j]]
    raise ValueError("всі є мимобіжними")

def get_point_from_other_point(my_point: "Point", direction: Tuple[float, float, float]) -> Point:
    """
    за вектором від нашої точки знаходимо іншу точку

    :param my_point: Початкова точка
    :param direction: Напрямний вектор прямої (dx, dy, dz)
    :return: Точка, в якій опиниться наша точка після руху по вказаному вектору
    """
    return Point(my_point.x + direction[0],my_point.y + direction[1],my_point.z + direction[2])

def det3x3(v1:tuple, v2:tuple, v3:tuple):
    return (v1[0] * v2[1] * v3[2]) + (v1[2] * v2[0] * v3[1]) + (v1[1] * v2[2] * v3[0]) - (v1[2] * v2[1] * v3[0]) - (v1[1] * v2[0] * v3[2]) - (v1[0] * v2[2] * v3[1])

# # test skew
# # 1 - all skew
# # 2 - find two lines not skew
#
# # файл з даними
file_path = 'part24_2.txt'
#
# # список всіх прямих із файла
list_of_all_lines = read_lines_from_file(file_path)
#
# # список із 2-х прямих, які лежать в одній площині
# list_lines_on_one_plane = find_first_non_skew(read_lines_from_file(file_path))
#
# # у змінні записуємо ці прямі
# line_1 = list_lines_on_one_plane[0]
# line_2 = list_lines_on_one_plane[1]
# # print(f"{line_1},{line_2}")
#
# # шукаємо площину, яка визначається цими прямими
# my_plane = line_1.find_plane_with_another_line(line_2)
#
# # всі інші прямі або належать цій площині або перетинають її,
# # але не можуть бути паралельними до площини
# # назвемо пряму, що шукаємо my_line
# # вона повинна лежати у площині my_plane,
# # бо інакше вона не перетне обидві прямі line_1 і line_2 в різних точках
#
# # шукаємо, чи є серед інших прямих та, яка не лежить в площині, а перетинає її в точці
# # шукаємо, чи є серед інших прямих та, яка не лежить в площині, а перетинає її в точці
# # якщо є - джек-пот, в нас буде готова точка, через яку точно проходить розшукувана пряма
#
# cross_point = None
#
# for l in list_of_all_lines:
#     if l == line_1 or l == line_2: # не беремо в розрахунок вже знайдені прямі
#         continue
#     else:
#         cross_point = my_plane.cross_with_line(l) # точка перетину l і my_plane
#         line_3: "Line" = l
#         # if cross_point and isinstance(cross_point.x, int) and isinstance(cross_point.y, int) and isinstance(cross_point.z, int):
#         #     break
#         # else:
#         #     cross_point = None
#
#
# #cross_point_line_1_and_line_2 = line_1.multiply(line_2)
#
# print (line_1)
# print (line_2)
# #print (cross_point_line_1_and_line_2)
# print (my_plane)
# print (line_3)
# print (cross_point)


line_1: "Line" = list_of_all_lines[0]
line_2: "Line" = list_of_all_lines[1]
line_3: "Line" = list_of_all_lines[2]

# перевірити, чи вони не паралельні

# t1 = 0 # час до зіткнення з line_1
# t2 = 0 # час до зіткнення з line_2
T3 = None

# while not T3:
for t1 in range(1, 100000):
    # t1 += 1
    # t2 += 0
    # print(t1, t2)
    # while not T3:
    if t1 == 2000:
        print (1)
    for t2 in range(1, 10):
        # t2 += 1
        if t2 == t1:
            continue
        del_t = t2 - t1
        T1 = Point(line_1.point.x + t1 * line_1.direction[0]
                   ,line_1.point.y + t1 * line_1.direction[1]
                   ,line_1.point.z + t1 * line_1.direction[2])
        T2 = Point(line_2.point.x + t2 * line_2.direction[0]
                   , line_2.point.y + t2 * line_2.direction[1]
                   , line_2.point.z + t2 * line_2.direction[2])
        dx = (T2.x - T1.x) / del_t
        dy = (T2.y - T1.y) / del_t
        dz = (T2.z - T1.z) / del_t

        x_T0 = T1.x - dx * t1
        y_T0 = T1.y - dy * t1
        z_T0 = T1.z - dz * t1

        T0 = Point(x_T0,y_T0,z_T0)
        my_line = Line(T0,((T2.x - T1.x) / del_t,(T2.y - T1.y) / del_t,(T2.z - T1.z) / del_t))
        T3 = line_3.multiply(my_line)

        if T3:
            del_x = T3.x - T0.x
            del_y = T3.y - T0.y
            del_z = T3.z - T0.z
            if del_x != 0:
                dist = del_x
                dd = dx
            elif del_y != 0:
                dist = del_y
                dd = dy
            elif del_z != 0:
                dist = del_z
                dd = dz
            else:
                dist = None
                dd = None

            if dist:
                t3 = dist / dd
            else:
                t3 = 0
        else:
            t3 = 0
        if T3 and int(t3) == t3:
            print(my_line)
            break
    if T3 and int(t3) == t3:
        break

