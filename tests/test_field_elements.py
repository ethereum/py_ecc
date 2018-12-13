import pytest

from py_ecc import (
    field_elements,
    optimized_field_elements,
)
from py_ecc.field_properties import (
    field_properties,
)


# Tests both field_elements and optimized_field_elements
@pytest.fixture(params=[field_elements, optimized_field_elements])
def lib(request):
    return request.param


@pytest.fixture
def FQ(lib):
    return lib.FQ


@pytest.fixture
def FQ2(lib):
    return lib.FQ2


@pytest.fixture
def FQ12(lib):
    return lib.FQ12


def test_FQ_object(FQ):
    for curve_name in ("bn128", "bls12_381"):
        field_modulus = field_properties[curve_name]["field_modulus"]
        assert FQ(2, curve_name) * FQ(2, curve_name) == FQ(4, curve_name)
        assert FQ(2, curve_name) / FQ(7, curve_name) + FQ(9, curve_name) / FQ(7, curve_name) == FQ(11, curve_name) / FQ(7, curve_name)
        assert FQ(2, curve_name) * FQ(7, curve_name) + FQ(9, curve_name) * FQ(7, curve_name) == FQ(11, curve_name) * FQ(7, curve_name)
        assert FQ(9, curve_name) ** field_modulus == FQ(9, curve_name)


def test_FQ2_object(FQ2):
    for curve_name in ("bn128", "bls12_381"):
        field_modulus = field_properties[curve_name]["field_modulus"]
        x = FQ2([1, 0], curve_name)
        f = FQ2([1, 2], curve_name)
        fpx = FQ2([2, 2], curve_name)
        one = FQ2.one(curve_name)
        assert x + f == fpx
        assert f / f == one
        assert one / f + x / f == (one + x) / f
        assert one * f + x * f == (one + x) * f
        assert x ** (field_modulus ** 2 - 1) == one


def test_FQ12_object(FQ12):
    for curve_name in ("bn128", "bls12_381"):
        field_modulus = field_properties[curve_name]["field_modulus"]
        x = FQ12([1] + [0] * 11, curve_name)
        f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], curve_name)
        fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], curve_name)
        one = FQ12.one(curve_name)
        assert x + f == fpx
        assert f / f == one
        assert one / f + x / f == (one + x) / f
        assert one * f + x * f == (one + x) * f
        # This check takes too long
        # assert x ** (field_modulus ** 12 - 1) == one
