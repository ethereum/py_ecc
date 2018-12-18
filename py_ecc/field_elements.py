from typing import (
    cast,
    List,
    Sequence,
    Union,
)

from py_ecc.field_properties import (
    field_properties,
)

from py_ecc.utils import (
    deg,
    poly_rounded_div,
    prime_field_inv,
)


IntOrFQ = Union[int, "FQ"]


# A class for field elements in FQ. Wrap a number in this class,
# and it becomes a field element.
class FQ(object):
    n = None  # type: int
    field_modulus = None
    curve_name = None

    def __init__(self, val: IntOrFQ, curve_name: str) -> None:
        """
        curve_name can be either 'bn128' or 'bls12_381'
        This is needed to obtain field_modulus, FQ2_MODULUS_COEFFS
        and FQ12_MODULUS_COEFFS from the curve properties
        """
        self.curve_name = curve_name
        self.field_modulus = field_properties[curve_name]["field_modulus"]

        if isinstance(val, FQ):
            self.n = val.n
        elif isinstance(val, int):
            self.n = val % self.field_modulus
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(val))
            )

    def __add__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ((self.n + on) % self.field_modulus, self.curve_name)

    def __mul__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ((self.n * on) % self.field_modulus, self.curve_name)

    def __rmul__(self, other: IntOrFQ) -> "FQ":
        return self * other

    def __radd__(self, other: IntOrFQ) -> "FQ":
        return self + other

    def __rsub__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ((on - self.n) % self.field_modulus, self.curve_name)

    def __sub__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ((self.n - on) % self.field_modulus, self.curve_name)

    def __div__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ(
            self.n * prime_field_inv(on, self.field_modulus) % self.field_modulus,
            self.curve_name
        )

    def __truediv__(self, other: IntOrFQ) -> "FQ":
        return self.__div__(other)

    def __rdiv__(self, other: IntOrFQ) -> "FQ":
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return FQ(
            prime_field_inv(self.n, self.field_modulus) * on % self.field_modulus,
            self.curve_name
        )

    def __rtruediv__(self, other: IntOrFQ) -> "FQ":
        return self.__rdiv__(other)

    def __pow__(self, other: int) -> "FQ":
        if other == 0:
            return FQ(1, self.curve_name)
        elif other == 1:
            return FQ(self.n, self.curve_name)
        elif other % 2 == 0:
            return (self * self) ** (other // 2)
        else:
            return ((self * self) ** int(other // 2)) * self

    def __eq__(self, other: IntOrFQ) -> bool:  # type:ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        if isinstance(other, FQ):
            return self.n == other.n
        elif isinstance(other, int):
            return self.n == other
        else:
            raise ValueError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

    def __ne__(self, other: IntOrFQ) -> bool:    # type:ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        return not self == other

    def __neg__(self) -> "FQ":
        return FQ(-self.n, self.curve_name)

    def __repr__(self) -> str:
        return repr(self.n)

    def __int__(self) -> int:
        return self.n

    @classmethod
    def one(cls, curve_name: str) -> "FQ":
        return cls(1, curve_name)

    @classmethod
    def zero(cls, curve_name: str) -> "FQ":
        return cls(0, curve_name)


int_types_or_FQ = (int, FQ)


# A class for elements in polynomial extension fields
class FQP(object):
    degree = 0
    curve_name = None

    def __init__(self,
                 coeffs: Sequence[IntOrFQ],
                 curve_name: str,
                 modulus_coeffs: Sequence[IntOrFQ]=None) -> None:
        if len(coeffs) != len(modulus_coeffs):
            raise Exception(
                "coeffs and modulus_coeffs aren't of the same length"
            )
        self.coeffs = tuple(FQ(c, curve_name) for c in coeffs)
        self.curve_name = curve_name
        # The coefficients of the modulus, without the leading [1]
        self.modulus_coeffs = modulus_coeffs
        # The degree of the extension field
        self.degree = len(self.modulus_coeffs)

    def __add__(self, other: "FQP") -> "FQP":
        if not isinstance(other, type(self)):
            raise ValueError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        return type(self)([x + y for x, y in zip(self.coeffs, other.coeffs)], self.curve_name)

    def __sub__(self, other: "FQP") -> "FQP":
        if not isinstance(other, type(self)):
            raise ValueError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        return type(self)([x - y for x, y in zip(self.coeffs, other.coeffs)], self.curve_name)

    def __mul__(self, other: Union[int, "FQ", "FQP"]) -> "FQP":
        if isinstance(other, int) or isinstance(other, FQ):
            return type(self)([c * other for c in self.coeffs], self.curve_name)
        elif isinstance(other, FQP):
            b = [FQ(0, self.curve_name) for i in range(self.degree * 2 - 1)]
            for i in range(self.degree):
                for j in range(self.degree):
                    b[i + j] += self.coeffs[i] * other.coeffs[j]
            while len(b) > self.degree:
                exp, top = len(b) - self.degree - 1, b.pop()
                for i in range(self.degree):
                    b[exp + i] -= top * FQ(self.modulus_coeffs[i], self.curve_name)
            return type(self)(b, self.curve_name)
        else:
            raise ValueError(
                "Expected an int or FQ object or FQP object, but got object of type {}"
                .format(type(other))
            )

    def __rmul__(self, other: Union[int, "FQ", "FQP"]) -> "FQP":
        return self * other

    def __div__(self, other: Union[int, "FQ", "FQP"]) -> "FQP":
        if isinstance(other, int_types_or_FQ):
            return type(self)([c / other for c in self.coeffs], self.curve_name)
        elif isinstance(other, FQP):
            return self * other.inv()
        else:
            raise ValueError(
                "Expected an int or FQ object or FQP object, but got object of type {}"
                .format(type(other))
            )

    def __truediv__(self, other: Union[int, "FQ", "FQP"]) -> "FQP":
        return self.__div__(other)

    def __pow__(self, other: int) -> "FQP":
        if other == 0:
            return type(self)([1] + [0] * (self.degree - 1), self.curve_name)
        elif other == 1:
            return type(self)(self.coeffs, self.curve_name)
        elif other % 2 == 0:
            return (self * self) ** (other // 2)
        else:
            return ((self * self) ** int(other // 2)) * self

    # Extended euclidean algorithm used to find the modular inverse
    def inv(self) -> "FQP":
        lm, hm = (
            [1] + [0] * self.degree,
            [0] * (self.degree + 1),
        )
        low, high = (
            # Ignore mypy yelling about the inner types for  the tuples being incompatible
            cast(List[IntOrFQ], list(self.coeffs + (0,))),  # type: ignore
            cast(List[IntOrFQ], list(self.modulus_coeffs + (1,))),  # type: ignore
        )
        while deg(low):
            r = cast(List[IntOrFQ], list(poly_rounded_div(high, low)))
            r += [0] * (self.degree + 1 - len(r))
            nm = [x for x in hm]
            new = [x for x in high]
            if len(set(
                [len(lm), len(hm), len(low), len(high), len(nm), len(new), self.degree + 1]
            )) != 1:
                raise Exception("Mismatch between the lengths of lm, hm, low, high, nm, new")

            for i in range(self.degree + 1):
                for j in range(self.degree + 1 - i):
                    nm[i + j] -= lm[i] * int(r[j])
                    new[i + j] -= low[i] * int(r[j])
            lm, low, hm, high = nm, new, lm, low
        return type(self)(lm[:self.degree], self.curve_name) / low[0]

    def __repr__(self) -> str:
        return repr(self.coeffs)

    def __eq__(self, other: "FQP") -> bool:     # type: ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        if not isinstance(other, type(self)):
            raise ValueError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        for c1, c2 in zip(self.coeffs, other.coeffs):
            if c1 != c2:
                return False
        return True

    def __ne__(self, other: "FQP") -> bool:     # type: ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        return not self == other

    def __neg__(self) -> "FQP":
        return type(self)([-c for c in self.coeffs], self.curve_name)

    @classmethod
    def one(cls, curve_name: str) -> "FQP":
        return cls([1] + [0] * (cls.degree - 1), curve_name)

    @classmethod
    def zero(cls, curve_name: str) -> "FQP":
        return cls([0] * cls.degree, curve_name)


# The quadratic extension field
class FQ2(FQP):
    degree = 2

    def __init__(self, coeffs: Sequence[IntOrFQ], curve_name: str) -> None:
        FQ2_MODULUS_COEFFS = field_properties[curve_name]["fq2_modulus_coeffs"]
        super().__init__(coeffs, curve_name, FQ2_MODULUS_COEFFS)


# The 12th-degree extension field
class FQ12(FQP):
    degree = 12

    def __init__(self, coeffs: Sequence[IntOrFQ], curve_name: str) -> None:
        FQ12_MODULUS_COEFFS = field_properties[curve_name]["fq12_modulus_coeffs"]
        super().__init__(coeffs, curve_name, FQ12_MODULUS_COEFFS)
