import pytest

from py_ecc.bls.ciphersuites.BLS_SIG_BLS12381G2_SHA256_SSWU_RO__AUG_ import (
    PrivToPub,
    Sign,
    Aggregate,
    AggregateVerify,
)


@pytest.mark.parametrize(
    'SKs,messages',
    [
        (range(10), range(10)),
    ]
)
def test_aggregate_verify(SKs, messages):
    PKs = [PrivToPub(SK) for SK in SKs]
    messages = [bytes(msg) + PK for msg, PK in zip(messages, PKs)]
    signatures = [Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = Aggregate(signatures)
    assert AggregateVerify(zip(PKs, messages), aggregate_signature)
