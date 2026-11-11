import sympy as sp
from k3_example.line_helper import equivalence_class_index_from_line_index
from k3_example.x4.lines import compute_lines, compute_line_labels
from k3_example.x1.orbits import compute_x1_permutation
from sympy.combinatorics import Permutation
from pprint import pprint

def a1_permut(permut, a1_identifiers, offset):
    pts = {tuple(sorted(lst[0])): i for i, lst in enumerate(a1_identifiers)} | {tuple(sorted(lst[1])): i for i, lst in enumerate(a1_identifiers)}
    return [pts[tuple(sorted([i^permut for i in lns[0]]))]+offset for lns in a1_identifiers]

def a3_permut(permut, lines, a3_identifiers):
    pts = {(tuple(sorted(a3[0])), a3[1]): i for i, a3 in enumerate(a3_identifiers)}
    idx_offset = len(lines) - len(a3_identifiers)
    return [pts[(tuple(sorted([i^permut for i in a3[0]])), None if a3[1] is None else a3[1]^permut)]+idx_offset for a3 in a3_identifiers]

def compute_x4_orbits(group_action_matrix: sp.Matrix, print_to_terminal=False, lines=None, a1_identifiers=None, a3_identifiers=None, labels=None) -> list[list[int]]:
    if lines is None or a1_identifiers is None or a3_identifiers is None:
        lines, a1_identifiers, a3_identifiers = compute_lines()
    if print_to_terminal and labels is None:
        labels = compute_line_labels(lines, a1_identifiers, a3_identifiers)
    
    p = compute_x1_permutation(group_action_matrix)
    num_exceptional = len(a1_identifiers) + len(a3_identifiers)
    # for the equivalence class curves we simply compute where one representive goes
    image_under_action = [equivalence_class_index_from_line_index(line[0]^p, lines) for line in lines[:-num_exceptional]]
    # then we compute the images of the exceptional curves: a1 then a3
    image_under_action.extend(a1_permut(p, a1_identifiers, len(lines) - num_exceptional))
    image_under_action.extend(a3_permut(p, lines, a3_identifiers))
    permut = Permutation(image_under_action)
    
    if print_to_terminal:
        pprint([[labels[i] for i in cycle] for cycle in permut.cyclic_form])
    
    return permut.full_cyclic_form
