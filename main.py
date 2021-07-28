import math
import re
from decimal import *

pi = Decimal("3.14159265358979323846264338327950288419716939937510")

pi_div_2 = Decimal("1.5707963267948966")


def factorial(number):
    assert number % Decimal("1") == Decimal("0"), "Incorrect value"
    one = Decimal("1")
    fact = number
    while number > one:
        number -= one
        fact *= number

    return fact


def gen_den():
    d = 1
    f = 1
    while (1):
        yield f
        d = d + 1
        f = f * d
    return


def gen_num(x):
    n = x
    while (1):
        yield n
        n *= x
    return


def gen_sign():
    while (1):
        yield 1
        yield -1
        yield -1
        yield 1
    return


def sincos(x):
    x = divmod(x, 2 * pi)[1]
    den = gen_den()
    num = gen_num(x)
    sign = gen_sign()

    s = 0
    c = 1
    i = 1
    done_s = False;
    done_c = False

    while (not done_s and not done_c):
        new_s = s + next(sign) * next(num) / next(den)
        new_c = c + next(sign) * next(num) / next(den)
        if (new_c - c == 0): done_c = True
        if (new_s - s == 0): done_s = True
        c = new_c
        s = new_s
        i = i + 2
    return (s, c)


def dec_sin(x):
    (s, c) = sincos(x)
    return s


def dec_cos(x):
    (s, c) = sincos(x)
    return c


def dec_tan(x):
    (s, c) = sincos(x)
    return s / c


def dec_cot(x):
    (s, c) = sincos(x)
    return c / s


def dec_asin(x):
    one = Decimal("1")
    assert x <= one and x >= -one, "Out of range"

    return Decimal(str(math.asin(float(str(x)))))


def dec_acos(x):
    one = Decimal("1")
    assert x <= one and x >= -one, "Out of range"

    return Decimal(str(math.acos(float(str(x)))))


def dec_acos(x):
    one = Decimal("1")
    assert x <= one and x >= -one, "Out of range"

    return Decimal(str(math.acos(float(str(x)))))


def dec_atan(x):
    return dec_asin(x / (Decimal("1") + x ** Decimal("2")).sqrt())


def dec_acot(x):
    return pi_div_2 - dec_atan(x)


OPERATORS = {
    '+': (1, lambda x, y: x + y),
    '-': (1, lambda x, y: x - y),
    '*': (2, lambda x, y: x * y),
    '/': (2, lambda x, y: x / y),
    '^': (3, lambda x, y: x ** y),
}

FUNCTIONS = {
    '(': lambda x: x,
    'sin(': lambda x: dec_sin(x),
    'cos(': lambda x: dec_cos(x),
    'tan(': lambda x: dec_tan(x),
    'cot(': lambda x: dec_cot(x),
    'asin(': lambda x: dec_sin(x),
    'acos(': lambda x: dec_cos(x),
    'atan(': lambda x: dec_atan(x),
    'acot(': lambda x: dec_acot(x),
    'sqrt(': lambda x: x.sqrt(),
    'exp(': lambda x: x.exp(),
    'abs(': lambda x: abs(x),
}

POSTFIX_FUNCTIONS = {
    '!': lambda x: factorial(x)
}


def calculator(formula):
    def is_number(string):
        return re.match(r'\d+\.\d+|\d+', string)

    def parse(formula_string):
        regexp = r'sin\(|cos\(|tan\(|sqrt\(|cot\(|exp\(|asin\(|acos\(|abs\(|\(|\)|\+|-|/|\^|\*|\!|\d+\.\d+|\d+'

        for el in re.finditer(regexp, formula_string):
            yield Decimal(str(el[0])) if is_number(el[0]) else el[0]

    def skob(parsed_formula, ):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] in OPERATORS and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()

                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    yield x
                    if x in FUNCTIONS:
                        break
            elif token in FUNCTIONS:
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polskiy):
        stack = []
        for token in polskiy:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][1](x, y))
            elif token in POSTFIX_FUNCTIONS:
                x = stack.pop()
                stack.append(POSTFIX_FUNCTIONS[token](x))
            elif token in FUNCTIONS:
                x = stack.pop()
                stack.append(FUNCTIONS[token](x))
            else:
                stack.append(token)
        return Decimal(str(stack[0]))

    return calc(skob(parse(formula)))


if __name__ == '__main__':
    print(calculator('(2!+2!)! + (tan(0.3) + sin(0.3)) * 2^2/3'))
