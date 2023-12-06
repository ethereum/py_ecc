import pytest

from py_ecc.bls import (
    G2MessageAugmentation,
)


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
    pub = G2MessageAugmentation.SkToPk(privkey)
    sig = G2MessageAugmentation.Sign(privkey, msg)
    assert G2MessageAugmentation.Verify(pub, msg, sig)


@pytest.mark.parametrize("SKs,messages", [(list(range(1, 11)), list(range(1, 11)))])
def test_aggregate_verify(SKs, messages):
    PKs = [G2MessageAugmentation.SkToPk(SK) for SK in SKs]
    messages = [bytes(msg) + PK for msg, PK in zip(messages, PKs)]
    signatures = [G2MessageAugmentation.Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = G2MessageAugmentation.Aggregate(signatures)
    assert G2MessageAugmentation.AggregateVerify(PKs, messages, aggregate_signature)
