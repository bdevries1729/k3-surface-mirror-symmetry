from k3_example.x1.intersections import compute_x1_intersection_matrix
import k3_example.x1.automorphisms.xy_permutation as xy
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from k3_example.orbits import compute_orbits, orbit_basis
import k3_example.x1.automorphisms.xy_permutation as xy
import k3_example.x1.automorphisms.xzyw_permutation as xzyw
import k3_example.x1.automorphisms.sigma_r as sigma_r
import k3_example.x1.automorphisms.tau as tau

def print_rank_and_discriminant_group(name='', intersection_matrix=None, basis=None):
    if name:
        print()
    print(name)
    if intersection_matrix is None:
        intersection_matrix = compute_x1_intersection_matrix()
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
    orbits = compute_orbits(group_action_matrix=xy.permutation_matrix)
    basis = sp.Matrix.hstack(*orbit_basis(orbits))
    print_rank_and_discriminant_group(name='(xy) invariant sublattice', intersection_matrix=intersection_matrix, basis=basis)

def xzyw_invariant_sublattice(intersection_matrix=None):
    orbits = compute_orbits(group_action_matrix=xzyw.permutation_matrix)
    basis = sp.Matrix.hstack(*orbit_basis(orbits))
    print_rank_and_discriminant_group(name='(xzyw) invariant sublattice', intersection_matrix=intersection_matrix, basis=basis)

def sigma_r_invariant_sublattice(intersection_matrix=None):
    orbits = compute_orbits(group_action_matrix=sigma_r.matrix)
    basis = sp.Matrix.hstack(*orbit_basis(orbits))
    print_rank_and_discriminant_group(name='(sigma_r) invariant sublattice', intersection_matrix=intersection_matrix, basis=basis)

def tau_invariant_sublattice(intersection_matrix=None):
    orbits = compute_orbits(group_action_matrix=tau.matrix)
    basis = sp.Matrix.hstack(*orbit_basis(orbits))
    print_rank_and_discriminant_group(name='(tau) invariant sublattice', intersection_matrix=intersection_matrix, basis=basis)

intersection_mat = compute_x1_intersection_matrix()
full_picard(intersection_mat)
# xy_invariant_sublattice(intersection_mat)
# xzyw_invariant_sublattice(intersection_mat)
sigma_r_invariant_sublattice(intersection_mat)
# tau_invariant_sublattice(intersection_mat)

# for m in range(2):
#     for n in range(8):
#         sigma = (tau.matrix ** m) * (sigma_r.matrix ** n)
#         print(sigma)
#         orbits = compute_orbits(group_action_matrix=sigma, print_to_terminal=True)
#         basis = sp.Matrix.hstack(*orbit_basis(orbits))
#         print_rank_and_discriminant_group(name=f'({m}, {n}) invariant sublattice', intersection_matrix=intersection_mat, basis=basis)
#         print('-----------------------------------------')

