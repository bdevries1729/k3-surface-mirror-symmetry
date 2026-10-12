import sympy as sp
from k3_example.x1.intersections import compute_intersection_matrix
from k3_example.x2.lines import lines, exceptional_points, lines_through_exceptional_point, equivalence_class_index_from_line_index

x1_intersection_matrix = compute_intersection_matrix()
line_idxs = [i for i in range(x1_intersection_matrix.rows)] # as we delete rows/cols this lets us keep track easily

modified_x1_intersections = x1_intersection_matrix.copy()
# now we delete the lines which already have a representive in the equivalence class
# this is incorrect when we have two equivalence classes intersecting which each have two lines. Otherwise, this works.
# We will go back and fix the other case after.
for line_class in lines[:-len(exceptional_points)]:
    if len(line_class) > 1:
        for i in line_class[1:]:
            j = line_idxs.index(i)
            line_idxs.remove(i)
            modified_x1_intersections = modified_x1_intersections.minor_submatrix(j, j)
# now fix the case when two lines intersect two other lines. The quotients should intersect twice
for i, line_i in enumerate(lines):
    for j, line_j in enumerate(lines):
        if len(line_i) == 2 and len(line_j) == 2 and modified_x1_intersections[i, j] == 1:
            modified_x1_intersections[i, j] = 2

x2_intersection_matrix = sp.Matrix.zeros(len(lines), len(lines))
x2_intersection_matrix[:modified_x1_intersections.rows,:modified_x1_intersections.cols] = modified_x1_intersections
# the exceptional curves are lines so 2g - 2 = -2
for i in range(len(lines) - len(exceptional_points), len(lines)):
    x2_intersection_matrix[i, i] = -2
# there are A1 singularities, and so for each we perform a blow up and modify 
for exceptional_idx, set_of_intersecting_lines in enumerate(lines_through_exceptional_point):
    for line in set_of_intersecting_lines:
        class_idx = equivalence_class_index_from_line_index(line)
        other_lines = [other_line for other_line in set_of_intersecting_lines if other_line != line]
        for other_line in other_lines:
            other_class_idx = equivalence_class_index_from_line_index(other_line)
            x2_intersection_matrix[class_idx, other_class_idx] = 0
        x2_intersection_matrix[class_idx, exceptional_idx + len(lines) - len(exceptional_points)] = 1
        x2_intersection_matrix[exceptional_idx + len(lines) - len(exceptional_points), class_idx] = 1

sp.pprint(x2_intersection_matrix)
# todo: some bugs still in the code giving an incorrect matrix. However, it is mostly correct, and 