import sympy as sp

def same_line(line_1_matrix: sp.Matrix, line_2_matrix: sp.Matrix, row_reduce=True) -> bool:
    '''
    Checks if two lines, defined as the null space of corresponding matrices, are the same. The argument
    `row_reduce` can be set to `False` if the matrices have already been row reduced for efficiency.
    '''
    if not row_reduce:
        return line_1_matrix == line_2_matrix
    return line_1_matrix.rref() == line_2_matrix.rref()

def equivalence_class_index_from_line_index(i, line_equiv_classes):
    return next((j for j, equiv_class in enumerate(line_equiv_classes) if i in equiv_class), None)
