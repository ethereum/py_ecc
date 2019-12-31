import pytest

from py_ecc.bls import G2ProofOfPossession
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
    pk = G2ProofOfPossession.PrivToPub(sk)
    proof = G2ProofOfPossession.PopProve(sk)
    assert G2ProofOfPossession.PopVerify(pk, proof)


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
    assert G2ProofOfPossession._AggregatePKs(signatures) == result_signature


@pytest.mark.parametrize(
    'SKs,message',
    [
        (range(5), b'11'*48),
    ]
)
def test_fast_aggregate_verify(SKs, message):
    PKs = [G2ProofOfPossession.PrivToPub(sk) for sk in SKs]
    signatures = [G2ProofOfPossession.Sign(sk, message) for sk in SKs]
    aggregate_signature = G2ProofOfPossession.Aggregate(signatures)
    assert G2ProofOfPossession.FastAggregateVerify(PKs, message, aggregate_signature)
