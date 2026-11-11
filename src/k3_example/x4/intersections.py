import sympy as sp
from k3_example.line_helper import equivalence_class_index_from_line_index
from k3_example.x1.intersections import compute_x1_intersection_matrix
from k3_example.x4.lines import compute_lines, compute_line_labels
from k3_example.output import output_matrix

# TODO: Still a bug in the intersection matrix which needs to be found.

def compute_x4_intersection_matrix(lines=None, a1_identifiers=None, a3_identifiers=None, x1_intersection_matrix=None) -> sp.Matrix:
    if x1_intersection_matrix is None:
        x1_intersection_matrix = compute_x1_intersection_matrix()
    if lines is None or a1_identifiers is None or a3_identifiers is None:
        lines, a1_identifiers, a3_identifiers = compute_lines()

    num_exceptional = len(a1_identifiers) + len(a3_identifiers)

    x4_intersection_matrix = sp.Matrix.zeros(len(lines), len(lines))

    for i in range(len(lines)):
        x4_intersection_matrix[i, i] = -2  # 2g - 2 = -2

    # fix intersections between the non-exceptional lines
    for i, line_i in enumerate(lines[:-num_exceptional]):
        for j, line_j in enumerate(lines[:-num_exceptional]):
            if i == j: # skip the diagonal
                continue
            if (len(line_i) != 4 and len(line_j) != 4): # blow up required
                x4_intersection_matrix[i, j] = 0 # won't intersect after blow up
                continue
            
            four_line_quotient, other_quotient = (line_i, line_j) if len(line_i) == 4 else (line_j, line_i)
            intersections = 0
            for line in other_quotient:
                if x1_intersection_matrix[line, four_line_quotient[0]]:
                        intersections += 1
            x4_intersection_matrix[i, j] = intersections

    # modification for A1 blow ups
    # we already got rid of the intersection of original lines. Now add interection of exceptional curve with lines
    for exceptional_idx, quotient_of_intersecting_lines in enumerate(a1_identifiers):
        i = exceptional_idx + len(lines) - num_exceptional

        for line in quotient_of_intersecting_lines[0]:
            j = equivalence_class_index_from_line_index(line, lines)
            x4_intersection_matrix[j, i] = 1
            x4_intersection_matrix[i, j] = 1

    # now modification for A3 blow ups
    for exceptional_idx, (lines_through_point, side) in enumerate(a3_identifiers):
        i = exceptional_idx + len(lines) - len(a3_identifiers)

        # there are 4 lines going through each of these points
        # two glue together under the group action, and the remaining two map to themselves.
        if side is None:
            # this is the center exceptional curve. The two lines glued together intersect it.
            # we compute the index of this glued double line
            double_line = next((j for j, equiv_class in enumerate(lines) 
                                      for line in lines_through_point 
                                      if len(equiv_class) == 2 and line in equiv_class), 0)
            x4_intersection_matrix[double_line, i] = 1
            x4_intersection_matrix[i, double_line] = 1
            # the center exceptional curve also intersects the side curves
            x4_intersection_matrix[i, i+1] = 1
            x4_intersection_matrix[i+1, i] = 1
            x4_intersection_matrix[i, i-1] = 1
            x4_intersection_matrix[i-1, i] = 1
            continue

        # otherwise, this is a side curve. It intersects the middle exceptional curve as well as one of the 4 lines identified by `side` variable 
        j = equivalence_class_index_from_line_index(side, lines)
        x4_intersection_matrix[j, i] = 1
        x4_intersection_matrix[i, j] = 1
        # the center exceptional line already corrects the intersection with this curve, so we are done

    return x4_intersection_matrix

def generate_and_output_x4_matrix(print_to_terminal:bool=True) -> None:
    lines, a1_identifiers, a3_identifiers = compute_lines()
    labels = compute_line_labels(lines, a1_identifiers, a3_identifiers)
    x4_int_matrix = compute_x4_intersection_matrix(lines=lines, a1_identifiers=a1_identifiers, a3_identifiers=a3_identifiers)
    output_matrix('x4_intersections.txt', labels, x4_int_matrix, print_to_terminal)
