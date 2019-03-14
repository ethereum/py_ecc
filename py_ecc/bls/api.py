from typing import (
    Sequence,
)

from eth_typing import (
    BLSPubkey,
    BLSSignature,
    Hash32,
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
)
from .utils import (
    G1_to_pubkey,
    G2_to_signature,
    hash_to_G2,
    pubkey_to_G1,
    signature_to_G2,
)


def sign(message_hash: Hash32,
         privkey: int,
         domain: int) -> BLSSignature:
    return G2_to_signature(
        multiply(
            hash_to_G2(message_hash, domain),
            privkey,
        ))


def privtopub(k: int) -> BLSPubkey:
    return G1_to_pubkey(multiply(G1, k))


def verify(message_hash: Hash32, pubkey: BLSPubkey, signature: BLSSignature, domain: int) -> bool:
    try:
        final_exponentiation = final_exponentiate(
            pairing(
                signature_to_G2(signature),
                G1,
                final_exponentiate=False,
            ) *
            pairing(
                hash_to_G2(message_hash, domain),
                neg(pubkey_to_G1(pubkey)),
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


def aggregate_pubkeys(pubkeys: Sequence[BLSPubkey]) -> BLSPubkey:
    o = Z1
    for p in pubkeys:
        o = add(o, pubkey_to_G1(p))
    return G1_to_pubkey(o)


def verify_multiple(pubkeys: Sequence[BLSPubkey],
                    message_hashes: Sequence[Hash32],
                    signature: BLSSignature,
                    domain: int) -> bool:
    len_msgs = len(message_hashes)

    if len(pubkeys) != len_msgs:
        raise ValidationError(
            "len(pubkeys) (%s) should be equal to len(message_hashes) (%s)" % (
                len(pubkeys), len_msgs
            )
        )

    try:
        o = FQ12([1] + [0] * 11)
        for m_pubs in set(message_hashes):
            # aggregate the pubs
            group_pub = Z1
            for i in range(len_msgs):
                if message_hashes[i] == m_pubs:
                    group_pub = add(group_pub, pubkey_to_G1(pubkeys[i]))

            o *= pairing(hash_to_G2(m_pubs, domain), group_pub, final_exponentiate=False)
        o *= pairing(signature_to_G2(signature), neg(G1), final_exponentiate=False)

        final_exponentiation = final_exponentiate(o)
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False
