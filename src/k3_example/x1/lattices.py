from k3_example.x1.intersections import compute_intersection_matrix
import k3_example.x1.automorphisms.xy_permutation as xy
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

def print_rank_and_discriminant_group(name='', intersection_matrix=None, basis=None):
    if name:
        print()
    print(name)
    if intersection_matrix is None:
        intersection_matrix = compute_intersection_matrix()
    if basis is None:
        basis = sp.eye(intersection_mat.rows)
    intersec_mat_in_new_basis = basis.T * intersection_matrix * basis
    print(f'rank: {intersec_mat_in_new_basis.rank()}')
    snf = smith_normal_form(intersec_mat_in_new_basis, domain=sp.ZZ)
    disc_group = [snf[i, i] for i in range(snf.rows) if snf[i, i] != 0 and snf[i, i] != 1]
    print(f'discriminant group: {disc_group}')

def full_picard(intersection_matrix=None):
    print_rank_and_discriminant_group(name='Full Picard', intersection_matrix=intersection_matrix)

def xy_invariant_sublattice(intersection_matrix=None):
    basis = sp.Matrix.hstack(*xy.compute_orbits())
    print_rank_and_discriminant_group(name='(xy) invariant sublattice', intersection_matrix=intersection_matrix, basis=basis)

intersection_mat = compute_intersection_matrix()
full_picard(intersection_mat)
xy_invariant_sublattice(intersection_mat)