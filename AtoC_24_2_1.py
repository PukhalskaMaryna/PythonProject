import itertools # permutations - функція обробки списку і генерування варіантів перестановки

# all_my_lst = [[19, 13, 30, -2,  1, -2],
#             [18, 19, 22, -1, -1, -2],
#             [20, 25, 34, -2, -2, -4],
#             [12, 31, 28, -1, -2, -1],
#             [20, 19, 15,  1, -5, -3]
#             ]

# забираємо дані з файлу і формуємо кортеж із списків
with open("F:/OPERU.KHO.VMAP/СОТРУДНИКИ/PUKHALSK/РІЗНЕ/AtoC/part24_1.txt", 'r', encoding='utf-8') as file:
    all_my_lst = [
        [int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5].replace('\n', ''))]
        for line in (
            line.replace('@', ',').replace(' ', '').split(',')  # Заміна @ на кому і видалення пробілів
            for line in file)]



def find_time(x1, x2, v_x1, v_x2):
    """
        функція знаходить час зіткнення по одній координаті,
        при цьому враховує, якщо швидкості рівні,
        то перевіряє і рівність координат.
    """
    if v_x1 == v_x2:
        return 0 if x1 == x2 else None  #  швидкості рівні, перевіряємо координати
    t = (x1 - x2) / (v_x2 - v_x1)  # час зіткнення.
    # чи час є цілим і невід'ємним
    return int(t) if t >= 0 and t.is_integer() else None


def generate_hailstone_variants(lst: list, t1, t2):
    """
    функція перебирає всі варіанти перестановок градинок, щоб отримати ту, яка буде вірною по черговості зіткнення
    статично передається час до першого і час до другого зіткнень
    :param lst: список для отримання всіх перестановок
    :param t1: час від 0 до першого зіткнення
    :param t2: час від 0 до другого зіткнення
    t2 > t1 завжди
    :return: початкову точку, якщо така знайшлась
    """
    # оскільки кожну наносекунду може бути зіткнення
    # то перебираємо всі варіанти перестановок градинок так,
    # щоб зафіксувати таку послідовність, яка визначить черговість зіткнення

    x = y = z = None  # координати стартової точки спочатку фіксуємо як None,
    # бо теоретично може не бути правильного варіанту

    delta_t = t2 - t1 # наносекунди між першим і другим зіткненнями

    for hailstones in list(itertools.permutations(lst)):
        # print('__' * 20)
        # print(hailstones)
        # print('__' * 20)
        # оскільки будуть перебрані всі варіанти перестановок,
        # то на якійсь перестановці отримаємо вірний варіант
        # спочатку беремо для кожної перестановки 2 перші градинки, як 1-ше і 2-ге зіткнення
        first_hailstone = hailstones[0]
        second_hailstone = hailstones[1]
        # тепер ми точно знаємо, де камінь буде через t1 наносекунд і через t2,
        # координати першого зіткнення
        x1, y1, z1 = (first_hailstone[0] + first_hailstone[3] * t1,
                      first_hailstone[1] + first_hailstone[4] * t1,
                      first_hailstone[2] + first_hailstone[5] * t1)

        # координати другого зіткнення
        x2, y2, z2 = (second_hailstone[0] + second_hailstone[3] * t2,
                      second_hailstone[1] + second_hailstone[4] * t2,
                      second_hailstone[2] + second_hailstone[5] * t2)

        # швидкість каменю
        v_x, v_y, v_z = ((x2 - x1) / delta_t,
                         (y2 - y1) / delta_t,
                         (z2 - z1) / delta_t)

        # зупиняємось, якщо швидкість не є цілим числом із test = False
        # значить вся перестановка із заданими t1 і t2 не підходить, переходимо до наступної
        if not (v_x.is_integer() and v_y.is_integer() and v_z.is_integer()):
            continue

        # стартова точка каменю
        x, y, z = x1 - v_x, y1 - v_y, z1 - v_z
        # цикл для визначення часу зіткнення з кожною наступною градинкою
        t = 0
        for i,hailstone in enumerate(hailstones[2:]):
            next_x, next_y, next_z, next_v_x, next_v_y, next_v_z = hailstones[2:][i]
            t_x = find_time(x, next_x, v_x, next_v_x)
            t_y = find_time(y, next_y, v_y, next_v_y)
            t_z = find_time(z, next_z, v_z, next_v_z)


            # список можливих варіантів t по кожній координаті
            lst_t = [t_x, t_y, t_z]
            # є хоч одне значення None, або всі 0 - значить нема єдиної точки перетину
            if lst_t.count(None) > 0 or lst_t.count(0) == 3:
                break
            # всі три значення рівні та вже не можуть бути нульові (і вже не можуть бути None)
            # set(lst_t) - set "схлопує" однакові значення, щоб були тільки унікальні
            elif len(set(lst_t)) == 1:
                t = lst_t[0]
            # хоч одне не 0,
            # перевіряємо рівність не нульових, якщо їх 2,
            # або забираємо третє, якщо 2 з 3-х нулі
            elif len(set(lst_t)) == 2 and lst_t.count(0) in (1, 2):
                t = next(t for t in lst_t if t != 0)  # забираємо перше не нульове
            else:  # зупиняємо перевірку, якщо хоч 1 градинка не має перетину з каменем
                break
            # перевірка, щоб кожен наступний час був більше попереднього, якщо ні - обриваємо перевірку
            if t <= t2:
                break
            # якщо знайшовся варіант, який перейшов всі перевірки
            else:
                return [x, y, z]

def final_func(insert_my_lst:list,max_i,max_ii):
    """
    ф-ія проганяє перевірку списку градинок на перетин з каменем,
    перебираючм в циклі варіанти наносекунд до першого і другого зіткнень
    :param insert_my_lst: частина списку із трьох градинок
    :param max_i: максимальне значення наносекунд для першого зіткнення
    :param max_ii: максимальне значення наносекунд для другого зіткнення
    :return: суму початкових координат і самі координати
    """
    for i in range(1,max_i + 1):
        # print(f'i = {i}')
        for ii in range(i+1, max_ii + 1):
            # print(f'   ii = {ii}')
            if generate_hailstone_variants(insert_my_lst, i, ii) is not None:
               return generate_hailstone_variants(insert_my_lst, i, ii)
    return []

iii = 0
for my_lst in itertools.combinations(all_my_lst, 3):
    iii += 1
    result = final_func(list(my_lst),5,6)
    if iii % 1000000 == 0:
        print(iii // 1000000)
    if result:
        print(result)
        break
else:
    print('без результату')

# для старту припускаємо, що перше і друге зіткнення станеться мнш ніж через 100 секунд
# якщо не спрацює - треба збільшувати максимум
# print(final_func(my_lst,10,10))
