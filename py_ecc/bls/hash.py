import math
import hashlib
import hmac
from typing import Union


def hkdf_extract(salt: Union[bytes, bytearray], ikm: Union[bytes, bytearray]) -> bytes:
    """
    HKDF-Extract

    https://tools.ietf.org/html/rfc5869
    """
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: Union[bytes, bytearray], info: Union[bytes, bytearray], length: int) -> bytes:
    """
    HKDF-Expand

    https://tools.ietf.org/html/rfc5869
    """
    n = math.ceil(length / 32)

    # okm = T(1) || T(2) || T(3) || ... || T(n)
    okm = bytearray(0)
    previous = bytearray(0)

    for i in range(0, n):
        # Concatenate (T(i) || info || i)
        text = previous + info + bytes([i + 1])

        # T(i + 1) = HMAC(T(i) || info || i)
        previous = bytearray(hmac.new(prk, text, hashlib.sha256).digest())
        okm.extend(previous)

    # Return first `length` bytes.
    return okm[:length]
