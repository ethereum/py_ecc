import time

import pytest

from py_ecc import bn128, optimized_bn128, bls12_381, optimized_bls12_381


@pytest.fixture(params=[bn128, optimized_bn128, bls12_381, optimized_bls12_381])
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


@pytest.fixture
def field_modulus(lib):
    return lib.field_modulus

@pytest.fixture
def G1(lib):
    return lib.G1


@pytest.fixture
def G2(lib):
    return lib.G2


@pytest.fixture
def G12(lib):
    return lib.G12


@pytest.fixture
def b(lib):
    return lib.b


@pytest.fixture
def b2(lib):
    return lib.b2


@pytest.fixture
def b12(lib):
    return lib.b12


@pytest.fixture
def is_inf(lib):
    return lib.is_inf


@pytest.fixture
def is_on_curve(lib):
    return lib.is_on_curve


@pytest.fixture
def eq(lib):
    return lib.eq


@pytest.fixture
def add(lib):
    return lib.add


@pytest.fixture
def double(lib):
    return lib.double


@pytest.fixture
def curve_order(lib):
    return lib.curve_order


@pytest.fixture
def multiply(lib):
    return lib.multiply


@pytest.fixture
def pairing(lib):
    return lib.pairing


@pytest.fixture
def neg(lib):
    return lib.neg


def test_FQ_object(FQ, field_modulus):
    assert FQ(2) * FQ(2) == FQ(4)
    assert FQ(2) / FQ(7) + FQ(9) / FQ(7) == FQ(11) / FQ(7)
    assert FQ(2) * FQ(7) + FQ(9) * FQ(7) == FQ(11) * FQ(7)
    assert FQ(9) ** field_modulus == FQ(9)


def test_FQ2_object(FQ2, field_modulus):
    x = FQ2([1, 0])
    f = FQ2([1, 2])
    fpx = FQ2([2, 2])
    one = FQ2.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (field_modulus ** 2 - 1) == one


def test_FQ12_object(FQ12, field_modulus):
    x = FQ12([1] + [0] * 11)
    f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    one = FQ12.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    # This check takes too long
    # assert x ** (field_modulus ** 12 - 1) == one


def test_G1_object(G1, eq, double, add, multiply, curve_order, is_inf):
    assert eq(add(add(double(G1), G1), G1), double(double(G1)))
    assert not eq(double(G1), G1)
    assert eq(add(multiply(G1, 9), multiply(G1, 5)), add(multiply(G1, 12), multiply(G1, 2)))
    assert is_inf(multiply(G1, curve_order))


def test_G2_object(G2, b2, eq, add, double, multiply, is_inf, curve_order, field_modulus, is_on_curve):
    assert eq(add(add(double(G2), G2), G2), double(double(G2)))
    assert not eq(double(G2), G2)
    assert eq(add(multiply(G2, 9), multiply(G2, 5)), add(multiply(G2, 12), multiply(G2, 2)))
    assert is_inf(multiply(G2, curve_order))
    assert not is_inf(multiply(G2, 2 * field_modulus - curve_order))
    assert is_on_curve(multiply(G2, 9), b2)


def test_G12_object(G12, b12, eq, add, double, multiply, is_on_curve, is_inf, curve_order):
    assert eq(add(add(double(G12), G12), G12), double(double(G12)))
    assert not eq(double(G12), G12)
    assert eq(add(multiply(G12, 9), multiply(G12, 5)), add(multiply(G12, 12), multiply(G12, 2)))
    assert is_on_curve(multiply(G12, 9), b12)
    assert is_inf(multiply(G12, curve_order))


def test_pairing_negative_G1(pairing, G1, G2, FQ12, curve_order, multiply, neg):
    p1 = pairing(G2, G1)
    pn1 = pairing(G2, neg(G1))

    assert p1 * pn1 == FQ12.one()


def test_pairing_negative_G2(pairing, G1, G2, FQ12, curve_order, multiply, neg):
    p1 = pairing(G2, G1)
    pn1 = pairing(G2, neg(G1))
    np1 = pairing(neg(G2), G1)

    assert p1 * np1 == FQ12.one()
    assert pn1 == np1


def test_pairing_output_order(G1, G2, FQ12, pairing, curve_order):
    p1 = pairing(G2, G1)

    assert p1 ** curve_order == FQ12.one()


