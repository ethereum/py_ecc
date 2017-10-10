# for an explanation of the BN parameters, see https://eprint.iacr.org/2010/429.pdf
# and https://eprint.iacr.org/2005/133.pdf

BN_PARAM_U = 4965661367192848881

curve_order = 36*(BN_PARAM_U**4) + 36*(BN_PARAM_U**3) + 18*(BN_PARAM_U**2) + 6*BN_PARAM_U + 1
field_modulus = 36*(BN_PARAM_U**4) + 36*(BN_PARAM_U**3) + 24*(BN_PARAM_U**2) + 6*BN_PARAM_U + 1
ate_loop_count = 6*BN_PARAM_U + 2

#frobenius_trace = 6*(BN_PARAM_U**2) + 1
#assert field_modulus == 21888242871839275222246405745257275088696311157297823662689037894645226208583
#assert curve_order   == 21888242871839275222246405745257275088548364400416034343698204186575808495617
#assert ate_loop_count = 29793968203157093288
#assert log_ate_loop_count = 63


# extension field coefficients derived (somehow?) from w^6 = (i + 9)
FQ12_modulus_coeffs = [82, 0, 0, 0, 0, 0, -18, 0, 0, 0, 0, 0] # Implied + [1]


# Non-Adjacent Form
def naf(d):
    naf_repr = []
    while d > 0:
        d_j = d % 2
        if d_j == 1 and ( (((d - d_j)//2) % 2) == 1):
            d_j = -1
        d = (d - d_j) // 2
        naf_repr.append(d_j)
    return naf_repr


# used for the miller loop in the pairing check
pseudo_binary_encoding = naf(ate_loop_count)

#pseudo_binary_encoding = [0, 0, 0, 1, 0, 1, 0, -1, 0, 0, 1, -1, 0, 0, 1, 0,
#                          0, 1, 1, 0, -1, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 1,
#                          1, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 1,
#                          1, 0, 0, -1, 0, 0, 0, 1, 1, 0, -1, 0, 0, 1, 0, 1, 1]

assert sum([e * 2**i for i, e in enumerate(pseudo_binary_encoding)]) == ate_loop_count
