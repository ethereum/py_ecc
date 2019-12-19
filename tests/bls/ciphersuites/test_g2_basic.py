import pytest

from py_ecc.bls.ciphersuites.BLS_SIG_BLS12381G2_SHA256_SSWU_RO__NUL_ import (
    PrivToPub,
    Sign,
    Aggregate,
    AggregateVerify,
)


@pytest.mark.parametrize(
    'SKs,messages,success',
    [
        (range(10), range(10), True),
        (range(3), (b'42', b'69', b'42'), False),  # Test duplicate messages fail
    ]
)
def test_aggregate_verify(SKs, messages, success):
    PKs = [PrivToPub(SK) for SK in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = Aggregate(signatures)
    assert AggregateVerify(zip(PKs, messages), aggregate_signature) == success
