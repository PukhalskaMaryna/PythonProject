# my_tuple = ([19, 13, -2, 1],[18, 19, -1, -1],[20, 25, -2, -2],[12, 31, -1, -2],[20, 19, 1, -5])

with open("F:/OPERU.KHO.VMAP/СОТРУДНИКИ/PUKHALSK/РІЗНЕ/AtoC/part24_1.txt", 'r') as file:
    my_tuple = tuple(
        [int(line[0]), int(line[1]), int(line[3]), int(line[4])]
        for line in (line.replace('@', ',').replace(' ', '').split(',') for line in file)
    )

a,b,counter = 200000000000000,400000000000000,0

# функція для перевірки належності одного числа до проміжку
def is_in_range(x, a, b):
    return a <= x <= b

def is_moving_towards(vector, coord, coord1):
    return (vector >= 0 and coord >= coord1) or (vector <= 0 and coord <= coord1)

for i, lst_1 in enumerate(my_tuple):
    for lst_2 in my_tuple[i + 1:]:
        x1, y1, Vx1, Vy1 = lst_1
        x2, y2, Vx2, Vy2 = lst_2

        up = (x2 - x1) * Vy2 - (y2 - y1) * Vx2
        down = Vx1 * Vy2 - Vy1 * Vx2

        if down != 0:
            t = up / down
            x = x1 + t * Vx1
            y = y1 + t * Vy1

            if is_in_range(x, a, b) and \
                    is_in_range(y, a, b) and \
                    is_moving_towards(Vx1, x, x1) and \
                    is_moving_towards(Vy1, y, y1) and \
                    is_moving_towards(Vx2, x, x2) and \
                    is_moving_towards(Vy2, y, y2):
                counter += 1

print(counter)
