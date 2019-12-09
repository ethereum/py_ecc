from eth_typing import (
    BLSSignature,
    BLSPubkey,
)
from eth_utils import big_endian_to_int

from py_ecc.optimized_bls12_381 import (
    is_inf,
    multiply,
    curve_order,
)

from .utils import (
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


def subgroup_check(P) -> bool:
    return is_inf(multiply(P, curve_order))


def G2_to_signature(pt: G2Uncompressed) -> BLSSignature:
    z1, z2 = compress_G2(pt)
    return BLSSignature(
        z1.to_bytes(48, "big") + z2.to_bytes(48, "big")
    )


def signature_to_G2(signature: BLSSignature) -> G2Uncompressed:
    p = G2Compressed(
        (big_endian_to_int(signature[:48]), big_endian_to_int(signature[48:]))
    )
    return decompress_G2(p)


def G1_to_pubkey(pt: G1Uncompressed) -> BLSPubkey:
    z = compress_G1(pt)
    return BLSPubkey(z.to_bytes(48, "big"))


def pubkey_to_G1(pubkey: BLSPubkey) -> G1Uncompressed:
    z = big_endian_to_int(pubkey)
    return decompress_G1(G1Compressed(z))
