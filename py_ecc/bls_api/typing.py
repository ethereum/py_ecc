from typing import (
    NewType,
    Tuple,
)

from py_ecc.fields import (
    optimized_bls12_381_FQ as FQ,
    optimized_bls12_381_FQ2 as FQ2,
)


# TODO: FQ and FQ2 here are invalid types, they need to be fixed in the future
G1Uncompressed = NewType('G1Uncompressed', Tuple[FQ, FQ, FQ])
G1Compressed = NewType('G1Compressed', int)

G2Uncompressed = NewType('G2Uncompressed', Tuple[FQ2, FQ2, FQ2])
G2Compressed = NewType('G2Compressed', Tuple[int, int])
