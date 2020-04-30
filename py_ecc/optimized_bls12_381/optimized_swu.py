from typing import (
    Tuple,
)
from py_ecc.fields import (
    optimized_bls12_381_FQ2 as FQ2,
)
from py_ecc.typing import (
    Optimized_Point3D,
)

from .constants import (
    ISO_3_A,
    ISO_3_B,
    ISO_3_Z,
    P_MINUS_9_DIV_16,
    ETAS,
    ISO_3_MAP_COEFFICIENTS,
    POSITIVE_EIGTH_ROOTS_OF_UNITY,
)


# Optimized SWU Map - FQ2 to G2': y^2 = x^3 + 240i * x + 1012 + 1012i
# Found in Section 4 of https://eprint.iacr.org/2019/403
def optimized_swu_G2(t: FQ2) -> Tuple[FQ2, FQ2, FQ2]:
    t2 = t ** 2
    iso_3_z_t2 = ISO_3_Z * t2
    temp = iso_3_z_t2 + iso_3_z_t2 ** 2
    denominator = -(ISO_3_A * temp)  # -a(Z * t^2 + Z^2 * t^4)
    temp = temp + FQ2.one()
    numerator = ISO_3_B * temp  # b(Z * t^2 + Z^2 * t^4 + 1)

    # Exceptional case
    if denominator == FQ2.zero():
        denominator = ISO_3_Z * ISO_3_A

    # v = D^3
    v = denominator ** 3
    # u = N^3 + a * N * D^2 + b* D^3
    u = (numerator ** 3) + (ISO_3_A * numerator * (denominator ** 2)) + (ISO_3_B * v)

    # Attempt y = sqrt(u / v)
    (success, sqrt_candidate) = sqrt_division_FQ2(u, v)
    y = sqrt_candidate

    # Handle case where (u / v) is not square
    # sqrt_candidate(x1) = sqrt_candidate(x0) * t^3
    sqrt_candidate = sqrt_candidate * t ** 3

    # u(x1) = Z^3 * t^6 * u(x0)
    u = (iso_3_z_t2) ** 3 * u
    success_2 = False
    etas = ETAS
    for eta in etas:
        # Valid solution if (eta * sqrt_candidate(x1)) ** 2 * v - u == 0
        eta_sqrt_candidate = eta * sqrt_candidate
        temp1 = eta_sqrt_candidate ** 2 * v - u
        if temp1 == FQ2.zero() and not success and not success_2:
            y = eta_sqrt_candidate
            success_2 = True

    if not success and not success_2:
        # Unreachable
        raise Exception("Hash to Curve - Optimized SWU failure")

    if not success:
        numerator = numerator * iso_3_z_t2

    if t.sgn0 != y.sgn0:
        y = -y

    y = y * denominator

    return (numerator, y, denominator)


# Square Root Division
# Return: uv^7 * (uv^15)^((p^2 - 9) / 16) * root of unity
# If valid square root is found return true, else false
def sqrt_division_FQ2(u: FQ2, v: FQ2) -> Tuple[bool, FQ2]:
    temp1 = u * v ** 7
    temp2 = temp1 * v ** 8

    # gamma =  uv^7 * (uv^15)^((p^2 - 9) / 16)
    gamma = temp2 ** P_MINUS_9_DIV_16
    gamma = gamma * temp1

    # Verify there is a valid root
    is_valid_root = False
    result = gamma
    roots = POSITIVE_EIGTH_ROOTS_OF_UNITY
    for root in roots:
        # Valid if (root * gamma)^2 * v - u == 0
        sqrt_candidate = (root * gamma)
        temp2 = sqrt_candidate ** 2 * v - u
        if temp2 == FQ2.zero() and not is_valid_root:
            is_valid_root = True
            result = sqrt_candidate

    return (is_valid_root, result)


# Optimal Map from 3-Isogenous Curve to G2
def iso_map_G2(x: FQ2, y: FQ2, z: FQ2) -> Optimized_Point3D[FQ2]:
    # x-numerator, x-denominator, y-numerator, y-denominator
    mapped_values = [FQ2.zero(), FQ2.zero(), FQ2.zero(), FQ2.zero()]
    z_powers = [z, z ** 2, z ** 3]

    # Horner Polynomial Evaluation
    for (i, k_i) in enumerate(ISO_3_MAP_COEFFICIENTS):
        mapped_values[i] = k_i[-1:][0]
        for (j, k_i_j) in enumerate(reversed(k_i[:-1])):
            mapped_values[i] = mapped_values[i] * x + z_powers[j] * k_i_j

    mapped_values[2] = mapped_values[2] * y  # y-numerator * y
    mapped_values[3] = mapped_values[3] * z  # y-denominator * z

    z_G2 = mapped_values[1] * mapped_values[3]  # x-denominator * y-denominator
    x_G2 = mapped_values[0] * mapped_values[3]  # x-numerator * y-denominator
    y_G2 = mapped_values[1] * mapped_values[2]  # y-numerator * x-denominator

    return (x_G2, y_G2, z_G2)
