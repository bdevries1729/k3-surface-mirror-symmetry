import sympy as sp

# not ideal, but we convert to floating point numbers for efficient comparison with other matrices
def matrix_key(mat: sp.Matrix, round_digits=5, precision=12):
    keyed = []
    for e in mat:
        v = sp.N(e, precision)
        re = round(float(sp.re(v)), round_digits)
        im = round(float(sp.im(v)), round_digits)
        keyed.append((re, im))
    return tuple(keyed)


def find_idxs(search_list, find_list):
    lookup = {matrix_key(mat[0]): i for i, mat in enumerate(search_list)}
    return [lookup[matrix_key(mat[0])] for mat in find_list]