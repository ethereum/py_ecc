import pytest

from py_ecc.bls import (
    G2Basic,
)
from py_ecc.bls.g2_primitives import (
    G2_to_signature,
)
from py_ecc.optimized_bls12_381 import (
    G2,
    multiply,
)


@pytest.mark.parametrize(
    "pubkey,success",
    [
        (G2Basic.SkToPk(42), True),
        (b"\x11" * 48, False),
    ],
)
def test_key_validate(pubkey, success):
    assert G2Basic.KeyValidate(pubkey) == success


@pytest.mark.parametrize(
    "privkey",
    [
        (1),
        (5),
        (124),
        (735),
        (127409812145),
        (90768492698215092512159),
    ],
)
def test_sign_verify(privkey):
    msg = str(privkey).encode("utf-8")
    pub = G2Basic.SkToPk(privkey)
    sig = G2Basic._CoreSign(privkey, msg, G2Basic.DST)
    assert G2Basic._CoreVerify(pub, msg, sig, G2Basic.DST)


@pytest.mark.parametrize(
    "signature_points,result_point",
    [
        ([multiply(G2, 2), multiply(G2, 3)], multiply(G2, 2 + 3)),
        ([multiply(G2, 42), multiply(G2, 69)], multiply(G2, 42 + 69)),
    ],
)
def test_aggregate(signature_points, result_point):
    signatures = [G2_to_signature(pt) for pt in signature_points]
    result_signature = G2_to_signature(result_point)
    assert G2Basic.Aggregate(signatures) == result_signature


@pytest.mark.parametrize(
    "SKs,messages",
    [
        (list(range(1, 6)), list(range(1, 6))),
    ],
)
def test_core_aggregate_verify(SKs, messages):
    PKs = [G2Basic.SkToPk(sk) for sk in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [
        G2Basic._CoreSign(sk, msg, G2Basic.DST) for sk, msg in zip(SKs, messages)
    ]
    aggregate_signature = G2Basic.Aggregate(signatures)
    assert G2Basic._CoreAggregateVerify(PKs, messages, aggregate_signature, G2Basic.DST)
