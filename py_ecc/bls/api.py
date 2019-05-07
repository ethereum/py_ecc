
from secrets import (
    randbelow,
)
from typing import (
    Iterator,
    Sequence,
    Tuple,
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


def _zip(pubkeys: Sequence[BLSPubkey],
         message_hashes: Sequence[Hash32])-> Iterator[Tuple[BLSPubkey, Hash32]]:
    if len(pubkeys) != len(message_hashes):
        raise ValidationError(
            "len(pubkeys) (%s) should be equal to len(message_hashes) (%s)" % (
                len(pubkeys), len(message_hashes)
            )
        )
    return zip(pubkeys, message_hashes)


def verify_multiple(pubkeys: Sequence[BLSPubkey],
                    message_hashes: Sequence[Hash32],
                    signature: BLSSignature,
                    domain: int) -> bool:

    o = FQ12.one()
    for pubkey, message_hash in _zip(pubkeys, message_hashes):
        o *= pairing(
            hash_to_G2(message_hash, domain),
            pubkey_to_G1(pubkey),
            final_exponentiate=False,
        )
    o *= pairing(signature_to_G2(signature), neg(G1), final_exponentiate=False)
    final_exponentiation = final_exponentiate(o)
    return final_exponentiation == FQ12.one()


def verify_multiple_multiple(
        signatures: Sequence[BLSSignature],
        pubkeys_and_messages: Sequence[Tuple[Sequence[BLSPubkey], Sequence[Hash32]]],
        domain: int)-> bool:
    """
    This is the optimized version of len(signatures) rounds of verify_multiple
    """
    if len(signatures) != len(pubkeys_and_messages):
        raise ValidationError(
            "len(signatures) (%s) should be equal to len(pubkeys_and_messages) (%s)" % (
                len(signatures), len(pubkeys_and_messages)
            )
        )

    random_ints = (1,) + tuple(2**randbelow(64) for _ in signatures[:-1])
    o = FQ12.one()
    for r_i, (pubkeys, message_hashes) in zip(random_ints, pubkeys_and_messages):
        for pubkey, message_hash in _zip(pubkeys, message_hashes):
            o *= pairing(
                multiply(hash_to_G2(message_hash, domain), r_i),
                pubkey_to_G1(pubkey),
                final_exponentiate=False,
            )
    agg_sig = Z2
    for r_i, sig in zip(random_ints, signatures):
        agg_sig = add(agg_sig, multiply(signature_to_G2(sig), r_i))
    o *= pairing(agg_sig, neg(G1), final_exponentiate=False)

    final_exponentiation = final_exponentiate(o)
    return final_exponentiation == FQ12.one()
