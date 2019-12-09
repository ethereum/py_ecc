from eth_utils import (
    big_endian_to_int,
)
import pytest

from py_ecc.bls import (
    AggregatePubkeys,
    AggregateSignatures,
    PrivToPub,
    KeyGen,
    Sign,
    Verify,
    AggregateVerify,
    FastAggregateVerify,
)
from py_ecc.bls.utils import (
    compress_G1,
    compress_G2,
    decompress_G1,
    decompress_G2,
    hash_to_G2,
    signature_to_G2,
)
from py_ecc.bls.constants import (
    POW_2_381,
    POW_2_382,
    POW_2_383,
)
from py_ecc.fields import (
    optimized_bls12_381_FQ as FQ,
    optimized_bls12_381_FQ2 as FQ2,
)
from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    Z1,
    Z2,
    b,
    b2,
    is_on_curve,
    multiply,
    normalize,
    field_modulus as q,
)


def test_hash_to_G2():
    message_hash = b'\x12' * 32

    result_1 = hash_to_G2(message_hash)
    assert is_on_curve(result_1, b2)


def test_decompress_G2_with_no_modular_square_root_found():
    with pytest.raises(ValueError, match="Failed to find a modular squareroot"):
        signature_to_G2(b'\x11' * 96)


@pytest.mark.parametrize(
    'pt,on_curve,is_infinity',
    [
        # On curve points
        (G1, True, False),
        (multiply(G1, 5), True, False),
        # Infinity point but still on curve
        (Z1, True, True),
        # Not on curve
        ((FQ(5566), FQ(5566), FQ.one()), False, None),
    ]
)
def test_G1_compress_and_decompress_flags(pt, on_curve, is_infinity):
    assert on_curve == is_on_curve(pt, b)
    z = compress_G1(pt)
    if on_curve:
        x = z % POW_2_381
        c_flag = (z % 2**384) // POW_2_383
        b_flag = (z % POW_2_383) // POW_2_382
        a_flag = (z % POW_2_382) // POW_2_381
        assert x < q
        assert c_flag == 1
        if is_infinity:
            assert b_flag == 1
            assert a_flag == x == 0
        else:
            assert b_flag == 0
            pt_x, pt_y = normalize(pt)
            assert a_flag == (pt_y.n * 2) // q
            assert x == pt_x.n
        # Correct flags should decompress correct x, y
        normalize(decompress_G1(z)) == normalize(pt)
    else:
        with pytest.raises(ValueError):
            decompress_G1(z)


@pytest.mark.parametrize(
    'pt,on_curve,is_infinity',
    [
        # On curve points
        (G2, True, False),
        (multiply(G2, 5), True, False),
        # Infinity point but still on curve
        (Z2, True, True),
        # Not on curve
        ((FQ2([5566, 5566]), FQ2([5566, 5566]), FQ2.one()), False, None),
    ]
)
def test_G2_compress_and_decompress_flags(pt, on_curve, is_infinity):
    if on_curve:
        z1, z2 = compress_G2(pt)
        x1 = z1 % POW_2_381
        c_flag1 = (z1 % 2**384) // POW_2_383
        b_flag1 = (z1 % POW_2_383) // POW_2_382
        a_flag1 = (z1 % POW_2_382) // POW_2_381
        x2 = z2 % POW_2_381
        c_flag2 = (z2 % 2**384) // POW_2_383
        b_flag2 = (z2 % POW_2_383) // POW_2_382
        a_flag2 = (z2 % POW_2_382) // POW_2_381
        assert x1 < q
        assert x2 < q
        assert c_flag2 == b_flag2 == a_flag2 == 0
        assert c_flag1 == 1
        if is_infinity:
            assert b_flag1 == 1
            assert a_flag1 == x1 == x2 == 0
        else:
            assert b_flag1 == 0
            _, y = normalize(pt)
            _, y_im = y.coeffs
            # TODO: need a case for y_im == 0
            assert a_flag1 == (y_im * 2) // q
        # Correct flags should decompress correct x, y
        normalize(decompress_G2((z1, z2))) == normalize(pt)
    else:
        with pytest.raises(ValueError):
            compress_G2(pt)


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
def test_bls_core(privkey):
    p1 = multiply(G1, privkey)
    p2 = multiply(G2, privkey)
    msg = str(privkey).encode('utf-8')
    msghash = hash_to_G2(msg)

    assert normalize(decompress_G1(compress_G1(p1))) == normalize(p1)
    assert normalize(decompress_G2(compress_G2(p2))) == normalize(p2)
    assert normalize(decompress_G2(compress_G2(msghash))) == normalize(msghash)
    sig = Sign(privkey, msg)
    pub = PrivToPub(privkey)
    assert Verify(pub, msg, sig)


