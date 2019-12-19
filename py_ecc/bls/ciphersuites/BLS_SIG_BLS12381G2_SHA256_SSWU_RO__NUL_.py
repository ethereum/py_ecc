from typing import (
    Iterable,
    Tuple,
)
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)

from py_ecc.bls.g2_core import (
    Aggregate,
    AggregatePKs,
    CoreAggregateVerify,
    CoreSign,
    CoreVerify,
    KeyGen,
    PrivToPub,
)

DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_NUL_'
ID = 'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_NUL_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    return CoreSign(SK, message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, message, signature, DST)


def AggregateVerify(pairs: Iterable[Tuple[BLSPubkey, bytes]], signature: BLSSignature) -> bool:
    pairs = list(pairs)
    _, messages = zip(*pairs)
    if len(messages) != len(set(messages)):  # Messages are not unique
        return False
    return CoreAggregateVerify(pairs, signature, DST)
