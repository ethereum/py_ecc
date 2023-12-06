import pytest

from py_ecc.bls.constants import (
    POW_2_381,
    POW_2_382,
    POW_2_383,
    POW_2_384,
)
from py_ecc.bls.point_compression import (
    compress_G1,
    compress_G2,
    decompress_G1,
    decompress_G2,
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
    field_modulus as q,
    is_on_curve,
    multiply,
    normalize,
)


@pytest.mark.parametrize(
    "pt,on_curve,is_infinity",
    [
        # On curve points
        (G1, True, False),
        (multiply(G1, 5), True, False),
        # Infinity point but still on curve
        (Z1, True, True),
        # Not on curve
        ((FQ(5566), FQ(5566), FQ.one()), False, None),
    ],
)
def test_G1_compress_and_decompress_flags(pt, on_curve, is_infinity):
    assert on_curve == is_on_curve(pt, b)
    z = compress_G1(pt)
    if on_curve:
        x = z % POW_2_381
        c_flag = (z % POW_2_384) // POW_2_383
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
        assert normalize(decompress_G1(z)) == normalize(pt)
    else:
        with pytest.raises(ValueError):
            decompress_G1(z)


compressed_g1 = compress_G1(G1)
compressed_z1 = compress_G1(Z1)


@pytest.mark.parametrize(
    "z, error_message",
    [
        (compressed_g1, None),  # baseline
        (compressed_g1 & ~(1 << 383), "c_flag should be 1"),  # set c_flag to 0
        (compressed_g1 | (1 << 382), "b_flag should be 0"),  # set b_flag to 1
        (compressed_z1 & ~(1 << 382), "b_flag should be 1"),  # set b_flag to 0
        (
            compressed_z1 | (1 << 381),
            "a point at infinity should have a_flag == 0",
        ),  # set a_flag to 1
        (
            q | (1 << 383),
            "Point value should be less than field modulus.",
        ),  # field modulus and c_flag
    ],
)
def test_decompress_G1_edge_case(z, error_message):
    if error_message is None:
        decompress_G1(z)
    else:
        with pytest.raises(ValueError, match=error_message):
            decompress_G1(z)


@pytest.mark.parametrize(
    "pt,on_curve,is_infinity",
    [
        # On curve points
        (G2, True, False),
        (multiply(G2, 5), True, False),
        # Infinity point but still on curve
        (Z2, True, True),
        # Not on curve
        ((FQ2([5566, 5566]), FQ2([5566, 5566]), FQ2.one()), False, None),
    ],
)
def test_G2_compress_and_decompress_flags(pt, on_curve, is_infinity):
    if on_curve:
        z1, z2 = compress_G2(pt)
        x1 = z1 % POW_2_381
        c_flag1 = (z1 % POW_2_384) // POW_2_383
        b_flag1 = (z1 % POW_2_383) // POW_2_382
        a_flag1 = (z1 % POW_2_382) // POW_2_381
        x2 = z2 % POW_2_381
        c_flag2 = (z2 % POW_2_384) // POW_2_383
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
        assert normalize(decompress_G2((z1, z2))) == normalize(pt)
    else:
        with pytest.raises(ValueError):
            compress_G2(pt)


compressed_g2 = compress_G2(G2)
compressed_z2 = compress_G2(Z2)


@pytest.mark.parametrize(
    "z, error_message",
    [
        (compressed_g2, None),  # baseline
        (
            (compressed_g2[0] & ~(1 << 383), compressed_g2[1]),
            "c_flag should be 1",
        ),  # set c_flag1 to 0
        (
            (compressed_g2[0] | (1 << 382), compressed_g2[1]),
            "b_flag should be 0",
        ),  # set b_flag1 to 1
        (
            (compressed_z2[0] & ~(1 << 382), compressed_z2[1]),
            "b_flag should be 1",
        ),  # set b_flag1 to 0
        (
            (q | (1 << 383), compressed_z2[1]),
            "x1 value should be less than field modulus.",
        ),  # x1 == q
        (
            (compressed_z2[0] | (1 << 381), compressed_z2[1]),
            "a point at infinity should have a_flag == 0",
        ),  # set a_flag1 to 1
        (
            (compressed_g2[0], compressed_z2[1] | (1 << 383)),
            "z2 point value should be less than field modulus.",
        ),  # set c_flag2 to 1
        (
            (compressed_g2[0], compressed_z2[1] | (1 << 382)),
            "z2 point value should be less than field modulus.",
        ),  # set b_flag2 to 1
        (
            (compressed_g2[0], compressed_z2[1] | (1 << 381)),
            "z2 point value should be less than field modulus.",
        ),  # set a_flag2 to 1
        (
            (compressed_g2[0], compressed_g2[1] + q),
            "z2 point value should be less than field modulus.",
        ),  # z2 value >= field modulus
    ],
)
def test_decompress_G2_edge_case(z, error_message):
    if error_message is None:
        decompress_G2(z)
    else:
        with pytest.raises(ValueError, match=error_message):
            decompress_G2(z)
