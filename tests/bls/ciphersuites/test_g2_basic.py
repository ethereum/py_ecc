import pytest
from py_ecc.bls import G2Basic

@pytest.mark.parametrize(
    'SKs,messages,success',
    [
        (range(10), range(10), True),
        (range(3), (b'42', b'69', b'42'), False),  # Test duplicate messages fail
    ]
)
def test_aggregate_verify(SKs, messages, success):
    PKs = [G2Basic.PrivToPub(SK) for SK in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [G2Basic.Sign(SK, msg) for SK, msg in zip(SKs, messages)]
    aggregate_signature = G2Basic.Aggregate(signatures)
    assert G2Basic.AggregateVerify(zip(PKs, messages), aggregate_signature) == success
