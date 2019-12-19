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

DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP_'
ID = 'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    return CoreSign(SK, message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, message, signature, DST)


def AggregateVerify(pairs: Iterable[Tuple[BLSPubkey, bytes]], signature: BLSSignature) -> bool:
    return CoreAggregateVerify(pairs, signature, DST)


def PopProve(SK: int) -> BLSSignature:
    pubkey = PrivToPub(SK)
    return CoreSign(SK, pubkey, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')


def PopVerify(PK: BLSPubkey, proof: BLSSignature) -> bool:
    return CoreVerify(PK, PK, proof, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')


def FastAggregateVerify(PKs: Iterable[BLSPubkey], message: bytes, signature: BLSSignature) -> bool:
    aggregate_pubkey = AggregatePKs(PKs)
    return Verify(aggregate_pubkey, message, signature)
