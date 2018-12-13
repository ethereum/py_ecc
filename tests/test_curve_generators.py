import pytest

from py_ecc import (
    field_elements,
    optimized_field_elements,
)

from py_ecc.bls12_381_curve import (
    BLS12_381_Curve,
    Optimized_BLS12_381_Curve,
)
from py_ecc.bn128_curve import (
    BN128_Curve,
    Optimized_BN128_Curve,
)

from py_ecc.curve_properties import (
    curve_properties,
    optimized_curve_properties,
)

from py_ecc.field_properties import (
    field_properties,
)


@pytest.mark.parametrize(
    'curve_obj,G1',
    (
        (BN128_Curve(), curve_properties["bn128"]["G1"]),
        (Optimized_BN128_Curve(), optimized_curve_properties["bn128"]["G1"]),
        (BLS12_381_Curve(), curve_properties["bls12_381"]["G1"]),
        (Optimized_BLS12_381_Curve(), optimized_curve_properties["bls12_381"]["G1"]),
    ),
)
def test_G1_object(curve_obj, G1):
    assert curve_obj.eq(curve_obj.add(curve_obj.add(curve_obj.double(G1), G1), G1), curve_obj.double(curve_obj.double(G1)))
    assert not curve_obj.eq(curve_obj.double(G1), G1)
    assert curve_obj.eq(curve_obj.add(curve_obj.multiply(G1, 9), curve_obj.multiply(G1, 5)), curve_obj.add(curve_obj.multiply(G1, 12), curve_obj.multiply(G1, 2)))
    assert curve_obj.is_inf(curve_obj.multiply(G1, curve_obj.curve_order))


@pytest.mark.parametrize(
    'curve_obj,G2,field_modulus',
    (
        (BN128_Curve(), curve_properties["bn128"]["G2"], field_properties["bn128"]["field_modulus"]),
        (Optimized_BN128_Curve(), optimized_curve_properties["bn128"]["G2"], field_properties["bn128"]["field_modulus"]),
        (BLS12_381_Curve(), curve_properties["bls12_381"]["G2"], field_properties["bls12_381"]["field_modulus"]),
        (Optimized_BLS12_381_Curve(), optimized_curve_properties["bls12_381"]["G2"], field_properties["bls12_381"]["field_modulus"]),
    ),
)
def test_G2_object(curve_obj, G2, field_modulus):
    assert curve_obj.eq(curve_obj.add(curve_obj.add(curve_obj.double(G2), G2), G2), curve_obj.double(curve_obj.double(G2)))
    assert not curve_obj.eq(curve_obj.double(G2), G2)
    assert curve_obj.eq(curve_obj.add(curve_obj.multiply(G2, 9), curve_obj.multiply(G2, 5)), curve_obj.add(curve_obj.multiply(G2, 12), curve_obj.multiply(G2, 2)))
    assert curve_obj.is_inf(curve_obj.multiply(G2, curve_obj.curve_order))
    assert not curve_obj.is_inf(curve_obj.multiply(G2, 2 * field_modulus - curve_obj.curve_order))
    assert curve_obj.is_on_curve(curve_obj.multiply(G2, 9), curve_obj.b2)


@pytest.mark.parametrize(
    'curve_obj',
    (
        BN128_Curve(),
        Optimized_BN128_Curve(),
        BLS12_381_Curve(),
        Optimized_BLS12_381_Curve(),
    ),
)
def test_G12_object(curve_obj):
    G12 = curve_obj.G12
    assert curve_obj.eq(curve_obj.add(curve_obj.add(curve_obj.double(G12), G12), G12), curve_obj.double(curve_obj.double(G12)))
    assert not curve_obj.eq(curve_obj.double(G12), G12)
    assert curve_obj.eq(curve_obj.add(curve_obj.multiply(G12, 9), curve_obj.multiply(G12, 5)), curve_obj.add(curve_obj.multiply(G12, 12), curve_obj.multiply(G12, 2)))
    assert curve_obj.is_on_curve(curve_obj.multiply(G12, 9), curve_obj.b12)
    assert curve_obj.is_inf(curve_obj.multiply(G12, curve_obj.curve_order))
