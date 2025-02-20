def common_elements():
    result_3 = {x for x in range(100) if x % 3 == 0}
    result_5 = {x for x in range(100) if x % 5 == 0}
    return result_3.intersection(result_5)

assert common_elements() == {0, 75, 45, 15, 90, 60, 30}
print('ОК')