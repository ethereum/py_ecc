from py_ecc.fields import (
    optimized_bls12_381_FQ2 as FQ2,
)
from py_ecc.optimized_bls12_381 import (
    field_modulus as q,
)

G2_COFACTOR = 305502333931268344200999753193121504214466019254188142667664032982267604182971884026507427359259977847832272839041616661285803823378372096355777062779109  # noqa: E501
FQ2_ORDER = q ** 2 - 1
EIGTH_ROOTS_OF_UNITY = tuple(
    FQ2([1, 1]) ** ((FQ2_ORDER * k) // 8)
    for k in range(8)
)

POW_2_381 = 2**381
POW_2_382 = 2**382
POW_2_383 = 2**383


# Store all the possible single bytes for faster access in hash-to-field
ALL_BYTES = tuple(bytes([i]) for i in range(256))

# Paramaters for hashing to the field as specified in:
# https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-06#section-8.7
HASH_TO_FIELD_L = 64
HASH_TO_FIELD_B_IN_BYTES = 32
HASH_TO_FIELD_R_IN_BYTES = 64
