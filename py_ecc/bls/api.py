from typing import (
    Sequence,
    Tuple,
    Union,
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
from.hash import (
    hkdf_expand,
    hkdf_extract,
)


def Sign(sk: int, message: bytes) -> BLSSignature:
    return G2_to_signature(
        multiply(
            hash_to_G2(message),
            sk,
        ))


def PrivToPub(k: int) -> BLSPubkey:
    return G1_to_pubkey(multiply(G1, k))


def KeyGen(IKM: bytes) -> Tuple[BLSPubkey, int]:
    prk = hkdf_extract(b'BLS-SIG-KEYGEN-SALT-', IKM)
    l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa E741
    okm = hkdf_expand(prk, b'', l)
    sk = big_endian_to_int(okm) % curve_order
    pk = PrivToPub(sk)
    return (pk, sk)


def Verify(pk: BLSPubkey,
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


def Aggregate(*signatures: BLSSignature) -> BLSSignature:
    o = Z2
    for s in signatures:
        o = add(o, signature_to_G2(s))
    return G2_to_signature(o)


def AggregatePubkeys(*pks: BLSPubkey) -> BLSPubkey:
    o = Z1
    for p in pks:
        o = add(o, pubkey_to_G1(p))
    return G1_to_pubkey(o)


def AggregateVerify(*args: Union[Sequence[Tuple[BLSPubkey, bytes]], BLSSignature]) -> bool:
    signature = args[-1]
    assert isinstance(signature, bytes)
    pks, messages = list(zip(*args[:-1][0]))  # Unzip PKs and messages
    signature_point = signature_to_G2(signature)
    if not is_inf(multiply(signature_point, curve_order)):
        return False

    try:
        o = FQ12([1] + [0] * 11)
        for m_pubs in set(messages):
            # aggregate the pubs
            group_pub = Z1
            for i in range(len(messages)):
                if messages[i] == m_pubs:
                    group_pub = add(group_pub, pubkey_to_G1(pks[i]))

            o *= pairing(hash_to_G2(m_pubs), group_pub, final_exponentiate=False)
        o *= pairing(signature_point, neg(G1), final_exponentiate=False)

        final_exponentiation = final_exponentiate(o)
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def FastAggregateVerify(*args: Union[BLSPubkey, bytes, BLSSignature]) -> bool:
    pks = args[:-2]
    message, signature = args[-2:]
    assert(isinstance(pks, (list, tuple)))
    assert(all(isinstance(pk, bytes) for pk in pks))
    assert(isinstance(message, bytes))
    assert(isinstance(signature, bytes))
    aggregate_pubkey = AggregatePubkeys(*pks)
    return Verify(aggregate_pubkey, message, signature)
