import sys

from .bls12_381_curve import (
    BLS12_381_Curve,
    Optimized_BLS12_381_Curve,
)

from .bn128_curve import (
    BN128_Curve,
    Optimized_BN128_Curve,
)

from .field_elements import (  # noqa: F401
    FQ,
    FQP,
    FQ2,
    FQ12,
)

from .optimized_field_elements import (  # noqa: F401
    FQ as optimized_FQ,
    FQP as optimized_FQP,
    FQ2 as optimized_FQ2,
    FQ12 as optimized_FQ12,
)

from .secp256k1 import secp256k1  # noqa: F401


sys.setrecursionlimit(max(100000, sys.getrecursionlimit()))

bn128 = BN128_Curve()
optimized_bn128 = Optimized_BN128_Curve()

bls12_381 = BLS12_381_Curve()
optimized_bls12_381 = Optimized_BLS12_381_Curve()
