import pytest

from py_ecc.bls.ciphersuites.BLS_SIG_BLS12381G2_SHA256_SSWU_RO__POP_ import (
    PrivToPub,
    Sign,
    Aggregate,
    PopProve,
    PopVerify,
    FastAggregateVerify,
)


@pytest.mark.parametrize(
    'sk',
    [
        42,
        69,
        31415926,
    ]
)
def test_pop(sk):
    pk = PrivToPub(sk)
    proof = PopProve(sk)
    assert PopVerify(pk, proof)


@pytest.mark.parametrize(
    'SKs,message',
    [
        (range(5), b'11'*48),
    ]
)
def test_fast_aggregate_verify(SKs, message):
    PKs = [PrivToPub(sk) for sk in SKs]
    signatures = [Sign(sk, message) for sk in SKs]
    aggregate_signature = Aggregate(signatures)
    assert FastAggregateVerify(PKs, message, aggregate_signature)
