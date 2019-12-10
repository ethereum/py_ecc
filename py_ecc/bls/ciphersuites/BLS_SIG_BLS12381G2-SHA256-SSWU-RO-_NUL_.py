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

DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_NUL_'


def Sign(SK: int, message: bytes) -> BLSSignature:
    return CoreSign(SK, message, DST)


def Verify(PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
    return CoreVerify(PK, message, signature, DST)


def AggregateVerify(*args: Union[Tuple[BLSSignature, bytes], BLSSignature]) -> bool:
    signature = args[-1]
    pks, messages = list(zip(*args[:-1][0]))  # Unzip PKs and messages
    if len(messages) != len(set(messages)):  # Messages are not unique
        return False
    return CoreAggregateVerify(pks, messages, signature, DST)
