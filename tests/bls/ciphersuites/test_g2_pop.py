import pytest

from py_ecc.bls import G2PoP
from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    multiply,
)
from py_ecc.bls.g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
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
    pk = G2PoP.PrivToPub(sk)
    proof = G2PoP.PopProve(sk)
    assert G2PoP.PopVerify(pk, proof)


@pytest.mark.parametrize(
    'signature_points,result_point',
    [
        ([multiply(G1, 2), multiply(G1, 3)], multiply(G1, 2 + 3)),
        ([multiply(G1, 42), multiply(G1, 69)], multiply(G1, 42 + 69)),
    ]
)
def test_aggregate_pks(signature_points, result_point):
    signatures = [G1_to_pubkey(pt) for pt in signature_points]
    result_signature = G1_to_pubkey(result_point)
    assert G2PoP._AggregatePKs(signatures) == result_signature


@pytest.mark.parametrize(
    'SKs,message',
    [
        (range(5), b'11'*48),
    ]
)
def test_fast_aggregate_verify(SKs, message):
    PKs = [G2PoP.PrivToPub(sk) for sk in SKs]
    signatures = [G2PoP.Sign(sk, message) for sk in SKs]
    aggregate_signature = G2PoP.Aggregate(signatures)
    assert G2PoP.FastAggregateVerify(PKs, message, aggregate_signature)
