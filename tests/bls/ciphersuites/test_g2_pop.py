import pytest

from py_ecc.bls import (
    G2ProofOfPossession,
)
from py_ecc.bls.g2_primitives import (
    G1_to_pubkey,
    G2_to_signature,
)
from py_ecc.optimized_bls12_381 import (
    G1,
    Z1,
    Z2,
    multiply,
)

sample_message = b"\x12" * 32

Z1_PUBKEY = G1_to_pubkey(Z1)
Z2_SIGNATURE = G2_to_signature(Z2)


def compute_aggregate_signature(SKs, message):
    PKs = [G2ProofOfPossession.SkToPk(sk) for sk in SKs]
    signatures = [G2ProofOfPossession.Sign(sk, message) for sk in SKs]
    aggregate_signature = G2ProofOfPossession.Aggregate(signatures)
    return (PKs, aggregate_signature)


@pytest.mark.parametrize(
    "sk",
    [
        42,
        69,
        31415926,
    ],
)
def test_pop(sk):
    pk = G2ProofOfPossession.SkToPk(sk)
    proof = G2ProofOfPossession.PopProve(sk)
    assert G2ProofOfPossession.PopVerify(pk, proof)


@pytest.mark.parametrize(
    "signature_points,result_point",
    [
        ([multiply(G1, 2), multiply(G1, 3)], multiply(G1, 2 + 3)),
        ([multiply(G1, 42), multiply(G1, 69)], multiply(G1, 42 + 69)),
    ],
)
def test_aggregate_pks(signature_points, result_point):
    signatures = [G1_to_pubkey(pt) for pt in signature_points]
    result_signature = G1_to_pubkey(result_point)
    assert G2ProofOfPossession._AggregatePKs(signatures) == result_signature


@pytest.mark.parametrize(
    "PK, message, signature, result",
    [
        (
            G2ProofOfPossession.SkToPk(1),
            sample_message,
            G2ProofOfPossession.Sign(1, sample_message),
            True,
        ),
        (None, sample_message, Z2_SIGNATURE, False),  # wrong type
        (Z1_PUBKEY, sample_message, Z2_SIGNATURE, False),
    ],
)
def test_verify(PK, message, signature, result):
    assert G2ProofOfPossession.Verify(PK, message, signature) == result


@pytest.mark.parametrize(
    "PKs, aggregate_signature, message, result",
    [
        (
            *compute_aggregate_signature(SKs=[1], message=sample_message),
            sample_message,
            True,
        ),
        (
            *compute_aggregate_signature(
                SKs=tuple(range(1, 5)), message=sample_message
            ),
            sample_message,
            True,
        ),
        ([], Z2_SIGNATURE, sample_message, False),
        (
            [G2ProofOfPossession.SkToPk(1), Z1_PUBKEY],
            G2ProofOfPossession.Sign(1, sample_message),
            sample_message,
            False,
        ),
    ],
)
def test_aggregate_verify(PKs, aggregate_signature, message, result):
    assert (
        G2ProofOfPossession.AggregateVerify(
            PKs, (message,) * len(PKs), aggregate_signature
        )
        == result
    )


@pytest.mark.parametrize(
    "PKs, aggregate_signature, message, result",
    [
        (
            *compute_aggregate_signature(SKs=[1], message=sample_message),
            sample_message,
            True,
        ),
        (
            *compute_aggregate_signature(
                SKs=tuple(range(1, 5)), message=sample_message
            ),
            sample_message,
            True,
        ),
        ([], Z2_SIGNATURE, sample_message, False),
        (
            [G2ProofOfPossession.SkToPk(1), Z1_PUBKEY],
            G2ProofOfPossession.Sign(1, sample_message),
            sample_message,
            False,
        ),
    ],
)
def test_fast_aggregate_verify(PKs, aggregate_signature, message, result):
    assert (
        G2ProofOfPossession.FastAggregateVerify(PKs, message, aggregate_signature)
        == result
    )
