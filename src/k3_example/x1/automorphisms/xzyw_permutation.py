import sympy as sp

# we want (xzyw) * [x, y, z, w] = [z, w, y, x], so we permute the columns of the identity matrix by (1324) cycle
permutation_matrix = sp.Matrix([
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
])
