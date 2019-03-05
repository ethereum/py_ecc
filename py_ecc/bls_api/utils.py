from typing import (  # noqa: F401
    Dict,
    Sequence,
    Tuple,
    Union,
)

from eth_utils import (
    big_endian_to_int,
)
from py_ecc.optimized_bls12_381 import (
    FQ,
    FQ2,
    b,
    b2,
    field_modulus as q,
    is_inf,
    is_on_curve,
    multiply,
    normalize,
    Z1,
    Z2,
)

from .hash import (
    hash_eth2,
)
from .typing import (
    BLSPubkey,
    BLSSignature,
    G1Compressed,
    G1Uncompressed,
    G2Compressed,
    G2Uncompressed,
    Hash32,
)
from .constants import (
    POW_2_381,
    POW_2_382,
    POW_2_383,
)

G2_cofactor = 305502333931268344200999753193121504214466019254188142667664032982267604182971884026507427359259977847832272839041616661285803823378372096355777062779109  # noqa: E501
FQ2_order = q ** 2 - 1
eighth_roots_of_unity = [
    FQ2([1, 1]) ** ((FQ2_order * k) // 8)
    for k in range(8)
]


#
# Helpers
#

def coerce_to_int(element: Union[int, FQ]) -> int:
    return element if isinstance(element, int) else element.n


def modular_squareroot(value: FQ2) -> FQ2:
    """
    ``modular_squareroot(x)`` returns the value ``y`` such that ``y**2 % q == x``,
    and None if this is not possible. In cases where there are two solutions,
    the value with higher imaginary component is favored;
    if both solutions have equal imaginary component the value with higher real
    component is favored.
    """
    candidate_squareroot = value ** ((FQ2_order + 8) // 16)
    check = candidate_squareroot ** 2 / value
    if check in eighth_roots_of_unity[::2]:
        x1 = candidate_squareroot / eighth_roots_of_unity[eighth_roots_of_unity.index(check) // 2]
        x2 = -x1
        x1_re, x1_im = coerce_to_int(x1.coeffs[0]), coerce_to_int(x1.coeffs[1])
        x2_re, x2_im = coerce_to_int(x2.coeffs[0]), coerce_to_int(x2.coeffs[1])
        return x1 if (x1_im > x2_im or (x1_im == x2_im and x1_re > x2_re)) else x2
    return None


def _get_x_coordinate(message_hash: Hash32, domain: int) -> FQ2:
    domain_in_bytes = domain.to_bytes(8, 'big')

    # Initial candidate x coordinate
    x_re = big_endian_to_int(hash_eth2(message_hash + domain_in_bytes + b'\x01'))
    x_im = big_endian_to_int(hash_eth2(message_hash + domain_in_bytes + b'\x02'))
    x_coordinate = FQ2([x_re, x_im])  # x_re + x_im * i

    return x_coordinate


def hash_to_G2(message_hash: Hash32, domain: int) -> G2Uncompressed:
    x_coordinate = _get_x_coordinate(message_hash, domain)

    # Test candidate y coordinates until a one is found
    while 1:
        y_coordinate_squared = x_coordinate ** 3 + FQ2([4, 4])  # The curve is y^2 = x^3 + 4(i + 1)
        y_coordinate = modular_squareroot(y_coordinate_squared)
        if y_coordinate is not None:  # Check if quadratic residue found
            break
        x_coordinate += FQ2([1, 0])  # Add 1 and try again

    return multiply(
        G2Uncompressed((x_coordinate, y_coordinate, FQ2([1, 0]))),
        G2_cofactor,
    )


#
# G1
#
def compress_G1(pt: G1Uncompressed) -> G1Compressed:
    """
    A compressed point in group G1 is 384-bit with the order (c_flag, b_flag, a_flag, x),
    where c_flag is always 1,
    b_flag indicates infinity,
    a_flag depends on y, and
    x is the x-coordinate of the point.
    """
    if is_inf(pt):
        # set c_flag = 1 and b_flag = 1, leave a_flag = x = 0
        return G1Compressed(POW_2_383 + POW_2_382)
    else:
        x, y = normalize(pt)
        # Record y's leftmost bit to the a_flag
        a_flag = (y.n * 2) // q
        # set c_flag = 1 and b_flag = 0
        return G1Compressed(x.n + a_flag * POW_2_381 + POW_2_383)


def decompress_G1(z: G1Compressed) -> G1Uncompressed:
    # The case b_flag == 1, indicating the infinity point
    if (z % POW_2_383) // POW_2_382 == 1:
        return G1Uncompressed(Z1)
    x = z % POW_2_381

    # Try solving y coordinate from the equation Y^2 = X^3 + b
    # using quadratic residue
    y = pow((x**3 + b.n) % q, (q + 1) // 4, q)

    if pow(y, 2, q) != (x**3 + b.n) % q:
        raise ValueError(
            "The given point is not on G1: y**2 = x**3 + b"
        )
    # Choose the y whose leftmost bit is equal to the a_flag
    a_flag = (z % POW_2_382) // POW_2_381
    if (y * 2) // q != a_flag:
        y = q - y
    return G1Uncompressed((FQ(x), FQ(y), FQ(1)))


def G1_to_pubkey(pt: G1Uncompressed) -> BLSPubkey:
    z = compress_G1(pt)
    return BLSPubkey(z.to_bytes(48, "big"))


def pubkey_to_G1(pubkey: BLSPubkey) -> G1Uncompressed:
    z = big_endian_to_int(pubkey)
    return decompress_G1(z)

#
# G2
#


def compress_G2(pt: G2Uncompressed) -> G2Compressed:
    if not is_on_curve(pt, b2):
        raise ValueError(
            "The given point is not on the twisted curve over FQ**2"
        )
    if is_inf(pt):
        return G2Compressed((POW_2_383 + POW_2_382, 0))
    x, y = normalize(pt)
    # c_flag1 = 1, b_flag1 = 0
    x_re, x_im = x.coeffs
    _, y_im = y.coeffs
    # Record the leftmost bit of y_im to the a_flag1
    a_flag1 = (y_im * 2) // q
    z1 = x_re + a_flag1 * POW_2_381 + POW_2_383
    # a_flag2 = b_flag2 = c_flag2 = 0
    z2 = x_im
    return G2Compressed((z1, z2))


def decompress_G2(p: G2Compressed) -> G2Uncompressed:
    z1, z2 = p
    # check b_flag1 for infinity
    if (z1 % POW_2_383) // POW_2_382 == 1:
        return G2Uncompressed(Z2)
    x1 = z1 % POW_2_381
    x2 = z2
    x = FQ2([x1, x2])
    y = modular_squareroot(x**3 + b2)
    if y is None:
        raise ValueError("Failed to find a modular squareroot")

    # Choose the y whose leftmost bit of the imaginary part is equal to the a_flag1
    a_flag1 = (z1 % POW_2_382) // POW_2_381
    if (y.coeffs[1] * 2) // q != a_flag1:
        y = FQ2((y * -1).coeffs)

    if not is_on_curve((x, y, FQ2([1, 0])), b2):
        raise ValueError(
            "The given point is not on the twisted curve over FQ**2"
        )
    return G2Uncompressed((x, y, FQ2([1, 0])))


def G2_to_signature(pt: G2Uncompressed) -> BLSSignature:
    z1, z2 = compress_G2(pt)
    return BLSSignature(
        z1.to_bytes(48, "big") +
        z2.to_bytes(48, "big")
    )


def signature_to_G2(signature: BLSSignature) -> G2Uncompressed:
    p = G2Compressed(
        (big_endian_to_int(signature[:48]), big_endian_to_int(signature[48:]))
    )
    return decompress_G2(p)
