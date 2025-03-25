# import math

class Fraction:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.a * other.a, self.b * other.b)
        return None

    def __add__(self, other):
        if isinstance(other, Fraction):
            a = self.a * other.b + self.b * other.a
            b = self.b * other.b
            # nsd = math.gcd(a, b)
            # a /= nsd
            # b /= nsd
            return Fraction(a, b)
        return None

    def __sub__(self, other):
        if isinstance(other, Fraction):
            other.a = -1 * other.a
            return self + other
        return None

    def __eq__(self, other):
        if isinstance(other, Fraction):
            self.a *= other.b
            other.a *= self.b
            return self.a == other.a
        return None

    def __gt__(self, other):
        if isinstance(other, Fraction):
            self.a *= other.b
            other.a *= self.b
            return self.a > other.a
        return None

    def __lt__(self, other):
        if isinstance(other, Fraction):
            return True if self != other and not self.a > other.a else False
        return None

    def __str__(self):
        return f"Fraction: {self.a}, {self.b}"

f_a = Fraction(2, 3)
f_b = Fraction(3, 6)
f_c = f_b + f_a
assert str(f_c) == 'Fraction: 21, 18'
f_d = f_b * f_a
assert str(f_d) == 'Fraction: 6, 18'
f_e = f_a - f_b
assert str(f_e) == 'Fraction: 3, 18'

assert f_d < f_c  # True
assert f_d > f_e  # True
assert f_a != f_b  # True
f_1 = Fraction(2, 4)
f_2 = Fraction(3, 6)
assert f_1 == f_2  # True
print('OK')
