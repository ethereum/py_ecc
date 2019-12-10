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

DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_AUG_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    PK = PrivToPub(SK)
    return CoreSign(SK, PK + message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, PK + message, signature, DST)


def AggregateVerify(*args: Union[Tuple[BLSSignature, bytes], BLSSignature]) -> bool:
    signature = args[-1]
    pks, _ = list(zip(*args[:-1][0]))  # Unzip PKs and messages
    messages = list([pk + msg for pk, msg in args[:-1]]) 
    return CoreAggregateVerify(pks, messages, signature, DST)
