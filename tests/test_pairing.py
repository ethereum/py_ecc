import pytest

from py_ecc.bls12_381_curve import (
    BLS12_381_Curve,
    Optimized_BLS12_381_Curve,
)
from py_ecc.bn128_curve import (
    BN128_Curve,
    Optimized_BN128_Curve,
)

from py_ecc.field_elements import (
    FQ,
    FQ2,
    FQ12,
)
from py_ecc.optimized_field_elements import (
    FQ as optimized_FQ,
    FQ2 as optimized_FQ2,
    FQ12 as optimized_FQ12,
)


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        BLS12_381_Curve(),
    ),
)
def test_linefunc_consistency_object_plain_curves(curve_obj):
    one, two, three = curve_obj.G1, curve_obj.double(curve_obj.G1), curve_obj.multiply(curve_obj.G1, 3)
    negone, negtwo, negthree = (
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 1),
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 2),
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 3),
    )

    assert curve_obj.linefunc(one, two, one) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, two) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, three) != FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, negthree) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, one) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, negone) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, two) != FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, one) == FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, two) != FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, negtwo) == FQ(0, curve_obj.curve_name)


@pytest.mark.parametrize(
    'curve_obj',
    (
        Optimized_BN128_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_linefunc_consistency_object_optimized_curves(curve_obj):
    one, two, three = curve_obj.G1, curve_obj.double(curve_obj.G1), curve_obj.multiply(curve_obj.G1, 3)
    negone, negtwo, negthree = (
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 1),
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 2),
        curve_obj.multiply(curve_obj.G1, curve_obj.curve_order - 3),
    )

    assert curve_obj.linefunc(one, two, one)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, two)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, three)[0] != optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, two, negthree)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, one)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, negone)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, negone, two)[0] != optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, one)[0] == optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, two)[0] != optimized_FQ(0, curve_obj.curve_name)
    assert curve_obj.linefunc(one, one, negtwo)[0] == optimized_FQ(0, curve_obj.curve_name)


@pytest.mark.parametrize(
    'curve_obj,FQ12',
    (
        (BN128_Curve(), FQ12),
        (Optimized_BN128_Curve(), optimized_FQ12),
        (BLS12_381_Curve(), FQ12),
        (Optimized_BLS12_381_Curve(), optimized_FQ12),
    ),
)
def test_pairing_negative_G1(curve_obj, FQ12):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)
    pn1 = curve_obj.pairing(curve_obj.G2, curve_obj.neg(curve_obj.G1))

    assert p1 * pn1 == FQ12.one(curve_obj.curve_name)


@pytest.mark.parametrize(
    'curve_obj,FQ12',
    (
        (BN128_Curve(), FQ12),
        (Optimized_BN128_Curve(), optimized_FQ12),
        (BLS12_381_Curve(), FQ12),
        (Optimized_BLS12_381_Curve(), optimized_FQ12),
    ),
)
def test_pairing_negative_G2(curve_obj, FQ12):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)
    pn1 = curve_obj.pairing(curve_obj.G2, curve_obj.neg(curve_obj.G1))
    np1 = curve_obj.pairing(curve_obj.neg(curve_obj.G2), curve_obj.G1)

    assert p1 * np1 == FQ12.one(curve_obj.curve_name)
    assert pn1 == np1


@pytest.mark.parametrize(
    'curve_obj,FQ12',
    (
        (BN128_Curve(), FQ12),
        (Optimized_BN128_Curve(), optimized_FQ12),
        (BLS12_381_Curve(), FQ12),
        (Optimized_BLS12_381_Curve(), optimized_FQ12),
    ),
)
def test_pairing_output_order(curve_obj, FQ12):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)

    assert p1 ** curve_obj.curve_order == FQ12.one(curve_obj.curve_name)


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        Optimized_BN128_Curve(),
        BLS12_381_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_pairing_bilinearity_on_G1(curve_obj):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)
    p2 = curve_obj.pairing(curve_obj.G2, curve_obj.multiply(curve_obj.G1, 2))
    np1 = curve_obj.pairing(curve_obj.neg(curve_obj.G2), curve_obj.G1)

    assert p1 * p1 == p2


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        Optimized_BN128_Curve(),
        BLS12_381_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_pairing_is_non_degenerate(curve_obj):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)
    p2 = curve_obj.pairing(curve_obj.G2, curve_obj.multiply(curve_obj.G1, 2))
    np1 = curve_obj.pairing(curve_obj.neg(curve_obj.G2), curve_obj.G1)

    assert p1 != p2 and p1 != np1 and p2 != np1


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        Optimized_BN128_Curve(),
        BLS12_381_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_pairing_bilinearity_on_G2(curve_obj):
    p1 = curve_obj.pairing(curve_obj.G2, curve_obj.G1)
    po2 = curve_obj.pairing(curve_obj.multiply(curve_obj.G2, 2), curve_obj.G1)

    assert p1 * p1 == po2


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        Optimized_BN128_Curve(),
        BLS12_381_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_pairing_composit_check(curve_obj):
    p3 = curve_obj.pairing(curve_obj.multiply(curve_obj.G2, 27), curve_obj.multiply(curve_obj.G1, 37))
    po3 = curve_obj.pairing(curve_obj.G2, curve_obj.multiply(curve_obj.G1, 999))

    assert p3 == po3
