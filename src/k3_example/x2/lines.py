from k3_example.x1.orbits import compute_x1_orbits
import k3_example.automorphisms.sigma_l as sigma_l
from k3_example.x1.lines import ci_labels, ci_matrices
from k3_example.x1.intersections import compute_intersection_points
from k3_example.named_lines import get_label, compute_c1_names


def check_c1_lines(set_of_idxs):
    for i in set_of_idxs:
        if i > 15:
            return False
    return True 

def compute_exceptional_points_and_lines():
    # the exceptional points for X2 happen only when 4 c1 lines meet
    int_points = compute_intersection_points().items()
    exceptional_points_and_lines = [(point, list(lines)) for point, lines in int_points if len(lines) == 4 and check_c1_lines(lines)]
    return map(list, zip(*exceptional_points_and_lines))

def compute_quotient_orbits(c1_names=None):
    quotient_matrix = sigma_l.matrix ** 4
    return compute_x1_orbits(quotient_matrix, print_to_terminal=False, c1_names=c1_names)

def compute_lines(c1_names=None):
    exceptional_points, lines_through_exceptional_point = compute_exceptional_points_and_lines()
    lines = compute_quotient_orbits(c1_names=c1_names)
    # add the exceptional curves to the end
    lines.extend([[i] for i in range(len(ci_matrices), len(ci_matrices)+len(exceptional_points))])
    return lines, lines_through_exceptional_point

def compute_line_labels(lines, lines_through_exceptional_point, c1_names=None):
    if c1_names is None:
        c1_names = compute_c1_names()
    line_labels = [get_label(*label_indices, names=c1_names) for label_indices in ci_labels]
    exceptional_point_labels = [' ∩ '.join(['('+line_labels[i]+')' for i in intersecting_lines]) for intersecting_lines in lines_through_exceptional_point]
    line_labels.extend(exceptional_point_labels)
    line_equivalence_class_labels = [' ~ '.join([line_labels[i] for i in line_equivalence_class]) for line_equivalence_class in lines]
    return line_equivalence_class_labels    
