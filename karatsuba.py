import math


def wrapper(x, y):
    ans = karatsuba(str(x), str(y))
    return int(ans)


def karatsuba(x, y):
    print(len(x), len(y), x, y)
    if len(x) <= 1 or len(y) <= 1:
        return int(x) * int(y)

    n = max(len(x), len(y))
    h = math.ceil(n / 2)

    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    print(a, b, c, d, "\n")
    input()

    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_plus_bc = (karatsuba(a + b, c + d)) - ac - bd

    return ac * (10 ** (2 * h)) + (ad_plus_bc * (10**h)) + bd


ans = wrapper(146123, 352120)

print(ans)
