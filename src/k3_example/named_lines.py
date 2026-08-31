import sympy as sp
from sympy import I
from k3_example.ci_matrices import c1

def named_lines() -> dict:
    '''
    Returns a dictionary of the named lines (such as xz or ybetabar) and the corresponding matrix
    '''
    planes = {
        'x': [1, 0, 0, 0],
        'y': [0, 1, 0, 0],
        'z': [0, 0, 1, 0],
        'w': [0, 0, 0, 1],
        'alpha': [1, I, 0, 0],
        'alphabar': [1, -I, 0, 0],
        'beta': [0, 0, 1, I],
        'betabar': [0, 0, 1, -I]
    }
    return {
        'xz': sp.Matrix([planes['x'], planes['z']]),
        'xw': sp.Matrix([planes['x'], planes['w']]),
        'yz': sp.Matrix([planes['y'], planes['z']]),
        'yw': sp.Matrix([planes['y'], planes['w']]),
        'xbeta': sp.Matrix([planes['x'], planes['beta']]),
        'xbetabar': sp.Matrix([planes['x'], planes['betabar']]),
        'ybeta': sp.Matrix([planes['y'], planes['beta']]),
        'ybetabar': sp.Matrix([planes['y'], planes['betabar']]),
        'zbeta': sp.Matrix([planes['z'], planes['alpha']]),
        'zbetabar': sp.Matrix([planes['z'], planes['alphabar']]),
        'wbeta': sp.Matrix([planes['w'], planes['alpha']]),
        'wbetabar': sp.Matrix([planes['w'], planes['alphabar']]),
        'alphabeta': sp.Matrix([planes['alpha'], planes['beta']]),
        'alphabetabar': sp.Matrix([planes['alpha'], planes['betabar']]),
        'alphabarbeta': sp.Matrix([planes['alphabar'], planes['beta']]),
        'alphabarbetabar': sp.Matrix([planes['alphabar'], planes['betabar']]),
    }

def c1_name(m: int, n: int, unused_lines: dict) -> tuple[str, dict]:
    '''
    Returns the alternate name for c1(m, n), and the remaining unused lines.
    '''
    c1_mat_rref = c1(m, n).rref()[0]
    for name, line_mat_rref in unused_lines.items():
        if c1_mat_rref == line_mat_rref:
            new_unused_lines = unused_lines.copy()
            new_unused_lines.pop(name)
            return name, new_unused_lines
    return 'unknown', unused_lines


def compute_c1_names() -> list:
    '''
    Returns an array of c1 line names, where the name for c1(m, n) is in the (m, n) position.
    '''
    
    lines = named_lines()
    lines_rref = {name: line_mat.rref()[0] for name, line_mat in lines.items()}
    lines_to_search = lines_rref.copy()

    names = [[''] * 4] * 4
    for m in range(4):
        for n in range(4):
            name, lines_to_search = c1_name(n, m, lines_to_search)
            names[m][n] = name
    return names

def get_label(i: int, m: int, n: int, names: list) -> str:
    '''
    For line ci(m, n) will return the string of the label. If the line is c1 and in names, then will 
    also append the name of that line.
    '''
    if i == 1:
        return f'c{i}({m}, {n}) - {names[m][n]}'
    return f'c{i}({m}, {n})'
