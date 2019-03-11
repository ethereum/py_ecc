def test_backward_compatibility_imports():
    from py_ecc.bn128 import (
        field_modulus,
        FQ,
        FQP,
        FQ2,
        FQ12,
    )
    from py_ecc.bls12_381 import (
        field_modulus,
        FQ,
        FQP,
        FQ2,
        FQ12,
    )
    from py_ecc.optimized_bn128 import (
        field_modulus,
        FQ,
        FQP,
        FQ2,
        FQ12,
    )
    from py_ecc.optimized_bls12_381 import (
        field_modulus,
        FQ,
        FQP,
        FQ2,
        FQ12,
    )


def test_backward_compatibility_py_evm():
    from py_ecc import optimized_bn128 as bn128
    from py_ecc.optimized_bn128 import (
        FQP,
        FQ2,
    )

    FQ = bn128.FQ
    p1 = (FQ(0), FQ(0), FQ(1))
    bn128.is_on_curve(p1, bn128.b)
