import sympy as sp
from sympy import I, pi

def c1(m: int, n: int) -> sp.Matrix:
    return sp.Matrix([
        [1 + I**m, 1 - I**m, 0, 0],
        [0, 0, 1 + I**n, 1 - I**n]
    ])

def c2(m: int, n: int) -> sp.Matrix:
    zeta = sp.exp(2 * pi * I / 8)
    return sp.Matrix([
        [1, 1, zeta * I**m, zeta * I**m],
        [1, -1, zeta * I**n, zeta * I**n * -1],
    ])

def c3(m: int, n: int) -> sp.Matrix:
    return sp.Matrix([
        [1, 1, I**m, -I**m],
        [1, -1, I**n, I**n],
    ])

def c(i:int, m: int, n: int) -> sp.Matrix:
    match i:
        case 1:
            return c1(m, n)
        case 2:
            return c2(m, n)
        case _:
            return c3(m, n)
