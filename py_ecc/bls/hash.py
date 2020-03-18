import hmac
import math
from typing import Union
from hashlib import sha256 as _sha256

from .constants import (
    HASH_TO_FIELD_B_IN_BYTES,
    HASH_TO_FIELD_R_IN_BYTES,
)


def hkdf_extract(salt: Union[bytes, bytearray], ikm: Union[bytes, bytearray]) -> bytes:
    """
    HKDF-Extract

    https://tools.ietf.org/html/rfc5869
    """
    return hmac.new(salt, ikm, _sha256).digest()


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
        previous = bytearray(hmac.new(prk, text, _sha256).digest())
        okm.extend(previous)

    # Return first `length` bytes.
    return okm[:length]


def sha256(x: bytes) -> bytes:
    m = _sha256()
    m.update(x)
    return m.digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(_a ^ _b for _a, _b in zip(a, b))


def expand_message_xmd(msg: bytes, DST: bytes, len_in_bytes: int) -> bytes:
    ell = math.ceil(len_in_bytes / HASH_TO_FIELD_B_IN_BYTES)
    DST_prime = len(DST).to_bytes(1, 'big') + DST
    Z_pad = b'\x00' * HASH_TO_FIELD_R_IN_BYTES
    l_i_b_str = len_in_bytes.to_bytes(2, 'big')
    b_0 = sha256(Z_pad + msg + l_i_b_str + b'\x00' + DST_prime)
    b = [sha256(b_0 + b'\x01' + DST_prime)]
    for i in range(2, ell + 1):
        b.append(sha256(xor(b_0, b[i - 2]) + i.to_bytes(1, 'big') + DST_prime))
    pseudo_random_bytes = b''.join(b)
    return pseudo_random_bytes[:len_in_bytes]
