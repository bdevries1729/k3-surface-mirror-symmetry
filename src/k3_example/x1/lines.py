from k3_example.ci_matrices import c

# ci(m, n) order of the (m, n) tuples for the intersection matrix
m_n_order = [
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [0, 2],
    [1, 3],
    [2, 0],
    [3, 1],
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [0, 3],
    [1, 0],
    [2, 1],
    [3, 2]
]

ci_labels = [[i, m, n] for i in range(1, 4) for m, n in m_n_order]
ci_matrices = [c(i, m, n) for i, m, n in ci_labels]