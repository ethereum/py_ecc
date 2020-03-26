import pytest

from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    multiply,
)
from py_ecc.bls.g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
)
from py_ecc.bls import G2Basic

# Tests taken from EIP 2333 https://eips.ethereum.org/EIPS/eip-2333
@pytest.mark.parametrize(
    'ikm,result_sk',
    [
        (bytes.fromhex('c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04'), 12513733877922233913083619867448865075222526338446857121953625441395088009793),
        (bytes.fromhex('3141592653589793238462643383279502884197169399375105820974944592'), 46029459550803682895343812821003080589696405386150182061394330539196052371668),
        (bytes.fromhex('0099FF991111002299DD7744EE3355BBDD8844115566CC55663355668888CC00'), 45379166311535261329029945990467475187325618028073620882733843918126031931161),
        (bytes.fromhex('d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3'), 31740500954810567003972734830331791822878290325762596213711963944729383643688),
    ]
)
def test_key_gen(ikm, result_sk):
    _, sk = G2Basic.KeyGen(ikm)
    assert sk == result_sk


@pytest.mark.parametrize(
    'pubkey,success',
    [
        (G2Basic.SkToPk(42), True),
        (b'11' * 48, False),
    ]
)
def test_key_validate(pubkey, success):
    assert G2Basic.KeyValidate(pubkey) == success


@pytest.mark.parametrize(
    'privkey',
    [
        (1),
        (5),
        (124),
        (735),
        (127409812145),
        (90768492698215092512159),
        (0),
    ]
)
def test_sign_verify(privkey):
    msg = str(privkey).encode('utf-8')
    pub = G2Basic.SkToPk(privkey)
    sig = G2Basic._CoreSign(privkey, msg, G2Basic.DST)
    assert G2Basic._CoreVerify(pub, msg, sig, G2Basic.DST)


@pytest.mark.parametrize(
    'signature_points,result_point',
    [
        ([multiply(G2, 2), multiply(G2, 3)], multiply(G2, 2 + 3)),
        ([multiply(G2, 42), multiply(G2, 69)], multiply(G2, 42 + 69)),
    ]
)
def test_aggregate(signature_points, result_point):
    signatures = [G2_to_signature(pt) for pt in signature_points]
    result_signature = G2_to_signature(result_point)
    assert G2Basic.Aggregate(signatures) == result_signature



@pytest.mark.parametrize(
    'SKs,messages',
    [
        (range(5), range(5)),
    ]
)
def test_core_aggregate_verify(SKs, messages):
    PKs = [G2Basic.SkToPk(sk) for sk in SKs]
    messages = [bytes(msg) for msg in messages]
    signatures = [G2Basic._CoreSign(sk, msg, G2Basic.DST) for sk, msg in zip(SKs, messages)]
    aggregate_signature = G2Basic.Aggregate(signatures)
    assert G2Basic._CoreAggregateVerify(zip(PKs, messages), aggregate_signature, G2Basic.DST)
