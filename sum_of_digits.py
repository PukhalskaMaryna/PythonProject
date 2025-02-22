def sum_of_digits(number):
    return sum(int(i) for i in list(str(abs(number))))