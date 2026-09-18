import sympy as sp
from k3_example.x1.intersections import compute_intersection_matrix

def normalize_by_lcm(vec):
    denoms = []
    for val in vec:
        val = sp.sympify(val) # not sure if this is necessary
        if val.is_irrational:
            return None
        if val.is_Integer:
            continue
        if val.is_rational:
            denoms.append(val.q)
    return sp.lcm(denoms) * vec

def unit_first_indexes(vec):
    idxs = []
    if 1 in vec:
        idxs.append(vec.index(1))
    if -1 in vec:
        idxs.append(vec.index(-1))
    return idxs

def find_basis(intersection_matrix=None, basis=None):
    if intersection_matrix is None:
        intersection_matrix = compute_intersection_matrix()
    if basis is None:
        basis = sp.eye(intersection_matrix.rows)
    if 0 not in intersection_matrix.eigenvals():
        return basis
    intersection_mat_for_basis = basis.T * intersection_matrix * basis
    null_space = next((val[2] for val in intersection_mat_for_basis.eigenvects() if val[0] == 0), [])

    integer_eigenvecs = [list(normalize_by_lcm(vec)) for vec in null_space if vec is not None] # type: ignore
    if len(integer_eigenvecs) == 0:
        return basis
    
    for vec in integer_eigenvecs:
        unit_idxs = unit_first_indexes(vec)
        if len(unit_idxs) > 0:
            i = min(unit_idxs)
            idxs = [j for j in range(basis.cols) if j != i]
            return find_basis(intersection_matrix=intersection_matrix, basis=basis[:, idxs])
