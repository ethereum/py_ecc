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
    CoreAggregateVerify,
    CoreSign,
    CoreVerify,
    KeyGen,
    PrivToPub,
)

DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_AUG_'
ID = 'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_AUG_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    PK = PrivToPub(SK)
    return CoreSign(SK, PK + message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, PK + message, signature, DST)


def AggregateVerify(pairs: Iterable[Tuple[BLSPubkey, bytes]], signature: BLSSignature) -> bool:
    pairs = list(pairs)
    pairs = [(pk, pk + msg) for pk, msg in pairs]
    return CoreAggregateVerify(pairs, signature, DST)
