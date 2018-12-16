import sys

from .bls12_381_curve import (  # noqa: F401
    bls12_381,
    BLS12_381_Curve,
    optimized_bls12_381,
    Optimized_BLS12_381_Curve,
)

from .bn128_curve import (  # noqa: F401
    bn128,
    BN128_Curve,
    optimized_bn128,
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

from .validate_constants import validate_constants


sys.setrecursionlimit(max(100000, sys.getrecursionlimit()))

# Check all the constants are valid, before using them
validate_constants()
