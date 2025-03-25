def is_even(number):
    """ Перевірка чи є парним число """
    return str(number)[-1] in ('2','4','6','8','0')

assert is_even(2494563894038**2) == True, 'Test1'
assert is_even(1056897**2) == False, 'Test2'
assert is_even(24945638940387**3) == False, 'Test3'
print("OK")
