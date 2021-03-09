import sys
import pkg_resources


sys.setrecursionlimit(max(100000, sys.getrecursionlimit()))


from py_ecc import secp256k1  # noqa: F401
from py_ecc import bn128  # noqa: F401
from py_ecc import optimized_bn128  # noqa: F401
from py_ecc import bls12_381  # noqa: F401
from py_ecc import optimized_bls12_381  # noqa: F401
from py_ecc import bls  # noqa: F401

__version__ = pkg_resources.get_distribution("py_ecc").version
