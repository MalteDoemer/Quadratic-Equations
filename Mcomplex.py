import math

class Complex:
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def __str__(self):
        def i_str(n): return f"{n}i" if n != 1 and n != - \
            1 else "i" if n == 1 else "-i"

        if self.imag == 0:
            return f"{self.real}"
        elif self.real == 0:
            return f"{i_str(self.imag)}"
        elif self.imag < 0:
            return f"({self.real} - {i_str(abs(self.imag))})"
        elif self.imag > 0 and self.real < 0:
            return f"({i_str(self.imag)} - {abs(self.real)})"
        else:
            return f"({self.real} + {i_str(self.imag)})"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Complex(self.real + other, self.imag)
        elif isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (float, int)):
            return self + other
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return Complex(self.real - other, self.imag)
        elif isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (float, int)):
            return other + (-self)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)
        elif isinstance(other, Complex):
            a1 = self.real
            a2 = other.real
            b1 = self.imag
            b2 = other.imag
            return Complex(a1 * a2 - b1 * b2, a1 * b2 + b1 * a2)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return self * other
        else:
            return NotImplemented

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.real / other, self.imag / other)
        elif isinstance(other, Complex):
            num = self * other.conjugate()           # mit komplex Konjugiertem erweitern
            den = other.real ** 2 + other.imag ** 2  # Betrag im quadrat
            return num / den                         # 'den' ist eine reelle Zahl
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            num = other * self.conjugate()          # mit komplex Konjugiertem erweitern
            den = self.real ** 2 + self.imag ** 2   # Betrag im quadrat
            return num / den                        # 'den' ist eine reelle Zahl
        else:
            return NotImplemented

    def __abs__(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def conjugate(self):
        return Complex(self.real, -self.imag)
