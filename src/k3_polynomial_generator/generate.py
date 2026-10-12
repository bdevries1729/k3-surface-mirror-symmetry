import csv, json
from itertools import permutations

from polynomial import Polynomial, Term
from weight_set import WeightSet

weights_filename = "src/k3_polynomial_generator/95_weights.csv"
exponent_matrices_filename = "src/k3_polynomial_generator/output/exponent_matrices.json"
num_vars = 4


def read_weights() -> list[WeightSet]:
    with open(weights_filename, mode='r') as weights_file:
        return [WeightSet(lst) for lst in csv.reader(weights_file)]


def generate_all_terms(weight_set: WeightSet) -> list[list[Term]]:
    total = weight_set.get_total()
    trms = [[] for _ in range(num_vars)]

    for j in range(num_vars):
        w_j = weight_set.get(j)

        if total % w_j == 0:
            trms[j].append(Term(j, [total // w_j if k == j else 0 for k in range(num_vars)]))

        for i in range(num_vars):
            if i == j:
                continue

            w_i = weight_set.get(i)
            if (total - w_i) % w_j == 0:
                term_exponents = [0 for _ in range(num_vars)]
                term_exponents[j] = (total - w_i) // w_j
                term_exponents[i] = 1
                trms[j].append(Term(j, term_exponents))

    return list(filter(lambda j_terms: len(j_terms) > 0, trms))


def allowed_new_term(previous_terms: list[Term], new_term: Term) -> bool:
    for previous_term in previous_terms:
        if not new_term.is_compatible_with(previous_term):
            return False

    return True


def generate_term_combinations(all_terms: list[list[Term]], previous_terms: list[Term]) -> list[list[Term]]:
    if len(previous_terms) == num_vars:
        yield previous_terms
    else:
        for term in all_terms[len(previous_terms)]:
            if allowed_new_term(previous_terms, term):
                for next_combination in generate_term_combinations(all_terms, previous_terms + [term]):
                    yield next_combination


def variable_permutation_sets(weight_set: WeightSet) -> list[list[int]]:
    var_perms = []
    weight_vals = weight_set.get_all_weights()
    weight_occurrences = {w: weight_vals.count(w) for w in weight_vals}
    for w in weight_occurrences:
        if weight_occurrences[w] > 1:
            var_perms.append([i for i in range(len(weight_vals)) if weight_vals[i] == w])
    return var_perms


def permute_list(list_to_permute: list[int], perm_list: list[int]) -> list[int]:
    j = 0
    new_permute = list_to_permute.copy()
    for i, elem in enumerate(list_to_permute):
        if elem in perm_list:
            new_permute[i] = perm_list[j]
            j += 1
    return new_permute


def permutations_for_var_set(list_to_permute: list[int], var_set: list[list[int]]) -> list[int]:
    if len(var_set) == 0:
        yield list_to_permute
    else:
        for perm_tuple in permutations(var_set[0]):
            for next_perm in permutations_for_var_set(permute_list(list_to_permute, list(perm_tuple)), var_set[1::]):
                yield next_perm


def permute_poly(poly_to_permute: list[Term], permutation: list[int]):
    permuted_poly = poly_to_permute.copy()
    # Swap rows
    for i, j in enumerate(permutation):
        permuted_poly[j] = poly_to_permute[i]
    # Swap cols
    for index, term in enumerate(permuted_poly):
        exponents_to_permute = term.get_exponents()
        permuted_exponents = exponents_to_permute.copy()
        for i, j in enumerate(permutation):
            permuted_exponents[j] = exponents_to_permute[i]
        permuted_poly[index] = Term(permutation[term.get_index()], permuted_exponents)
    return permuted_poly


def filter_for_unique_polynomials(weight_set: WeightSet, all_combinations: list[list[Term]]) -> list[Polynomial]:
    unique_combinations = []
    for poly in all_combinations:
        is_new = True
        for permutation in permutations_for_var_set([i for i in range(4)], variable_permutation_sets(weight_set)):
            new_poly = permute_poly(poly, permutation)
            if new_poly in unique_combinations:
                is_new = False
        if is_new:
            unique_combinations.append(poly)
    return [Polynomial(p) for p in unique_combinations]


def generate_polynomials(weight_set: WeightSet, filter_duplicates: bool = True) -> list[Polynomial]:
    all_terms = generate_all_terms(weight_set)
    all_combinations = generate_term_combinations(all_terms, [])
    if filter_duplicates:
        return filter_for_unique_polynomials(weight_set, all_combinations)
    return [Polynomial(p) for p in all_combinations]

print(f"Reading weights from {weights_filename}")
weights = read_weights()
print(weights)
print("Done!\n")
polynomials = []
print("Generating...\n")
for weight in weights:
    print("Weight: ", weight)
    polys_with_weight = generate_polynomials(weight)
    for poly in polys_with_weight:
        print(poly)
    polynomials.extend([[weight.get_all_weights(), poly.get_exponent_matrix()] for poly in polys_with_weight])
    print("")

with open(exponent_matrices_filename, "w") as exponent_matrices_file:
    json.dump(polynomials, exponent_matrices_file)
print(f"exponent matrices saved to {exponent_matrices_filename}")
