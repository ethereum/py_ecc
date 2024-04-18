import pytest

from py_ecc.utils import (
    prime_field_inv,
)


@pytest.mark.parametrize(
    "a,n,result",
    [
        (0, 7, 0),
        (7, 7, 0),
        (2, 7, 4),
        (10, 7, 5),
    ],
)
def test_prime_field_inv(a, n, result):
    assert prime_field_inv(a, n) % n == result
