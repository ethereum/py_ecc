from eth_utils import (
    big_endian_to_int,
)

from py_ecc.fields import (
    optimized_bls12_381_FQ2 as FQ2,
)
from py_ecc.optimized_bls12_381 import (
    add,
    iso_map_G2,
    multiply_clear_cofactor_G2,
    optimized_swu_G2,
)

from .constants import HASH_TO_G2_L
from .typing import (
    G2Uncompressed,
)
from .hash import (
    hkdf_expand,
    hkdf_extract,
)


# Hash to G2
def hash_to_G2(message: bytes, DST: bytes) -> G2Uncompressed:
    """
    Convert a message to a point on G2 as defined here:
    https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-05#section-3

    Contants and inputs follow the ciphersuite ``BLS12381G2-SHA256-SSWU-RO-`` defined here:
    https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-05#section-8.9.2
    """
    u0 = hash_to_base_FQ2(message, 0, DST)
    u1 = hash_to_base_FQ2(message, 1, DST)
    q0 = map_to_curve_G2(u0)
    q1 = map_to_curve_G2(u1)
    r = add(q0, q1)
    p = clear_cofactor_G2(r)
    return p


def hash_to_base_FQ2(message: bytes, ctr: int, DST: bytes) -> FQ2:
    """
    Hash To Base for FQ2

    Convert a message to a point in the finite field as defined here:
    https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-05#section-5
    """
    m_prime = hkdf_extract(DST, message + b'\x00')
    info_pfx = b'H2C' + bytes([ctr])
    e = []

    #  for i in (1, ..., m), where m is the extension degree of FQ2
    for i in range(1, 3):
        info = info_pfx + bytes([i])
        t = hkdf_expand(m_prime, info, HASH_TO_G2_L)
        e.append(big_endian_to_int(t))

    return FQ2(e)


def map_to_curve_G2(u: FQ2) -> G2Uncompressed:
    """
    Map To Curve for G2

    First, convert FQ2 point to a point on the 3-Isogeny curve.
    SWU Map: https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-05#section-6.6.2

    Second, map 3-Isogeny curve to BLS12-381-G2 curve.
    3-Isogeny Map: https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-05#appendix-C.3
    """
    (x, y, z) = optimized_swu_G2(u)
    return iso_map_G2(x, y, z)


def clear_cofactor_G2(p: G2Uncompressed) -> G2Uncompressed:
    """
    Clear Cofactor via Multiplication

    Ensure a point falls in the correct sub group of the curve.
    """
    return multiply_clear_cofactor_G2(p)
