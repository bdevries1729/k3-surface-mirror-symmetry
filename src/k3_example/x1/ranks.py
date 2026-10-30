from k3_example.lattices import invariant_sublattice
from k3_example.x1.intersections import compute_x1_intersection_matrix
from k3_example.x1.orbits import compute_x1_orbits
import k3_example.automorphisms.id as id
import k3_example.automorphisms.xy_permutation as xy
import k3_example.automorphisms.xzyw_permutation as xzyw
import k3_example.automorphisms.sigma_r as sigma_r
import k3_example.automorphisms.tau as tau

intersection_mat = compute_x1_intersection_matrix()
def compute_orbs(group_action_matrix):
    return compute_x1_orbits(group_action_matrix=group_action_matrix, print_to_terminal=False)

invariant_sublattice(name='full lattice', automorphism_matrix=id.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='(xy) invariant sublattice', automorphism_matrix=xy.permutation_matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='(xzyw) invariant sublattice', automorphism_matrix=xzyw.permutation_matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='sigma_r invariant sublattice', automorphism_matrix=sigma_r.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)
invariant_sublattice(name='tau invariant sublattice', automorphism_matrix=tau.matrix, compute_orbits=compute_orbs, intersection_matrix=intersection_mat)

print('-----------------------------------------')
print('All diagonal automorphisms')

for m in range(2):
    for n in range(8):
        sigma = (tau.matrix ** m) * (sigma_r.matrix ** n)
        print(sigma)
        invariant_sublattice(name=f'({m},{n}) invariant sublattice', automorphism_matrix=sigma, compute_orbits=compute_x1_orbits, intersection_matrix=intersection_mat)
        

