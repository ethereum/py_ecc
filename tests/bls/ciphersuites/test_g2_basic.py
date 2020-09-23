import pytest
from py_ecc.bls import G2Basic

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
