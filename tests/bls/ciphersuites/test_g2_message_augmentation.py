import pytest

from eth_utils import (
    ValidationError,
)

from py_ecc.bls import (
    G2MessageAugmentation,
)
from py_ecc.bls.g2_primitives import (
    G1_to_pubkey,
    G2_to_signature,
)
from py_ecc.optimized_bls12_381 import (
    Z1,
    Z2,
)

Z1_PUBKEY = G1_to_pubkey(Z1)
Z2_SIGNATURE = G2_to_signature(Z2)
SAMPLE_MESSAGE = b"helloworld"


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


@pytest.mark.parametrize(
    "pubkey, message, signature, result",
    [
        (
            G2MessageAugmentation.SkToPk(1),
            SAMPLE_MESSAGE,
            G2MessageAugmentation.Sign(1, SAMPLE_MESSAGE),
            True,
        ),
        (
            G2MessageAugmentation.SkToPk(2),
            SAMPLE_MESSAGE,
            G2MessageAugmentation.Sign(1, SAMPLE_MESSAGE),
            False,
        ),
        (G2MessageAugmentation.SkToPk(1), SAMPLE_MESSAGE, Z2_SIGNATURE, False),
        (
            Z1_PUBKEY,
            SAMPLE_MESSAGE,
            G2MessageAugmentation.Sign(1, SAMPLE_MESSAGE),
            False,
        ),
        # identity pubkey and identity signature must not verify (#74)
        (Z1_PUBKEY, SAMPLE_MESSAGE, Z2_SIGNATURE, False),
    ],
)
def test_verify(pubkey, message, signature, result):
    assert G2MessageAugmentation.Verify(pubkey, message, signature) == result


def test_aggregate_empty():
    # empty aggregation is rejected (#65)
    with pytest.raises(ValidationError):
        G2MessageAugmentation.Aggregate([])
    assert not G2MessageAugmentation.AggregateVerify([], [], Z2_SIGNATURE)
