import hashlib
from typing import Union

from eth_typing import Hash32


def hash_eth2(data: Union[bytes, bytearray]) -> Hash32:
    """
    Return SHA-256 hashed result.

    Note: this API is currently under active research/development so is subject to change
    without a major version bump.

    Note: it's a placeholder and we aim to migrate to a S[T/N]ARK-friendly hash function in
    a future Ethereum 2.0 deployment phase.
    """
    return Hash32(hashlib.sha256(data).digest())
