from eth_typing import (
    BLSSignature,
    BLSPubkey,
)

from py_ecc.optimized_bls12_381 import (
    is_inf,
    multiply,
    curve_order,
)
from py_ecc.typing import Optimized_Point3D

from .hash import (
    i2osp,
    os2ip,
)
from .point_compression import (
    compress_G1,
    decompress_G1,
    compress_G2,
    decompress_G2
)
from .typing import (
    G1Compressed,
    G1Uncompressed,
    G2Compressed,
    G2Uncompressed,
)


def subgroup_check(P: Optimized_Point3D) -> bool:
    return is_inf(multiply(P, curve_order))


def G2_to_signature(pt: G2Uncompressed) -> BLSSignature:
    z1, z2 = compress_G2(pt)
    return BLSSignature(i2osp(z1, 48) + i2osp(z2, 48))


def signature_to_G2(signature: BLSSignature) -> G2Uncompressed:
    p = G2Compressed((os2ip(signature[:48]), os2ip(signature[48:])))
    signature_point = decompress_G2(p)
    return signature_point


def G1_to_pubkey(pt: G1Uncompressed) -> BLSPubkey:
    z = compress_G1(pt)
    return BLSPubkey(i2osp(z, 48))


def pubkey_to_G1(pubkey: BLSPubkey) -> G1Uncompressed:
    z = os2ip(pubkey)
    return decompress_G1(G1Compressed(z))
