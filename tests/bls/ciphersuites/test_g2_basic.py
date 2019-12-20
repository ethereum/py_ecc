import pytest

from py_ecc.bls import G2Basic

bls = G2Basic()

@pytest.mark.parametrize(
    'SKs,messages,success',
    [
        (range(10), range(10), True),
        (range(3), (b'42', b'69', b'42'), False),  # Test duplicate messages fail
    ]
)
def test_aggregate_verify(SKs, messages, success):
    PKs = [bls.PrivToPub(SK) for SK in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [bls.Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = bls.Aggregate(signatures)
    assert bls.AggregateVerify(zip(PKs, messages), aggregate_signature) == success
