from typing import (
    Iterable,
    Tuple,
)
from math import (
    ceil,
    log2,
)
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    big_endian_to_int,
    ValidationError,
)

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
)

from .hash import (
    hkdf_expand,
    hkdf_extract,
)
from .hash_to_curve import hash_to_G2
from .g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
)


def PrivToPub(privkey: int) -> BLSPubkey:
    return G1_to_pubkey(multiply(G1, privkey))


def KeyGen(IKM: bytes) -> Tuple[BLSPubkey, int]:
    prk = hkdf_extract(b'BLS-SIG-KEYGEN-SALT-', IKM)
    l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
    okm = hkdf_expand(prk, b'', l)
    x = big_endian_to_int(okm) % curve_order
    return (PrivToPub(x), x)


def KeyValidate(PK: BLSPubkey) -> bool:
    try:
        pubkey_to_G1(PK)
    except ValidationError:
        return False
    return True


def CoreSign(SK: int, message: bytes, DST: bytes) -> BLSSignature:
    message_point = hash_to_G2(message, DST)
    signature_point = multiply(message_point, SK)
    return G2_to_signature(signature_point)


def CoreVerify(PK: BLSPubkey, message: bytes, signature: BLSSignature, DST: bytes) -> bool:
    try:
        signature_point = signature_to_G2(signature)
        final_exponentiation = final_exponentiate(
            pairing(
                signature_point,
                G1,
                final_exponentiate=False,
            ) * pairing(
                hash_to_G2(message, DST),
                neg(pubkey_to_G1(PK)),
                final_exponentiate=False,
            )
        )
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def Aggregate(signatures: Iterable[BLSSignature]) -> BLSSignature:
    accumulator = Z2  # Seed with the point at infinity
    for signature in signatures:
        signature_point = signature_to_G2(signature)
        accumulator = add(accumulator, signature_point)
    return G2_to_signature(accumulator)


def AggregatePKs(PKs: Iterable[BLSPubkey]) -> BLSPubkey:
    accumulator = Z1  # Seed with the point at infinity
    for pk in PKs:
        pubkey_point = pubkey_to_G1(pk)
        accumulator = add(accumulator, pubkey_point)
    return G1_to_pubkey(accumulator)


def CoreAggregateVerify(pairs: Iterable[Tuple[BLSPubkey, bytes]],
                        signature: BLSSignature, DST: bytes) -> bool:
    try:
        signature_point = signature_to_G2(signature)
        accumulator = FQ12([1] + [0] * 11)
        for pk, message in pairs:
            pubkey_point = pubkey_to_G1(pk)
            message_point = hash_to_G2(message, DST)
            accumulator *= pairing(message_point, pubkey_point, final_exponentiate=False)
        accumulator *= pairing(signature_point, neg(G1), final_exponentiate=False)
        return final_exponentiate(accumulator) == FQ12.one()

    except (ValidationError, ValueError, AssertionError):
        return False
