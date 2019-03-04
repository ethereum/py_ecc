# This module will not be included in the PR.
# These types should be replaced with those in eth-typing

from typing import (
    NewType,
    Tuple,
)
from py_ecc.optimized_bls12_381.optimized_field_elements import (
    FQ,
    FQ2,
)


Hash32 = NewType("Hash32", bytes)
BLSPubkey = NewType('BLSPubkey', bytes)  # bytes48
BLSSignature = NewType('BLSSignature', bytes)  # bytes96


G1Uncompressed = NewType('G1Uncompressed', Tuple[FQ, FQ, FQ])
G1Compressed = NewType('G1Compressed', int)

G2Uncompressed = NewType('G2Uncompressed', Tuple[FQ2, FQ2, FQ2])
G2Compressed = NewType('G2Compressed', Tuple[int, int])
