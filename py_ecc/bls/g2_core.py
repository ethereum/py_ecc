from typing import Tuple
from math import (
    ceil,
    log2,
)
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import big_endian_to_int

from py_ecc.optimized_bls12_381 import (
    G1,
    multiply,
    curve_order,
)

from .hash import (
    hkdf_expand,
    hkdf_extract,
)
from .g2_primatives import (
    G1_to_pubkey,
    pubkey_to_G1,
    subgroup_check,
)


def priv_to_pub(privkey: int) -> BLSPubkey:
    return G1_to_pubkey(multiply(G1, privkey))


def KeyGen(IKM: bytes) -> Tuple[BLSPubkey, int]:
    prk = hkdf_extract(b'BLS-SIG-KEYGEN-SALT-', IKM)
    l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
    okm = hkdf_expand(prk, b'', l)
    x = big_endian_to_int(okm) % curve_order
    return (priv_to_pub(x), x)


def KeyValidate(PK: BLSPubkey) -> bool:
    xP = pubkey_to_G1(PK)
    return subgroup_check(xP)


def CoreSign(SK: int, message: bytes, DST: bytes) -> BLSSignature:
    pass


def CoreVerify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    pass


def Aggregate(*signatures: BLSSignature) -> BLSSignature:
    pass


def CoreAggregateVerify(*args) -> bool:
    pass
