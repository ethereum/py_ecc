from py_ecc.BaseCurve import (
    BaseCurve,
    BaseOptimizedCurve,
)

from py_ecc.curve_properties import (
    curve_properties,
    optimized_curve_properties,
)

from py_ecc.field_elements import (
    FQP,
    FQ12,
)

from py_ecc.field_properties import (
    field_properties,
)

from py_ecc.optimized_field_elements import (
    FQP as optimized_FQP,
    FQ12 as optimized_FQ12,
)

from py_ecc.typing import (
    Field,
    Optimized_Point3D,
    Point2D,
)


class BLS12_381_Curve(BaseCurve):
    curve_name = "bls12_381"
    curve_order = curve_properties[curve_name]["curve_order"]
    field_modulus = field_properties[curve_name]["field_modulus"]
    b = curve_properties[curve_name]["b"]
    b2 = curve_properties[curve_name]["b2"]
    b12 = curve_properties[curve_name]["b12"]
    G1 = curve_properties[curve_name]["G1"]
    G2 = curve_properties[curve_name]["G2"]
    Z1 = curve_properties[curve_name]["Z1"]
    Z2 = curve_properties[curve_name]["Z2"]
    ate_loop_count = curve_properties[curve_name]["ate_loop_count"]
    log_ate_loop_count = curve_properties[curve_name]["log_ate_loop_count"]
    pseudo_binary_encoding = curve_properties[curve_name]["pseudo_binary_encoding"]

    @staticmethod
    def twist(pt: Point2D[FQP]) -> Point2D[FQP]:
        if pt is None:
            return None
        w = FQ12([0, 1] + [0] * 10, "bls12_381")
        _x, _y = pt
        # Field isomorphism from Z[p] / x**2 + 1 to Z[p] / x**2 - 2*x + 2
        xcoeffs = [_x.coeffs[0] - _x.coeffs[1], _x.coeffs[1]]
        ycoeffs = [_y.coeffs[0] - _y.coeffs[1], _y.coeffs[1]]
        # Isomorphism into subfield of Z[p] / w**12 - 2 * w**6 + 2,
        # where w**6 = x
        nx = FQ12([int(xcoeffs[0])] + [0] * 5 + [int(xcoeffs[1])] + [0] * 5, "bls12_381")
        ny = FQ12([int(ycoeffs[0])] + [0] * 5 + [int(ycoeffs[1])] + [0] * 5, "bls12_381")
        # Divide x coord by w**2 and y coord by w**3
        return (nx / w**2, ny / w**3)

    @classmethod
    def miller_loop(cls, Q: Point2D[Field], P: Point2D[Field]) -> FQP:
        if Q is None or P is None:
            return FQ12.one(cls.curve_name)
        R = Q
        f = FQ12.one(cls.curve_name)
        for i in range(cls.log_ate_loop_count, -1, -1):
            f = f * f * cls.linefunc(R, R, P)
            R = cls.double(R)
            if cls.ate_loop_count & (2**i):
                f = f * cls.linefunc(R, Q, P)
                R = cls.add(R, Q)
        # assert R == multiply(Q, ate_loop_count)
        # Q1 = (Q[0] ** field_modulus, Q[1] ** field_modulus)
        # assert is_on_curve(Q1, b12)
        # nQ2 = (Q1[0] ** field_modulus, -Q1[1] ** field_modulus)
        # assert is_on_curve(nQ2, b12)
        # f = f * linefunc(R, Q1, P)
        # R = add(R, Q1)
        # f = f * linefunc(R, nQ2, P)
        # R = add(R, nQ2) This line is in many specifications but it technically does nothing
        return f ** ((cls.field_modulus ** 12 - 1) // cls.curve_order)


class Optimized_BLS12_381_Curve(BaseOptimizedCurve):
    curve_name = "bls12_381"
    curve_order = optimized_curve_properties[curve_name]["curve_order"]
    field_modulus = field_properties[curve_name]["field_modulus"]
    b = optimized_curve_properties[curve_name]["b"]
    b2 = optimized_curve_properties[curve_name]["b2"]
    b12 = optimized_curve_properties[curve_name]["b12"]
    G1 = optimized_curve_properties[curve_name]["G1"]
    G2 = optimized_curve_properties[curve_name]["G2"]
    Z1 = optimized_curve_properties[curve_name]["Z1"]
    Z2 = optimized_curve_properties[curve_name]["Z2"]
    ate_loop_count = optimized_curve_properties[curve_name]["ate_loop_count"]
    log_ate_loop_count = optimized_curve_properties[curve_name]["log_ate_loop_count"]
    pseudo_binary_encoding = optimized_curve_properties[curve_name]["pseudo_binary_encoding"]

    @staticmethod
    def twist(pt: Optimized_Point3D[optimized_FQP]) -> Optimized_Point3D[optimized_FQP]:
        if pt is None:
            return None
        w = optimized_FQ12([0, 1] + [0] * 10, "bls12_381")
        _x, _y, _z = pt
        # Field isomorphism from Z[p] / x**2 + 1 to Z[p] / x**2 - 2*x + 2
        xcoeffs = [_x.coeffs[0] - _x.coeffs[1], _x.coeffs[1]]
        ycoeffs = [_y.coeffs[0] - _y.coeffs[1], _y.coeffs[1]]
        zcoeffs = [_z.coeffs[0] - _z.coeffs[1], _z.coeffs[1]]
        nx = optimized_FQ12([xcoeffs[0]] + [0] * 5 + [xcoeffs[1]] + [0] * 5, "bls12_381")
        ny = optimized_FQ12([ycoeffs[0]] + [0] * 5 + [ycoeffs[1]] + [0] * 5, "bls12_381")
        nz = optimized_FQ12([zcoeffs[0]] + [0] * 5 + [zcoeffs[1]] + [0] * 5, "bls12_381")
        # Divide x coord by w**2 and y coord by w**3
        return (nx / w**2, ny / w**3, nz)

    @classmethod
    def miller_loop(cls,
                    Q: Optimized_Point3D[optimized_FQP],
                    P: Optimized_Point3D[optimized_FQP],
                    final_exponentiate: bool=True) -> optimized_FQP:
        if Q is None or P is None:
            return optimized_FQ12.one(cls.curve_name)
        R = Q
        f_num, f_den = optimized_FQ12.one(cls.curve_name), optimized_FQ12.one(cls.curve_name)
        # for i in range(log_ate_loop_count, -1, -1):
        for v in cls.pseudo_binary_encoding[62::-1]:
            _n, _d = cls.linefunc(R, R, P)
            f_num = f_num * f_num * _n
            f_den = f_den * f_den * _d
            R = cls.double(R)
            if v == 1:
                _n, _d = cls.linefunc(R, Q, P)
                f_num = f_num * _n
                f_den = f_den * _d
                R = cls.add(R, Q)
            elif v == -1:
                nQ = cls.neg(Q)
                _n, _d = cls.linefunc(R, nQ, P)
                f_num = f_num * _n
                f_den = f_den * _d
                R = cls.add(R, nQ)
        # assert R == multiply(Q, ate_loop_count)
        # Q1 = (Q[0] ** field_modulus, Q[1] ** field_modulus, Q[2] ** field_modulus)
        # assert is_on_curve(Q1, b12)
        # nQ2 = (Q1[0] ** field_modulus, -Q1[1] ** field_modulus, Q1[2] ** field_modulus)
        # assert is_on_curve(nQ2, b12)
        # _n1, _d1 = linefunc(R, Q1, P)
        # R = add(R, Q1)
        # _n2, _d2 = linefunc(R, nQ2, P)
        # f = f_num * _n1 * _n2 / (f_den * _d1 * _d2)
        f = f_num / f_den
        # R = add(R, nQ2) This line is in many specifications but it technically does nothing
        if final_exponentiate:
            return f ** ((cls.field_modulus ** 12 - 1) // cls.curve_order)
        else:
            return f


bls12_381 = BLS12_381_Curve()
optimized_bls12_381 = Optimized_BLS12_381_Curve()
