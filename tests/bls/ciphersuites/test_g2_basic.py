import pytest

from eth_utils import (
    ValidationError,
)

from py_ecc.bls import G2Basic
from py_ecc.bls.ciphersuites import (
    Z1_PUBKEY,
    Z2_SIGNATURE,
)


@pytest.mark.parametrize(
    'SKs,messages,result',
    [
        (list(range(1, 11)), list(range(1, 11)), True),
        (list(range(1, 4)), (b'42', b'69', b'42'), False),  # Test duplicate messages fail
    ]
)
def test_aggregate_verify(SKs, messages, result):
    PKs = [G2Basic.SkToPk(SK) for SK in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [G2Basic.Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = G2Basic.Aggregate(signatures)
    assert G2Basic.AggregateVerify(PKs, messages, aggregate_signature) == result


@pytest.mark.parametrize(
    'privkey, success',
    [
        (1, True),
        (0, False),
        ('hello', False),  # wrong type
    ]
)
def test_sk_to_pk(privkey, success):
    if success:
        G2Basic.SkToPk(privkey)
    else:
        with pytest.raises(ValidationError):
            G2Basic.SkToPk(privkey)


@pytest.mark.parametrize(
    'privkey, message, success',
    [
        (1, b'message', True),
        (0, b'message', False),
        ('hello', b'message', False),  # wrong type privkey
        (1, 123, False),  # wrong type message
    ]
)
def test_sign(privkey, message, success):
    if success:
        G2Basic.Sign(privkey, message)
    else:
        with pytest.raises(ValidationError):
            G2Basic.Sign(privkey, message)



@pytest.mark.parametrize(
    'signatures, success',
    [
        ([G2Basic.Sign(1, b'helloworld')], True),
        ([G2Basic.Sign(1, b'helloworld'), G2Basic.Sign(2, b'helloworld')], True),
        ([Z2_SIGNATURE], True),
        (['hello'], False),
        ([], False),
    ]
)
def test_aggregate(signatures, success):
    if success:
        G2Basic.Aggregate(signatures)
    else:
        with pytest.raises(ValidationError):
            G2Basic.Aggregate(signatures)
