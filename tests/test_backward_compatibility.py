def test_backward_compatibility_imports():
    pass


def test_backward_compatibility_py_evm():
    from py_ecc import (
        optimized_bn128 as bn128,
    )

    FQ = bn128.FQ
    p1 = (FQ(0), FQ(0), FQ(1))
    bn128.is_on_curve(p1, bn128.b)
