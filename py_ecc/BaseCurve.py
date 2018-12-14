from abc import (
    abstractmethod,
)

from typing import (  # noqa: F401
    cast,
    List,
)

from py_ecc.field_elements import (  # noqa: F401
    FQ,
    FQP,
    FQ12,
)

from py_ecc.optimized_field_elements import (  # noqa: F401
    FQ as optimized_FQ,
    FQP as optimized_FQP,
    FQ12 as optimized_FQ12,
)

from py_ecc.typing import (
    Field,
    FQPoint2D,
    FQ2Point2D,
    FQ12Point2D,
    GeneralPoint,
    Optimized_Field,
    Optimized_FQPoint3D,
    Optimized_FQ2Point3D,
    Optimized_Point2D,
    Optimized_Point3D,
    Point2D,
)


class BaseCurve:
    # Name of the curve can be "bn128" or "bls12_381"
    curve_name = None  # type: str
    curve_order = None  # type: int
    field_modulus = None  # type: int
    # Curve is y**2 = x**3 + b
    b = None  # type: FQ
    # Twisted curve over FQ**2
    b2 = None  # type: FQP
    # Extension curve over FQ**12; same b value as over FQ
    b12 = None  # type: FQP
    # Generator for curve over FQ
    G1 = None  # type: Point2D[FQ]
    # Generator for twisted curve over FQ2
    G2 = None  # type: Point2D[FQP]
    # Generator for twisted curve over FQ12
    G12 = None  # type: Point2D[FQP]
    # Point at infinity over FQ
    Z1 = None
    # Point at infinity for twisted curve over FQ2
    Z2 = None
    ate_loop_count = None  # type: int
    log_ate_loop_count = None  # type: int
    pseudo_binary_encoding = None  # type: List[int]

    def __init__(self) -> None:
        self.G12 = self.twist(self.G2)

    def is_inf(self, pt: GeneralPoint[Field]) -> bool:
        """
        Check if a point is the point at infinity
        """
        return pt is None

    def is_on_curve(self, pt: Point2D[Field], b: Field) -> bool:
        """
        Check that a point is on the curve
        """
        if self.is_inf(pt):
            return True
        x, y = pt
        return y**2 == x**3 + b

    def double(self, pt: Point2D[Field]) -> Point2D[Field]:
        """
        Elliptic Curve Doubling (P+P).
        """
        x, y = pt
        m = (3 * x**2) / (2 * y)
        newx = m**2 - 2 * x
        newy = -m * newx + m * x - y
        return (newx, newy)

    def add(self,
            p1: Point2D[Field],
            p2: Point2D[Field]) -> Point2D[Field]:
        """
        Elliptic curve addition.
        """
        if p1 is None or p2 is None:
            return p1 if p2 is None else p2
        x1, y1 = p1
        x2, y2 = p2
        if x2 == x1 and y2 == y1:
            return self.double(p1)
        elif x2 == x1:
            return None
        else:
            m = (y2 - y1) / (x2 - x1)
        newx = m**2 - x1 - x2
        newy = -m * newx + m * x1 - y1
        assert newy == (-m * newx + m * x2 - y2)
        return (newx, newy)

    def multiply(self, pt: Point2D[Field], n: int) -> Point2D[Field]:
        """
        Elliptic curve point multiplication.
        """
        if n == 0:
            return None
        elif n == 1:
            return pt
        elif not n % 2:
            return self.multiply(self.double(pt), n // 2)
        else:
            return self.add(self.multiply(self.double(pt), n // 2), pt)

    def eq(self, p1: GeneralPoint[Field], p2: GeneralPoint[Field]) -> bool:
        """
        Check if 2 points are equal.
        """
        return p1 == p2

    def neg(self, pt: Point2D[Field]) -> Point2D[Field]:
        """
        Gives the reflection of point wrt x-axis (P => -P).
        """
        if pt is None:
            return None
        x, y = pt
        return (x, -y)

    @abstractmethod
    def twist(self, pt: Point2D[FQP]) -> Point2D[FQP]:
        """
        'Twist' a point in E(FQ2) into a point in E(FQ12)
        """
        raise NotImplementedError("Must be implemented by subclasses")

    # Pairing Related Functionalities
    def cast_point_to_fq12(self, pt: FQPoint2D) -> FQ12Point2D:
        if pt is None:
            return None
        x, y = pt
        fq12_point = (
            FQ12([x.n] + [0] * 11, self.curve_name),
            FQ12([y.n] + [0] * 11, self.curve_name),
        )
        return cast(FQ12Point2D, fq12_point)

    def linefunc(self,
                 P1: Point2D[Field],
                 P2: Point2D[Field],
                 T: Point2D[Field]) -> Field:
        """
        Create a function representing the line between P1 and P2,
        and evaluate it at T
        """
        assert P1 and P2 and T  # No points-at-infinity allowed, sorry
        x1, y1 = P1
        x2, y2 = P2
        xt, yt = T
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            return m * (xt - x1) - (yt - y1)
        elif y1 == y2:
            m = 3 * x1**2 / (2 * y1)
            return m * (xt - x1) - (yt - y1)
        else:
            return xt - x1

    @abstractmethod
    def miller_loop(self, Q: Point2D[Field], P: Point2D[Field]) -> FQP:
        raise NotImplementedError("Must be implemented by subclasses")

    def pairing(self, Q: FQ2Point2D, P: FQPoint2D) -> FQP:
        assert self.is_on_curve(Q, self.b2)
        assert self.is_on_curve(P, self.b)
        return self.miller_loop(self.twist(Q), self.cast_point_to_fq12(P))


class BaseOptimizedCurve:
    # Name of the curve can be "bn128" or "bls12_381"
    curve_name = None  # type: str
    curve_order = None  # type: int
    field_modulus = None  # type: int
    # Curve is y**2 = x**3 + b
    b = None  # type: optimized_FQ
    # Twisted curve over FQ**2
    b2 = None  # type: optimized_FQP
    # Extension curve over FQ**12; same b value as over FQ
    b12 = None  # type: optimized_FQP
    # Generator for curve over FQ
    G1 = None  # type: Optimized_Point3D[optimized_FQ]
    # Generator for twisted curve over FQ2
    G2 = None  # type: Optimized_Point3D[optimized_FQP]
    # Generator for curve over FQ12
    G12 = None  # type: Optimized_Point3D[optimized_FQP]
    # Point at infinity over FQ
    Z1 = None  # type: Optimized_Point3D[optimized_FQ]
    # Point at infinity for twisted curve over FQ2
    Z2 = None  # type: Optimized_Point3D[optimized_FQP]
    ate_loop_count = None  # type: int
    log_ate_loop_count = None  # type: int
    pseudo_binary_encoding = None  # type: List[int]

    def __init__(self) -> None:
        self.G12 = self.twist(self.G2)

    def is_inf(self, pt: Optimized_Point3D[Optimized_Field]) -> bool:
        """
        Check if a point is the point at infinity
        """
        return pt[-1] == (type(pt[-1]).zero(self.curve_name))

    def is_on_curve(self, pt: Optimized_Point3D[Optimized_Field], b: Optimized_Field) -> bool:
        """
        Check that a point is on the curve defined by y**2 == x**3 + b
        """
        if self.is_inf(pt):
            return True
        x, y, z = pt
        return y**2 * z == x**3 + (b * z**3)

    def double(self, pt: Optimized_Point3D[Optimized_Field]) -> Optimized_Point3D[Optimized_Field]:
        """
        Elliptic curve doubling
        """
        x, y, z = pt
        W = 3 * x * x
        S = y * z
        B = x * y * S
        H = W * W - 8 * B
        S_squared = S * S
        newx = 2 * H * S
        newy = W * (4 * B - H) - 8 * y * y * S_squared
        newz = 8 * S * S_squared
        return (newx, newy, newz)

    def add(self,
            p1: Optimized_Point3D[Optimized_Field],
            p2: Optimized_Point3D[Optimized_Field]) -> Optimized_Point3D[Optimized_Field]:
        """
        Elliptic curve addition
        """
        one, zero = type(p1[0]).one(self.curve_name), type(p1[0]).zero(self.curve_name)
        if p1[2] == zero or p2[2] == zero:
            return p1 if p2[2] == zero else p2
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        U1 = y2 * z1
        U2 = y1 * z2
        V1 = x2 * z1
        V2 = x1 * z2
        if V1 == V2 and U1 == U2:
            return self.double(p1)
        elif V1 == V2:
            return (one, one, zero)
        U = U1 - U2
        V = V1 - V2
        V_squared = V * V
        V_squared_times_V2 = V_squared * V2
        V_cubed = V * V_squared
        W = z1 * z2
        A = U * U * W - V_cubed - 2 * V_squared_times_V2
        newx = V * A
        newy = U * (V_squared_times_V2 - A) - V_cubed * U2
        newz = V_cubed * W
        return (newx, newy, newz)

    def multiply(self,
                 pt: Optimized_Point3D[Optimized_Field],
                 n: int) -> Optimized_Point3D[Optimized_Field]:
        """
        Elliptic curve point multiplication
        """
        if n == 0:
            return (
                type(pt[0]).one(self.curve_name),
                type(pt[0]).one(self.curve_name),
                type(pt[0]).zero(self.curve_name)
            )
        elif n == 1:
            return pt
        elif not n % 2:
            return self.multiply(self.double(pt), n // 2)
        else:
            return self.add(self.multiply(self.double(pt), int(n // 2)), pt)

    def eq(self,
           p1: Optimized_Point3D[Optimized_Field],
           p2: Optimized_Point3D[Optimized_Field]) -> bool:
        """
        Check if 2 points are equal.
        """
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        return x1 * z2 == x2 * z1 and y1 * z2 == y2 * z1

    def normalize(self,
                  pt: Optimized_Point3D[Optimized_Field]) -> Optimized_Point2D[Optimized_Field]:
        """
        Convert the Jacobian Point to a normal point
        """
        x, y, z = pt
        return (x / z, y / z)

    def neg(self, pt: Optimized_Point3D[Optimized_Field]) -> Optimized_Point3D[Optimized_Field]:
        """
        Gives the reflection of point wrt x-axis (P => -P).
        """
        if pt is None:
            return None
        x, y, z = pt
        return (x, -y, z)

    @abstractmethod
    def twist(self, pt: Optimized_Point3D[optimized_FQP]) -> Optimized_Point3D[optimized_FQP]:
        """
        'Twist' a point in E(FQ2) into a point in E(FQ12)
        """
        raise NotImplementedError("Must be implemented by subclasses")

    # Pairing Related Functionalities
    def cast_point_to_fq12(
            self,
            pt: Optimized_Point3D[optimized_FQ]) -> Optimized_Point3D[optimized_FQ12]:
        if pt is None:
            return None
        x, y, z = pt
        return (
            optimized_FQ12([x.n] + [0] * 11, self.curve_name),
            optimized_FQ12([y.n] + [0] * 11, self.curve_name),
            optimized_FQ12([z.n] + [0] * 11, self.curve_name),
        )

    def linefunc(self,
                 P1: Optimized_Point3D[Optimized_Field],
                 P2: Optimized_Point3D[Optimized_Field],
                 T: Optimized_Point3D[Optimized_Field]) -> Optimized_Point2D[Optimized_Field]:
        """
        Create a function representing the line between P1 and P2,
        and evaluate it at T.
        Returns a numerator and a denominator to avoid unneeded divisions
        """
        zero = type(P1[0]).zero(self.curve_name)
        x1, y1, z1 = P1
        x2, y2, z2 = P2
        xt, yt, zt = T
        # points in projective coords: (x / z, y / z)
        # hence, m = (y2/z2 - y1/z1) / (x2/z2 - x1/z1)
        # multiply numerator and denominator by z1z2 to get values below
        m_numerator = y2 * z1 - y1 * z2
        m_denominator = x2 * z1 - x1 * z2
        if m_denominator != zero:
            # m * ((xt/zt) - (x1/z1)) - ((yt/zt) - (y1/z1))
            return m_numerator * (xt * z1 - x1 * zt) - m_denominator * (yt * z1 - y1 * zt), \
                m_denominator * zt * z1
        elif m_numerator == zero:
            # m = 3(x/z)^2 / 2(y/z), multiply num and den by z**2
            m_numerator = 3 * x1 * x1
            m_denominator = 2 * y1 * z1
            return m_numerator * (xt * z1 - x1 * zt) - m_denominator * (yt * z1 - y1 * zt), \
                m_denominator * zt * z1
        else:
            return xt * z1 - x1 * zt, z1 * zt

    @abstractmethod
    def miller_loop(self,
                    Q: Optimized_Point3D[optimized_FQP],
                    P: Optimized_Point3D[optimized_FQP],
                    final_exponentiate: bool=True) -> optimized_FQP:
        raise NotImplementedError("Must be implemented by subclasses")

    def pairing(self,
                Q: Optimized_FQ2Point3D,
                P: Optimized_FQPoint3D,
                final_exponentiate: bool=True) -> optimized_FQP:
        assert self.is_on_curve(Q, self.b2)
        assert self.is_on_curve(P, self.b)
        if P[-1] == (type(P[-1]).zero(self.curve_name)) or Q[-1] == (type(Q[-1]).zero(self.curve_name)):  # noqa: E501
            return optimized_FQ12.one(self.curve_name)
        return self.miller_loop(
            self.twist(Q),
            self.cast_point_to_fq12(P),
            final_exponentiate=final_exponentiate,
        )
