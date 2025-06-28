def prime(divisible):
    return len(list(divisor for divisor in range(1, divisible + 1) if divisible % divisor == 0)) == 2

def prime_generator(end):
    count = 2
    while count < end + 1:
        if prime(count):
            yield count
        count += 1

from inspect import isgenerator

gen = prime_generator(1)
assert isgenerator(gen) == True, 'Test0'
assert list(prime_generator(10)) == [2, 3, 5, 7], 'Test1'
assert list(prime_generator(15)) == [2, 3, 5, 7, 11, 13], 'Test2'
assert list(prime_generator(29)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], 'Test3'
print('Ok')
