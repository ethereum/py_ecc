import sys


sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))


from py_ecc import secp256k1  # noqa: F401
from py_ecc import bn128  # noqa: F401
from py_ecc import optimized_bn128  # noqa: F401
