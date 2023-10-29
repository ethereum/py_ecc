from importlib.metadata import (
    version as __version,
)
import sys

from py_ecc import (
    bls,
    bls12_381,
    bn128,
    optimized_bls12_381,
    optimized_bn128,
    secp256k1,
)

sys.setrecursionlimit(max(100000, sys.getrecursionlimit()))

__version__ = __version("py_ecc")
