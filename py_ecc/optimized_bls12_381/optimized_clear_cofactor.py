from py_ecc.typing import (
    Optimized_Field,
    Optimized_Point3D,
)

from .constants import (
    H_EFF,
)
from .optimized_curve import (
    multiply,
)


# Cofactor Clearing Method by Multiplication
# There is an optimization based on this Section 4.1 of https://eprint.iacr.org/2017/419
# However there is a patent `US patent 7110538` so I'm not sure if it can be used.
def multiply_clear_cofactor_G2(
    p: Optimized_Point3D[Optimized_Field],
) -> Optimized_Point3D[Optimized_Field]:
    return multiply(p, H_EFF)
