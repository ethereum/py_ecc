from typing import (
    Sequence,
)

from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    ValidationError,
)

from py_ecc.fields import (
    optimized_bls12_381_FQ12 as FQ12,
)
from py_ecc.optimized_bls12_381 import (
    G1,
    Z1,
    Z2,
    add,
    final_exponentiate,
    multiply,
    neg,
    pairing,
    is_inf,
    curve_order,
)
from .utils import (
    G1_to_pubkey,
    G2_to_signature,
    hash_to_G2,
    pubkey_to_G1,
    signature_to_G2,
)


def sign(sk: int, message: bytes) -> BLSSignature:
    return G2_to_signature(
        multiply(
            hash_to_G2(message),
            sk,
        ))


def privtopub(k: int) -> BLSPubkey:
    return G1_to_pubkey(multiply(G1, k))


def verify(pk: BLSPubkey,
           message: bytes,
           signature: BLSSignature) -> bool:
    signature_point = signature_to_G2(signature)
    if not is_inf(multiply(signature_point, curve_order)):
        return False
    try:
        final_exponentiation = final_exponentiate(
            pairing(
                signature_point,
                G1,
                final_exponentiate=False,
            ) * pairing(
                hash_to_G2(message),
                neg(pubkey_to_G1(pk)),
                final_exponentiate=False,
            )
        )
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def aggregate_signatures(signatures: Sequence[BLSSignature]) -> BLSSignature:
    o = Z2
    for s in signatures:
        o = add(o, signature_to_G2(s))
    return G2_to_signature(o)


def aggregate_pubkeys(pks: Sequence[BLSPubkey]) -> BLSPubkey:
    o = Z1
    for p in pks:
        o = add(o, pubkey_to_G1(p))
    return G1_to_pubkey(o)


def aggregate_verify(pks: Sequence[BLSPubkey],
                     messages: Sequence[bytes],
                     signature: BLSSignature) -> bool:
    len_msgs = len(messages)

    if len(pks) != len_msgs:
        raise ValidationError(
            "len(pks) (%s) should be equal to len(message) (%s)" % (
                len(pks), len_msgs
            )
        )

    signature_point = signature_to_G2(signature)
    if not is_inf(multiply(signature_point, curve_order)):
        return False

    try:
        o = FQ12([1] + [0] * 11)
        for m_pubs in set(messages):
            # aggregate the pubs
            group_pub = Z1
            for i in range(len_msgs):
                if messages[i] == m_pubs:
                    group_pub = add(group_pub, pubkey_to_G1(pks[i]))

            o *= pairing(hash_to_G2(m_pubs), group_pub, final_exponentiate=False)
        o *= pairing(signature_point, neg(G1), final_exponentiate=False)

        final_exponentiation = final_exponentiate(o)
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def fast_aggregate_verify(pks: Sequence[BLSPubkey],
                          message: bytes,
                          signature: BLSSignature) -> bool:
    aggregate_pubkey = aggregate_pubkeys(pks)
    return verify(aggregate_pubkey, message, signature)
