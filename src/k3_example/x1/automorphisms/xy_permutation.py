from k3_example.x1.lines import ci_labels, ci_matrices
import sympy as sp
from sympy.combinatorics import Permutation
from k3_example.named_lines import get_label, compute_c1_names
from pprint import pprint

xy_permutation_matrix = sp.Matrix([
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

def compute_orbits(print_to_terminal:bool=False, c1_names=None) -> list[sp.Matrix]:
    '''
    Generates the orbits of lines under (xy) permutation. Orbits are returned as a list of list of 
    vectors, with each vector an orbit and each coordinate of the vector representing a line (1 for belonging
    to the orbit, and 0 if not). The argument `print_to_terminal` may be enabled, and names for c1_curves to eliminate
    the need to re-compute.
    '''
    if c1_names is None:
        c1_names = compute_c1_names()
    ci_matrices_rref = [ci_mat.rref() for ci_mat in ci_matrices]
    image_under_xy_rref =  [(ci_mat * xy_permutation_matrix).rref() for ci_mat in ci_matrices]
    permut = Permutation([ci_matrices_rref.index(xy_image) for xy_image in image_under_xy_rref])
    if print_to_terminal:
        pprint([[get_label(*ci_labels[i], names=c1_names) for i in cycle] for cycle in permut.cyclic_form])
    return [sp.Matrix([1 if i in cycle else 0 for i in range(len(ci_matrices))]) for cycle in permut.full_cyclic_form]
