import sympy as sp
import csv

def output_matrix(filename, curve_labels, intersection_matrix, print_to_terminal=True) -> None:
    if print_to_terminal:
        sp.pprint(intersection_matrix)

    with open('src/k3_example/output/'+filename, 'w', newline='') as f:
        # write the curve labels first
        f.write('Curves:\n')
        f.write('\n'.join([f'{i+1}. {curve_labels[i]}' for i in range(len(curve_labels))]))
        f.write('\n\n')

        writer = csv.writer(f)
        writer.writerows(intersection_matrix.tolist())
