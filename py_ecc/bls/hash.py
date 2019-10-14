import hashlib
import hmac
from typing import ByteString

from eth_typing import Hash32

from .constants import HASH_LENGTH_BYTES


def hash_eth2(data: ByteString) -> Hash32:
    """
    Return SHA-256 hashed result.

    Note: this API is currently under active research/development so is subject to change
    without a major version bump.

    Note: it's a placeholder and we aim to migrate to a S[T/N]ARK-friendly hash function in
    a future Ethereum 2.0 deployment phase.
    """
    return Hash32(hashlib.sha256(data).digest())


def hkdf_extract(salt: ByteString, ikm: ByteString) -> bytes:
    """
    HKDF-Expand

    https://tools.ietf.org/html/rfc5869
    """
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: ByteString, info: ByteString, length: int) -> bytes:
    """
    HKDF-Expand

    https://tools.ietf.org/html/rfc5869
    """
    # n = cieling(length / HASH_LENGTH_BYTES)
    n = length // HASH_LENGTH_BYTES
    if n * HASH_LENGTH_BYTES < length:
        n += 1

    # okm = T(1) || T(2) || T(3) || ... || T(n)
    okm = bytearray(0)
    previous = bytearray(0)

    for i in range(0, n):
        # Concatenate (T(i) || info || i)
        text = previous + info + bytes([i + 1])

        # T(i + 1) = HMAC(T(i) || info || i)
        previous = hmac.new(prk, text, hashlib.sha256).digest()
        okm.extend(previous)

    # Return first `length` bytes.
    return okm[:length]
