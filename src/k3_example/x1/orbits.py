from k3_example.x1.lines import ci_labels, ci_matrices
import sympy as sp
from sympy.combinatorics import Permutation
from k3_example.named_lines import get_label, compute_c1_names
from pprint import pprint
from k3_example.compare import find_idxs

def compute_x1_permutation(group_action_matrix: sp.Matrix) -> Permutation:
    ci_matrices_rref = [ci_mat.rref() for ci_mat in ci_matrices]
    # notice that if x -> sigma(x), then sigma({f(x) = 0}) = {f(sigma^(-1)(x)) = 0}
    image_under_action_rref =  [(ci_mat * group_action_matrix**-1).rref() for ci_mat in ci_matrices]
    return Permutation(find_idxs(ci_matrices_rref, image_under_action_rref))

def compute_x1_orbits(group_action_matrix: sp.Matrix, print_to_terminal=False, c1_names=None) -> list[list[int]]:
    '''
    Generates the orbits of lines under `group_action_matrix`. The argument `print_to_terminal` may be enabled, and names for `c1_curves` 
    is optionally provided to eliminate the need to re-compute.
    '''
    if c1_names is None:
        c1_names = compute_c1_names()
    permut = compute_x1_permutation(group_action_matrix)
    if print_to_terminal:
        pprint([[get_label(*ci_labels[i], names=c1_names) for i in cycle] for cycle in permut.cyclic_form])
    return permut.full_cyclic_form
