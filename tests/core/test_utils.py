import pytest

from py_ecc.utils import (
    is_integer,
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


def test_rejects_booleans():
    # booleans must be rejected even though bool is a subclass of int
    assert not is_integer(True)
    assert not is_integer(False)
    # plain integers must be accepted
    assert is_integer(0)
    assert is_integer(42)
    assert is_integer(-1)
    # non-integers must be rejected
    assert not is_integer(1.0)
    assert not is_integer("1")
    assert not is_integer(None)
