import k3_example.automorphisms.sigma_l as sigma_l
import k3_example.automorphisms.sigma_r as sigma_r
from k3_example.x1.orbits import compute_x1_orbits
from k3_example.x1.lines import ci_labels
from k3_example.x2.lines import compute_exceptional_points_and_lines as compute_exceptional_x2
from k3_example.named_lines import compute_c1_names, get_label

def A1_singularity_identifiers(x2_lines_through_except_pts):
    # two A1 singularities, located at points
    # (c1(1, 1) = alphabarbetabar) ∩ (c1(1, 0) = alphabarz) ∩ (c1(1, 3) = alphabarbeta) ∩ (c1(1, 2) = alphabarw)
    #    ~ (c1(2, 3) = ybeta) ∩ (c1(3, 3) = alphabeta) ∩ (c1(0, 3) = xbeta) ∩ (c1(1, 3) = alphabarbeta)
    # (c1(0, 1) = xbetabar) ∩ (c1(1, 1) = alphabarbetabar) ∩ (c1(2, 1) = ybetabar) ∩ (c1(3, 1) = alphabetabar)
    #    ~(c1(3, 0) = alphaz) ∩ (c1(3, 3) = alphabeta) ∩ (c1(3, 2) = alphaw) ∩ (c1(3, 1) = alphabetabar)
    # These correspond (respectively) to equivalence classes of x2_exceptional points with indices 35~38 and 34~39 

    # To know how an exceptinal curve is mapped under an automorphism, it suffices to know where the singular 
    # point lands, which is deduced from the mapping of the intersecting lines

    offset = 32 # number of x2 curves which are not exceptional
    return [
        [x2_lines_through_except_pts[35 - offset], x2_lines_through_except_pts[38 - offset]],
        [x2_lines_through_except_pts[34 - offset], x2_lines_through_except_pts[39 - offset]]
    ]

def A3_singularity_identifiers(x2_lines_through_except_pts):
    # four A3 singularities, which are located at points 
    # (c1(0, 0) = xz) ∩ (c1(0, 1) = xbetabar) ∩ (c1(0, 2) = xw) ∩ (c1(0, 3) = xbeta)
    # (c1(1, 2) = alphabarw) ∩ (c1(2, 2) = yw) ∩ (c1(0, 2) = xw) ∩ (c1(3, 2) = alphaw)
    # (c1(0, 0) = xz) ∩ (c1(3, 0) = alphaz) ∩ (c1(1, 0) = alphabarz) ∩ (c1(2, 0) = yz)
    # (c1(2, 2) = yw) ∩ (c1(2, 3) = ybeta) ∩ (c1(2, 0) = yz) ∩ (c1(2, 1) = ybetabar)
    # these correspond (respectively) to x2_exceptional points whose indices are 32, 33, 36, 37

    # To know how an exceptional curve is mapped under an automorphism, we need to know where the corresponding 
    # singular point maps, as well as the orientation of the three exceptional lines. 
    # We determine orientation by ensuring intersections are respected by the automorphism. Hence, the middle 
    # line always maps to itself and the lines on either side are associated with the lines with which they 
    # intersect. For these, we use the indices from X1 of those lines.
    
    # recall that the coordinate X1 lines have indices
    # 0. c1(0, 0) = xz
    # 2. c1(2, 2) = yw
    # 4. c1(0, 2) = xw
    # 6. c1(2, 0) = yz

    offset = 32 # number of x2 curves which are not exceptional
    return [
        [x2_lines_through_except_pts[32 - offset], 0],
        [x2_lines_through_except_pts[32 - offset], None],
        [x2_lines_through_except_pts[32 - offset], 4],
        [x2_lines_through_except_pts[33 - offset], 2],
        [x2_lines_through_except_pts[33 - offset], None],
        [x2_lines_through_except_pts[33 - offset], 4],
        [x2_lines_through_except_pts[36 - offset], 0],
        [x2_lines_through_except_pts[36 - offset], None],
        [x2_lines_through_except_pts[36 - offset], 6],
        [x2_lines_through_except_pts[37 - offset], 2],
        [x2_lines_through_except_pts[37 - offset], None],
        [x2_lines_through_except_pts[37 - offset], 6]
    ]

def compute_quotient_orbits():
    quotient_matrix = sigma_l.matrix * sigma_r.matrix ** -1
    return compute_x1_orbits(quotient_matrix)

def compute_lines():
    _, x2_lines_through_except_pts = compute_exceptional_x2()
    a1_identifiers = A1_singularity_identifiers(x2_lines_through_except_pts)
    a3_identifiers = A3_singularity_identifiers(x2_lines_through_except_pts)
    lines = compute_quotient_orbits()
    
    # In fact, several of these quotients are nodal so we will drop them. We drop the equivalence class of the following
    # with these X1 curve indices:
    # 24: c2(0, 1)
    # 29: c2(1, 0)
    # 40: c3(0, 1)
    # 45: c3(1, 0)
    def nodal(equiv_class):
        return True in [(i in equiv_class) for i in [24, 29, 40, 45]]
    lines = [equiv_class for equiv_class in lines if not nodal(equiv_class)]

    # now we add the exceptional curves
    lines.extend([[i] for i in range(len(ci_labels), len(ci_labels)+len(a1_identifiers)+len(a3_identifiers))])
    return lines, a1_identifiers, a3_identifiers

def compute_a1_labels(a1_identifiers, line_labels):
    return [' ~ '.join(['∩'.join(['('+line_labels[i]+')' for i in line_set]) for line_set in identifier]) for identifier in a1_identifiers]

def compute_a3_labels(a3_identifiers, line_labels):
    def orientation_label(orientation_identifier):
        if orientation_identifier is None:
            return "center"
        return line_labels[orientation_identifier]
    
    return ['∩'.join(['('+line_labels[i]+')' for i in identifier[0]]) + ' + (' + orientation_label(identifier[1]) + ')' for identifier in a3_identifiers]

def compute_line_labels(lines, a1_identifiers, a3_identifiers, c1_names=None):
    if c1_names is None:
        c1_names = compute_c1_names()
    line_labels = [get_label(*label_indices, names=c1_names) for label_indices in ci_labels]
    # chose ordering: A1 exceptional curves then A3 exceptional curves
    line_labels.extend(compute_a1_labels(a1_identifiers, line_labels))
    line_labels.extend(compute_a3_labels(a3_identifiers, line_labels))
    line_equivalence_class_labels = [' ~ '.join([line_labels[i] for i in line_equivalence_class]) for line_equivalence_class in lines]
    return line_equivalence_class_labels
