import hmac
import math
from typing import (
    Callable,
    Union,
)
from hashlib import sha256

from .constants import (
    ALL_BYTES,
    HASH_TO_FIELD_B_IN_BYTES,
    HASH_TO_FIELD_R_IN_BYTES,
)


def hkdf_extract(salt: Union[bytes, bytearray], ikm: Union[bytes, bytearray]) -> bytes:
    """
    HKDF-Extract

    https://tools.ietf.org/html/rfc5869
    """
    return hmac.new(salt, ikm, sha256).digest()


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
        previous = bytearray(hmac.new(prk, text, sha256).digest())
        okm.extend(previous)

    # Return first `length` bytes.
    return okm[:length]


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(_a ^ _b for _a, _b in zip(a, b))


def expand_message_xmd(msg: bytes, DST: bytes, len_in_bytes: int,
                       hash_function: Callable[[bytes], bytes]) -> bytes:
    ell = math.ceil(len_in_bytes / HASH_TO_FIELD_B_IN_BYTES)
    DST_prime = ALL_BYTES[len(DST)] + DST  # Prepend the length if the DST as a single byte
    Z_pad = b'\x00' * HASH_TO_FIELD_R_IN_BYTES
    l_i_b_str = len_in_bytes.to_bytes(2, 'big')
    b_0 = hash_function(Z_pad + msg + l_i_b_str + b'\x00' + DST_prime)
    b = [hash_function(b_0 + b'\x01' + DST_prime)]
    for i in range(2, ell + 1):
        b.append(hash_function(xor(b_0, b[i - 2]) + ALL_BYTES[i] + DST_prime))
    pseudo_random_bytes = b''.join(b)
    return pseudo_random_bytes[:len_in_bytes]
