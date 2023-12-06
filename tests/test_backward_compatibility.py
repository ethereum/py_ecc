def test_backward_compatibility_imports():
    from py_ecc.bls12_381 import (  # noqa: F401
        FQ,
        FQ2,
        FQ12,
        FQP,
        field_modulus,
    )
    from py_ecc.bn128 import (  # noqa: F401
        FQ,
        FQ2,
        FQ12,
        FQP,
        field_modulus,
    )
    from py_ecc.optimized_bls12_381 import (  # noqa: F401
        FQ,
        FQ2,
        FQ12,
        FQP,
        field_modulus,
    )
    from py_ecc.optimized_bn128 import (  # noqa: F401
        FQ,
        FQ2,
        FQ12,
        FQP,
        field_modulus,
    )


def test_backward_compatibility_py_evm():
    from py_ecc import (
        optimized_bn128 as bn128,
    )
    from py_ecc.optimized_bn128 import (  # noqa: F401
        FQ2,
        FQP,
    )

    FQ = bn128.FQ
    p1 = (FQ(0), FQ(0), FQ(1))
    bn128.is_on_curve(p1, bn128.b)
