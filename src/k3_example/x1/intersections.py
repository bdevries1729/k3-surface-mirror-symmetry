import sympy as sp
import csv
from k3_example.named_lines import get_label, compute_c1_names
from k3_example.x1.lines import ci_labels, ci_matrices



def intersect(line_mat_1: sp.Matrix, line_mat_2: sp.Matrix) -> bool:
    '''
    Takes the matrix defining two lines, and computes their intersection (in projective space).
    Returns True if they intersect, False otherwise.
    '''
    return line_mat_1.col_join(line_mat_2).det() == 0

def intersection_matrix_value(i: int, j: int) -> int:
    '''
    For row i and column j, returns the intersection number to be used in the intersection matrix for X1
    Notice that the order follows that of ci_labels above.
    '''
    if i == j:
        return -2 
    return 1 if intersect(ci_matrices[i], ci_matrices[j]) else 0


def compute_intersection_matrix() -> sp.Matrix:
    n = len(ci_labels)
    return sp.Matrix([[intersection_matrix_value(i, j) for i in range(n)] for j in range(n)])

def generate_and_output_matrix(print_to_terminal:bool=True) -> None:
    '''
    Generates the X1 intersection matrix, optionally prints to the terminal, and then saves the 
    matrix to `output/x1_intersections.txt`.
    '''
    x1_int_matrix = compute_intersection_matrix()
    sp.pprint(x1_int_matrix)
    with open('output/x1_intersections.txt', 'w', newline='') as f:
        # write the curve labels first
        f.write('Curves:\n')
        names = compute_c1_names()
        labels = [get_label(i, m, n, names) for i, m, n in ci_labels]
        f.write('\n'.join([f'{i+1}. {labels[i]}' for i in range(len(labels))]))
        f.write('\n\n')

        writer = csv.writer(f)
        writer.writerows(x1_int_matrix.tolist())
