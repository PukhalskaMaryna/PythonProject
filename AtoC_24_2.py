my_tuple = ([19, 13, 30, -2,  1, -2],[17, 14, 28],
            [18, 19, 22, -1, -1, -2],
            [20, 25, 34, -2, -2, -4],
            [12, 31, 28, -1, -2, -1],
            [20, 19, 15,  1, -5, -3]
            )

# забираємо дані з файлу і формуємо кортеж із списків,
# кожен список містить 2 координати і 2 швидкості
# with open("F:/OPERU.KHO.VMAP/СОТРУДНИКИ/PUKHALSK/РІЗНЕ/AtoC/part24_1.txt", 'r') as file:
#     my_tuple = tuple(
#         [int(line[0]), int(line[1]), int(line[3]), int(line[4])]
#         for line in (line.replace('@', ',').replace(' ', '').split(',') for line in file)
#     )

# область допустимих значень (ОДЗ) - межі (a, b)
# count_hailstone - к-ть градинок, а відповідно і к-ть зіткнень
a, b, count_hailstone = 7, 27, len(my_tuple)

#___________________________________________________________
# визначаємо необхідні функції
def is_in_range(x, min_x, max_x):
    """
        функція для перевірки належності одного числа до проміжку
    """
    return min_x <= x <= max_x

# !важливо: до зіткнення градинка і камінь рухались одну і ту саму к-ть наносекунд
# отже, якщо час зіткнення = t, тоді кожна координата пройде рівно t наносекунд
# якщо x1 - це абсциса градинки, а x2 - каменю
# то час зіткнення знаходиться як x1 + t * Vx1 = x2 + t * Vx2
# очевидно, якщо Vx1 = Vx2, то тоді та x1 повинно = x2, інакше зіткнення не буде
# t = (x1 - x2) / (Vx2 - Vx1) = (y1 - y2) / (Vy2 - Vy1) = (z1 - z2) / (Vz2 - Vz1) - умова перетину
# + врахувати можливість рівності кожної швидкості

def find_time(x1, x2, v_x1, v_x2):
    """
        функція знаходить час зіткнення координаті,
        при цьому враховує, якщо швидкості рівні,
        то перевіряє і рівність координат.
    """
    if v_x1 == v_x2:
        return 0 if x1 == x2 else None  #  швидкості рівні, перевіряємо координати
    t = (x1 - x2) / (v_x2 - v_x1)  # час зіткнення.
    # чи час є цілим і невід'ємним
    return int(t) if t >= 0 and t.is_integer() else None


def does_it_break_hailstone(insert_start_position:list,insert_my_tuple:tuple):
    """
        функція для перевірки,
        чи для вказаної стартової позиції start_position
        відбудеться зіткнення з усіма градинками
    """
    t  = None
    for lst in insert_my_tuple:
        x1, y1, z1, v_x1, v_y1, v_z1 = lst  # параметри градинки
        x2, y2, z2, v_x2, v_y2, v_z2 = insert_start_position # параметри каменю

        # список можливих варіантів t по кожній координаті
        lst_t = [find_time(x1, x2, v_x1, v_x2)
                , find_time(y1, y2, v_y1, v_y2)
                , find_time(z1, z2, v_z1, v_z2)]
        # є хоч одне значення None, або всі 0 - значить нема єдиної точки перетину
        if lst_t.count(None) > 0 or lst_t.count(0) == 3:
            t = None
        # всі три значення рівні та вже не можуть бути нульові (і вже не можуть бути None)
        # set(lst_t) - set "схлопує" однакові значення, щоб були тільки унікальні
        elif len(set(lst_t)) == 1:
            t = lst_t[0]
        # хоч одне не 0,
        # перевіряємо рівність не нульових, якщо їх 2,
        # або забираємо третє, якщо 2 з 3-х нулі
        elif len(set(lst_t)) == 2 and lst_t.count(0) in (1,2):
            t = next(t for t in lst_t if t != 0) # забираємо перше не нульове
        if t is None: # зупиняємо перевірку, якщо хоч 1 градинка не має перетину з каменем
            break
    # повертаємо start_position, якщо всі градинки розбиті каменем в межах ОДЗ або порожній список, якщо перевірка зазнала невдачі
    return insert_start_position if t is not None else []


# ________________________________________________________________________________
# якщо наша ОДЗ в проміжку (a, b), а к-ть зіткнень count_hailstone, то швидкість варіюється залежно від напрямку
# при початковій позиції x0 треба вирахувати відстань до краю = a - x0,
# розділити на к-ть зіткнень count_hailstone (забрати ціле від ділення),
# це буде мінімальна від'ємна швидкість minVx = (a - x0) / (count_hailstone + 1), де +1, бо до 1-о зіткнення мінімум 1 наносекунда
# 7-27 = -20, minVx = -20/5 = -4 - мінімальна від'ємна швидкість для позиції x0 = 27
# якщо при діленні виникає дробова частина - беремо тільки цілу (a - x0) // (count_hailstone + 1)
# аналогічно можна вирахувати максимальну додатну швидкість
# maxVx = (b - x0) // (count_hailstone + 1)
# наприклад x0 = 20, тоді 27-20 = 7, maxVx = 7//5 = 1
# отже, для кожної початкової позиції ми можемо вирахувати мінімально і максимально допустиму швидкість по кожній координаті
# minVx <= Vx <= maxVx

# фінальна функція
def find_start_position():
    """
    бігає по всім координатам і перебирає можливу швидкість для кожної координати
    :return: стартову позицію каменю або порожній список, якщо нема такої
    """
    for x0 in range(a, b+1): # перебираємо можливі координати по x, +1, щоб включити ліву межу b
        for v_x0 in range(a, b+1): # перебираємо можливу швидкість по x
            for y0 in range(a, b+1): # перебираємо можливі координати по y
                for v_y0 in range(a, b+1): # перебираємо можливу швидкість по y
                    for z0 in range(a, b+1): # перебираємо можливі координати по z
                        for v_z0 in range(a, b+1): # перебираємо можливу швидкість по z
                            # ф-ія does_it_break_hailstone() повертає стартову позицію, якщо ця позиція пройшла перевірку на перетин градинок
                            # або порожнечу, якщо ні
                            # print([x0, y0, z0, v_x0, v_y0, v_z0])
                            # print('_' * 20)
                            final_start_position = does_it_break_hailstone([x0, y0, z0, v_x0, v_y0, v_z0], my_tuple)
                            if final_start_position:
                                return final_start_position
    return []

print(find_start_position())