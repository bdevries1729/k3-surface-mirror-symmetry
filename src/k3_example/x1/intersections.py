import sympy as sp
from k3_example.named_lines import get_label, compute_c1_names
from k3_example.x1.lines import ci_labels, ci_matrices
from collections import defaultdict
from k3_example.compare import matrix_key
from k3_example.output import output_matrix

def intersect(line_mat_1: sp.Matrix, line_mat_2: sp.Matrix) -> bool:
    '''
    Takes the matrix defining two lines, and computes their intersection (in projective space).
    Returns True if they intersect, False otherwise.
    '''
    return line_mat_1.col_join(line_mat_2).det() == 0

def intersect_point(line_mat_1: sp.Matrix, line_mat_2: sp.Matrix) -> list:
    '''
    Takes the matrix defining two intersecting lines, and computes their intersection point 
    (in projective space). Note error will be thrown if lines do not intersect or have infinite intersection.
    '''
    rref, pivot_indices = line_mat_1.col_join(line_mat_2).rref()
    idxs = list(pivot_indices)
    j = [i for i in range(4) if i not in idxs][0]
    idxs.append(j)
    vals = list(sp.simplify(rref[:-1,list(pivot_indices)]**-1 * rref[:-1,j]))
    vals.append(1)
    return [vals[idxs.index(i)] for i in range(4)]

def intersection_matrix_value(i: int, j: int) -> int:
    '''
    For row i and column j, returns the intersection number to be used in the intersection matrix for X1
    Notice that the order follows that of ci_labels above.
    '''
    if i == j:
        return -2 
    return 1 if intersect(ci_matrices[i], ci_matrices[j]) else 0


def compute_x1_intersection_matrix() -> sp.Matrix:
    n = len(ci_labels)
    return sp.Matrix([[intersection_matrix_value(i, j) for i in range(n)] for j in range(n)])

def generate_and_output_x1_matrix(print_to_terminal:bool=True) -> None:
    names = compute_c1_names()
    labels = [get_label(i, m, n, names) for i, m, n in ci_labels]
    x1_int_matrix = compute_x1_intersection_matrix()
    output_matrix('x1_intersections.txt', labels, x1_int_matrix, print_to_terminal)

# this could be made more efficient. It suffices as a first pass.
def compute_intersection_points():
    print("Computing intersection points. Please wait...")
    pts = defaultdict(set)
    for i in range(len(ci_labels)):
        for j in range(i): # notice i != j so we avoid infinite intersection case
            if intersect(ci_matrices[i], ci_matrices[j]):
                pt = matrix_key(sp.Matrix(intersect_point(ci_matrices[i], ci_matrices[j])))
                pts[pt].update([i, j])
    print("Intersection point computation done!")
    return pts