def test_pairing_bilinearity_on_G1(G1, G2, neg, multiply, pairing):
    p1 = pairing(G2, G1)
    p2 = pairing(G2, multiply(G1, 2))
    np1 = pairing(neg(G2), G1)

    assert p1 * p1 == p2


def test_pairing_is_non_degenerate(G1, G2, neg, pairing, multiply):
    p1 = pairing(G2, G1)
    p2 = pairing(G2, multiply(G1, 2))
    np1 = pairing(neg(G2), G1)

    assert p1 != p2 and p1 != np1 and p2 != np1


def test_pairing_bilinearity_on_G2(G1, G2, pairing, multiply):
    p1 = pairing(G2, G1)
    po2 = pairing(multiply(G2, 2), G1)

    assert p1 * p1 == po2


def test_pairing_composit_check(G1, G2, multiply, pairing):
    p3 = pairing(multiply(G2, 27), multiply(G1, 37))
    po3 = pairing(G2, multiply(G1, 999))
    assert p3 == po3


"""
for lib in (bn128, optimized_bn128):
    FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
    assert FQ(2) * FQ(2) == FQ(4)
    assert FQ(2) / FQ(7) + FQ(9) / FQ(7) == FQ(11) / FQ(7)
    assert FQ(2) * FQ(7) + FQ(9) * FQ(7) == FQ(11) * FQ(7)
    assert FQ(9) ** field_modulus == FQ(9)
    print('FQ works fine')

    x = FQ2([1, 0])
    f = FQ2([1, 2])
    fpx = FQ2([2, 2])
    one = FQ2.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (field_modulus ** 2 - 1) == one
    print('FQ2 works fine')

    x = FQ12([1] + [0] * 11)
    f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    one = FQ12.one()
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    # This check takes too long
    # assert x ** (field_modulus ** 12 - 1) == one
    print('FQ12 works fine')

    G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply

    assert eq(add(add(double(G1), G1), G1), double(double(G1)))
    assert not eq(double(G1), G1)
    assert eq(add(multiply(G1, 9), multiply(G1, 5)), add(multiply(G1, 12), multiply(G1, 2)))
    assert is_inf(multiply(G1, curve_order))
    print('G1 works fine')

    assert eq(add(add(double(G2), G2), G2), double(double(G2)))
    assert not eq(double(G2), G2)
    assert eq(add(multiply(G2, 9), multiply(G2, 5)), add(multiply(G2, 12), multiply(G2, 2)))
    assert is_inf(multiply(G2, curve_order))
    assert not is_inf(multiply(G2, 2 * field_modulus - curve_order))
    assert is_on_curve(multiply(G2, 9), b2)
    print('G2 works fine')

    assert eq(add(add(double(G12), G12), G12), double(double(G12)))
    assert not eq(double(G12), G12)
    assert eq(add(multiply(G12, 9), multiply(G12, 5)), add(multiply(G12, 12), multiply(G12, 2)))
    assert is_on_curve(multiply(G12, 9), b12)
    assert is_inf(multiply(G12, curve_order))
    print('G12 works fine')

    pairing, neg = lib.pairing, lib.neg

    print('Starting pairing tests')
    a = time.time()
    p1 = pairing(G2, G1)
    pn1 = pairing(G2, neg(G1))
    assert p1 * pn1 == FQ12.one()
    print('Pairing check against negative in G1 passed')
    np1 = pairing(neg(G2), G1)
    assert p1 * np1 == FQ12.one()
    assert pn1 == np1
    print('Pairing check against negative in G2 passed')
    assert p1 ** curve_order == FQ12.one()
    print('Pairing output has correct order')
    p2 = pairing(G2, multiply(G1, 2))
    assert p1 * p1 == p2
    print('Pairing bilinearity in G1 passed')
    assert p1 != p2 and p1 != np1 and p2 != np1
    print('Pairing is non-degenerate')
    po2 = pairing(multiply(G2, 2), G1)
    assert p1 * p1 == po2
    print('Pairing bilinearity in G2 passed')
    p3 = pairing(multiply(G2, 27), multiply(G1, 37))
    po3 = pairing(G2, multiply(G1, 999))
    assert p3 == po3
    print('Composite check passed')
    print('Total time for pairings: %.3f' % (time.time() - a))
"""
