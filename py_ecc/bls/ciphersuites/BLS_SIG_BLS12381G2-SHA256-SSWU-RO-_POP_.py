from typing import (
    Union,
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

DST = b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    return CoreSign(SK, message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, message, signature, DST)


def AggregateVerify(*args: Union[Tuple[BLSSignature, bytes], BLSSignature]) -> bool:
    signature = args[-1]
    pks, messages = list(zip(*args[:-1][0]))  # Unzip PKs and messages
    return CoreAggregateVerify(pks, messages, signature, DST)


def PopProve(SK: int) -> BLSSignature:
    pubkey = PrivToPub(SK)
    return CoreSign(SK, pubkey, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')


def PopVerify(PK: BLSPubkey, proof: BLSSignature) -> bool:
    return CoreVerify(PK, PK, proof, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')


def FastAggregateVerify(*args: Union[BLSPubkey, bytes, BLSSignature]) -> bool:
    pks = args[:-2]
    message, signature = args[-2:]
    aggregate_pubkey = AggregatePKs(*pks)
    return Verify(aggregate_pubkey, message, signature)
