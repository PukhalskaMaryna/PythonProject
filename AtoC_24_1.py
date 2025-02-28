my_tuple = (
    [19, 13, -2, 1],
    [18, 19, -1, -1],
    [20, 25, -2, -2],
    [12, 31, -1, -2],
    [20, 19, 1, -5]
)

a = 7
b = 27
counter = 0

def is_in_range(x, y, a, b):
    return a <= x <= b and a <= y <= b

# def is_moving_towards(x, y, x1, y1, Vx, Vy):
#     return (Vx > 0 and x >= x1) or (Vx < 0 and x <= x1) and (Vy > 0 and y >= y1) or (Vy < 0 and y <= y1)

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

            if is_in_range(x, y, a, b) and \
                    is_moving_towards(Vx1, x, x1) and \
                    is_moving_towards(Vy1, y, y1) and \
                    is_moving_towards(Vx2, x, x2) and \
                    is_moving_towards(Vy2, y, y2):
                counter += 1

print(counter)