@pytest.mark.parametrize(
    'msg, privkeys',
    [
        (b'\x12' * 32, [1, 5, 124, 735, 127409812145, 90768492698215092512159, 0]),
        (b'\x34' * 32, [42, 666, 1274099945, 4389392949595]),
    ]
)
def test_signature_aggregation(msg, privkeys):
    sigs = [Sign(k, msg) for k in privkeys]
    pubs = [PrivToPub(k) for k in privkeys]
    aggsig = AggregateSignatures(sigs)
    aggpub = AggregatePubkeys(pubs)
    assert Verify(aggpub, msg, aggsig)


@pytest.mark.parametrize(
    'msg_1, msg_2',
    [
        (b'\x12' * 32, b'\x34' * 32)
    ]
)
@pytest.mark.parametrize(
    'privkeys_1, privkeys_2',
    [
        (tuple(range(10)), tuple(range(10))),
        ((0, 1, 2, 3), (4, 5, 6, 7)),
        ((0, 1, 2, 3), (2, 3, 4, 5)),
    ]
)
def test_multi_aggregation(msg_1, msg_2, privkeys_1, privkeys_2):
    sigs_1 = [Sign(k, msg_1) for k in privkeys_1]
    pubs_1 = [PrivToPub(k) for k in privkeys_1]
    aggsig_1 = AggregateSignatures(sigs_1)
    aggpub_1 = AggregatePubkeys(pubs_1)

    sigs_2 = [Sign(k, msg_2) for k in privkeys_2]
    pubs_2 = [PrivToPub(k) for k in privkeys_2]
    aggsig_2 = AggregateSignatures(sigs_2)
    aggpub_2 = AggregatePubkeys(pubs_2)

    messages = [msg_1, msg_2]
    pubs = [aggpub_1, aggpub_2]
    aggsig = AggregateSignatures([aggsig_1, aggsig_2])

    assert AggregateVerify(
        pks=pubs,
        messages=messages,
        signature=aggsig,
    )


@pytest.mark.parametrize(
    'msg, privkeys',
    [
        (b'\x12' * 32, [1, 5, 124, 735, 127409812145, 90768492698215092512159, 0]),
        (b'\x34' * 32, [42, 666, 1274099945, 4389392949595]),
    ]
)
def test_fast_aggregate_verify(msg, privkeys):
    sigs = [Sign(sk, msg) for sk in privkeys]
    pubs = [PrivToPub(sk) for sk in privkeys]
    aggsig = AggregateSignatures(sigs)
    assert FastAggregateVerify(
        pks=pubs,
        message=msg,
        signature=aggsig,
    )


@pytest.mark.parametrize(
    # Tests taken from https://eips.ethereum.org/EIPS/eip-2333
    'ikm, privkey',
    [
        (bytes.fromhex('c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04') , 12513733877922233913083619867448865075222526338446857121953625441395088009793),
        (bytes.fromhex('0099FF991111002299DD7744EE3355BBDD8844115566CC55663355668888CC00'), 45379166311535261329029945990467475187325618028073620882733843918126031931161),
    ]
)
def test_key_gen(ikm, privkey):
    _, calc_privkey = KeyGen(ikm)
    assert calc_privkey == privkey
