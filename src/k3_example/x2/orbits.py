import sympy as sp
from k3_example.line_helper import equivalence_class_index_from_line_index
from k3_example.x2.lines import compute_lines, compute_line_labels
from k3_example.x1.orbits import compute_x1_permutation
from sympy.combinatorics import Permutation
from pprint import pprint

def exceptional_point_permut(permut, lines, lines_through_exceptional_point):
    pts = {tuple(sorted(lst)): i for i, lst in enumerate(lines_through_exceptional_point)}
    idx_offset = len(lines) - len(lines_through_exceptional_point)
    return [pts[tuple(sorted([i^permut for i in lns]))]+idx_offset for lns in lines_through_exceptional_point] # type: ignore

def compute_x2_orbits(group_action_matrix: sp.Matrix, print_to_terminal=False, lines=None, lines_through_exceptional_point=None, labels=None) -> list[list[int]]:
    if lines is None or lines_through_exceptional_point is None:
        lines, lines_through_exceptional_point = compute_lines()
    if print_to_terminal and labels is None:
        labels = compute_line_labels(lines, lines_through_exceptional_point)
    
    p = compute_x1_permutation(group_action_matrix)
    num_exceptional = len(lines_through_exceptional_point)
    # for the equivalence class curves we simply compute where one representive goes
    image_under_action = [equivalence_class_index_from_line_index(line[0]^p, lines) for line in lines[:-num_exceptional]]
    # for the exceptional points, the image of the intersecting lines is the intersection of the images of the lines
    image_under_action.extend(exceptional_point_permut(p, lines, lines_through_exceptional_point))
    permut = Permutation(image_under_action)
    
    if print_to_terminal:
        pprint([[labels[i] for i in cycle] for cycle in permut.cyclic_form])
    
    return permut.full_cyclic_form
