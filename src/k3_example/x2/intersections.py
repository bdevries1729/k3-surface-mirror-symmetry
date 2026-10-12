import sympy as sp
from k3_example.x1.intersections import compute_x1_intersection_matrix
from k3_example.x2.lines import compute_lines, compute_line_labels, equivalence_class_index_from_line_index
from k3_example.output import output_matrix

def compute_x2_intersection_matrix(lines=None, lines_through_exceptional_point=None, x1_intersection_matrix=None) -> sp.Matrix:
    if x1_intersection_matrix is None:
        x1_intersection_matrix = compute_x1_intersection_matrix()

    if lines is None or lines_through_exceptional_point is None:
        lines, lines_through_exceptional_point = compute_lines()
    num_exceptional = len(lines_through_exceptional_point)

    x2_intersection_matrix = sp.Matrix.zeros(len(lines), len(lines))

    for i in range(len(lines)):
        x2_intersection_matrix[i, i] = -2  # 2g - 2 = -2
    
    for i, line_i in enumerate(lines[:-num_exceptional]):
        for j, line_j in enumerate(lines[:-num_exceptional]):
            if i == j:
                continue
            intersections = 0
            # the next bit of logic is tricky, but going through cases with pictures
            # explicitly can elluciate what is happening here
            idx = min(len(line_i), len(line_j))-len(line_i)
            line_i_to_check = line_i if idx == 0 else line_i[:-idx]
            for line in line_i_to_check:
                if x1_intersection_matrix[line, line_j[0]]:
                    intersections += 1
            x2_intersection_matrix[i, j] = intersections

    # there are A1 singularities at the exceptional points, and so for each we perform a blow up and modify 
    for exceptional_idx, set_of_intersecting_lines in enumerate(lines_through_exceptional_point):
        for line in set_of_intersecting_lines:
            class_idx = equivalence_class_index_from_line_index(line, lines)
            other_lines = [other_line for other_line in set_of_intersecting_lines if other_line != line]
            for other_line in other_lines:
                other_class_idx = equivalence_class_index_from_line_index(other_line, lines)
                x2_intersection_matrix[class_idx, other_class_idx] = 0
            x2_intersection_matrix[class_idx, exceptional_idx + len(lines) - num_exceptional] = 1
            x2_intersection_matrix[exceptional_idx + len(lines) - num_exceptional, class_idx] = 1

    return x2_intersection_matrix

def generate_and_output_x2_matrix(print_to_terminal:bool=True) -> None:
    lines, lines_through_exceptional_point = compute_lines()
    labels = compute_line_labels(lines, lines_through_exceptional_point)
    x2_int_matrix = compute_x2_intersection_matrix(lines=lines, lines_through_exceptional_point=lines_through_exceptional_point)
    output_matrix('x2_intersections.txt', labels, x2_int_matrix, print_to_terminal)
