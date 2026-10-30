import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

def print_rank_and_discriminant_group(name, intersection_matrix, basis=None):
    if name:
        print()
        print(name)
    if basis is None:
        basis = sp.eye(intersection_matrix.rows)
    intersec_mat_in_new_basis = basis.T * intersection_matrix * basis
    print(f'rank: {intersec_mat_in_new_basis.rank()}')
    snf = smith_normal_form(intersec_mat_in_new_basis, domain=sp.ZZ)
    disc_group = [snf[i, i] for i in range(snf.rows) if snf[i, i] != 0 and snf[i, i] != 1]
    print(f'discriminant group: {disc_group}')

def orbit_basis(orbits, n) -> list[sp.Matrix]:
    return [sp.Matrix([1 if i in cycle else 0 for i in range(n)]) for cycle in orbits]

def invariant_sublattice(name, automorphism_matrix, compute_orbits, intersection_matrix=None, compute_intersection_matrix=None):
    if intersection_matrix is None:
        if compute_intersection_matrix is None:
            print("No intersection matrix computation function provided.")
            return
        intersection_matrix = compute_intersection_matrix()
    orbits = compute_orbits(automorphism_matrix)
    basis = sp.Matrix.hstack(*orbit_basis(orbits, intersection_matrix.rows))
    print_rank_and_discriminant_group(name=name, intersection_matrix=intersection_matrix, basis=basis)
