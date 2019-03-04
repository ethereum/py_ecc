from typing import (
    Sequence,
)
from eth_utils import (
    ValidationError,
)
from py_ecc.optimized_bls12_381 import (
    FQ12,
    G1,
    Z1,
    Z2,
    add,
    final_exponentiate,
    multiply,
    neg,
    pairing,
)
from .typing import (
    BLSPubkey,
    BLSSignature,
    G1Uncompressed,
    G2Uncompressed,
    Hash32,
)
from .utils import (
    G1_to_pubkey,
    G2_to_signature,
    compress_G1,
    compress_G2,
    decompress_G1,
    decompress_G2,
    hash_to_G2,
    pubkey_to_G1,
    signature_to_G2,
)


def sign(message_hash: Hash32,
         privkey: int,
         domain: int) -> BLSSignature:
    return G2_to_signature(
        compress_G2(
            multiply(
                hash_to_G2(message_hash, domain),
                privkey
            )
        ))


def privtopub(k: int) -> BLSPubkey:
    return G1_to_pubkey(compress_G1(
        multiply(G1Uncompressed(G1), k)
    ))


def verify(message_hash: Hash32, pubkey: BLSPubkey, signature: BLSSignature, domain: int) -> bool:
    try:
        final_exponentiation = final_exponentiate(
            pairing(
                decompress_G2(signature_to_G2(signature)),
                G1,
                final_exponentiate=False,
            ) *
            pairing(
                hash_to_G2(message_hash, domain),
                neg(decompress_G1(pubkey_to_G1(pubkey))),
                final_exponentiate=False,
            )
        )
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def aggregate_signatures(signatures: Sequence[BLSSignature]) -> BLSSignature:
    o = G2Uncompressed(Z2)
    for s in signatures:
        o = add(o, decompress_G2(signature_to_G2(s)))
    return G2_to_signature(compress_G2(o))


def aggregate_pubkeys(pubkeys: Sequence[BLSPubkey]) -> BLSPubkey:
    o = G1Uncompressed(Z1)
    for p in pubkeys:
        o = add(o, decompress_G1(pubkey_to_G1(p)))
    return G1_to_pubkey(compress_G1(o))


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
                    group_pub = add(group_pub, decompress_G1(pubkey_to_G1(pubkeys[i])))

            o *= pairing(hash_to_G2(m_pubs, domain), group_pub, final_exponentiate=False)
        o *= pairing(decompress_G2(signature_to_G2(signature)), neg(G1), final_exponentiate=False)

        final_exponentiation = final_exponentiate(o)
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False
