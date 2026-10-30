import sympy as sp
from sympy import pi, I

zeta = sp.exp(2*pi*I/8)
matrix = sp.diag(1, 1, zeta ** 3, zeta ** -1) # type: ignore