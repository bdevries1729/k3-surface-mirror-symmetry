from k3_example.lattices import invariant_sublattice
from k3_example.x4.intersections import compute_x4_intersection_matrix
from k3_example.x4.orbits import compute_x4_orbits
from k3_example.x4.lines import compute_lines
import k3_example.automorphisms.id as id
import k3_example.automorphisms.xy_permutation as xy
import k3_example.automorphisms.xzyw_permutation as xzyw
import k3_example.automorphisms.sigma_r as sigma_r
import k3_example.automorphisms.tau as tau

lines, a1_identifiers, a3_identifiers = compute_lines()
intersection_mat = compute_x4_intersection_matrix(lines=lines, a1_identifiers=a1_identifiers, a3_identifiers=a3_identifiers)
def compute_orbs(group_action_matrix):
    return compute_x4_orbits(group_action_matrix=group_action_matrix, print_to_terminal=False, lines=lines, a1_identifiers=a1_identifiers, a3_identifiers=a3_identifiers)

invariant_sublattice(name='full lattice', automorphism_matrix=id.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='(xy) invariant sublattice', automorphism_matrix=xy.permutation_matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='(xzyw) invariant sublattice', automorphism_matrix=xzyw.permutation_matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='sigma_r invariant sublattice', automorphism_matrix=sigma_r.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='tau invariant sublattice', automorphism_matrix=tau.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)

print('-----------------------------------------')
print('All diagonal automorphisms')

for n in range(4):
    sigma = sigma_r.matrix ** n
    print(sigma)
    invariant_sublattice(name=f'({n}) invariant sublattice', automorphism_matrix=sigma, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
        

