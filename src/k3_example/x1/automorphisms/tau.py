import sympy as sp
from sympy import pi, I
import k3_example.x1.automorphisms.sigma_l as sigma_l
import k3_example.x1.automorphisms.sigma_r as sigma_r

zeta = sp.exp(2*pi*I/8)
matrix = sigma_l.matrix * sigma_r.matrix # type: ignore