import math
from Parser import Parser
from Mcomplex import Complex


def get_user_input():
    print("Enter a quadratic equation in form of:\n\tax^2 + bx + c = 0\n")
    a = parse_complex(input("a: "))
    b = parse_complex(input("b: "))
    c = parse_complex(input("c: "))

    if a == 0:
        print("\nThat's not a quadratic equation !!!")
        exit(-1)

    print(f"\n\t{equ_pretty(a,b,c)} = 0")
    return a, b, c


def equ_pretty(a, b, c):

    if isinstance(a, (int, float)):
        if a == 1:
            axsq = 'x^2'
        elif a == -1:
            axsq = '-x^2'
        else:
            axsq = f'{a}x^2'
    elif isinstance(a, Complex):
        axsq = f'{a}x^2'
    else:
        axsq = 'NaN'

    if isinstance(b, (int, float)):
        if b == 0:
            bx = ''
        elif b == -1:
            bx = '- x'
        elif b == 1:
            bx = '+ x'
        elif b < 1:
            bx = f'{b}x'
        else:
            bx = f'+ {b}x'
    elif isinstance(b, Complex):
        if b.real == 0 and b.imag < 0:
            bx = f'{b}x'
        else:
            bx = f'+ {b}x'
    else:
        bx = '+ NaN'

    if isinstance(c, (int, float)):
        if c == 0:
            c = ''
        elif c < 1:
            c = f'- {abs(c)}'
        else:
            c = f'+ {c}'
    elif isinstance(c, Complex):
        c = f'+ {c}'
    else:
        c = '+ NaN'

    return f"{axsq} {bx} {c}"


def parse_complex(inp: str):
    err = []
    tree = Parser(inp, err).parse()
    if len(err) == 0:
        res = tree.eval()

        if isinstance(res, Complex) and res.imag == 0:
            res = res.real

        return res
    else:
        for error in err:
            print(error)
        exit(-1)


def quad_equ_real(a, b, c):
    d = b**2 - 4 * a * c

    if d >= 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
    else:
        raise ValueError("math domain error")

    return x1, x2


def sqrtex(num):
    if isinstance(num, (int, float)) and num >= 0:
        root = math.sqrt(num)
        return root, -root
    elif isinstance(num, (int, float)) and num < 0:
        root = math.sqrt(abs(num))
        return Complex(0, root), Complex(0, -root)
    elif isinstance(num, Complex):
        if num.real == 0:
            return sqrtex(num.imag)
        elif num.imag == 0:
            return sqrtex(num.real)
        else:
            x1, x2 = quad_equ_real(4, -4 * num.real, -(num.imag**2))

            if x2 < 0 and x1 > 0:
                u1 = math.sqrt(x1)
                u2 = - math.sqrt(x1)
            elif x2 > 0 and x1 < 0:
                u1 = math.sqrt(x2)
                u2 = - math.sqrt(x2)
            else:
                raise Exception(f"My guess is wrong: x1 = {x1}; x2 = {x2}")

            v1 = num.imag / (2 * u1)
            v2 = num.imag / (2 * u2)

            return Complex(u1, v1), Complex(u2, v2)
    else:
        return NotImplemented


def main():

    a, b, c = get_user_input()

    p = - (b / (2 * a))
    q = c / a

    wsq = p * p - q

    w1, w2 = sqrtex(wsq)

    z1 = p + w1
    z2 = p + w2

    print(f"\nz1 = {z1}\nz2 = {z2}")


if __name__ == "__main__":
    main()
