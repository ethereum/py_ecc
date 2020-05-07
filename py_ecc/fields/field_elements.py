from typing import (  # noqa: F401
    cast,
    List,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    TYPE_CHECKING,
)

from py_ecc.utils import (
    deg,
    poly_rounded_div,
    prime_field_inv,
)

if TYPE_CHECKING:
    from py_ecc.typing import (  # noqa: F401
        FQ2_modulus_coeffs_type,
        FQ12_modulus_coeffs_type,
    )


# These new TypeVars are needed because these classes are kind of base classes and
# we need the output type to correspond to the type of the inherited class
T_FQ = TypeVar('T_FQ', bound="FQ")
T_FQP = TypeVar('T_FQP', bound="FQP")
T_FQ2 = TypeVar('T_FQ2', bound="FQ2")
T_FQ12 = TypeVar('T_FQ12', bound="FQ12")
IntOrFQ = Union[int, T_FQ]


class FQ(object):
    """
    A class for field elements in FQ. Wrap a number in this class,
    and it becomes a field element.
    """
    n = None  # type: int
    field_modulus = None  # type: int

    def __init__(self: T_FQ, val: IntOrFQ) -> None:
        if self.field_modulus is None:
            raise AttributeError("Field Modulus hasn't been specified")

        if isinstance(val, FQ):
            self.n = val.n
        elif isinstance(val, int):
            self.n = val % self.field_modulus
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(val))
            )

    def __add__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)((self.n + on) % self.field_modulus)

    def __mul__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)((self.n * on) % self.field_modulus)

    def __rmul__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        return self * other

    def __radd__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        return self + other

    def __rsub__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)((on - self.n) % self.field_modulus)

    def __sub__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)((self.n - on) % self.field_modulus)

    def __div__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)(
            self.n * prime_field_inv(on, self.field_modulus) % self.field_modulus
        )

    def __truediv__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        return self.__div__(other)

    def __rdiv__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        if isinstance(other, FQ):
            on = other.n
        elif isinstance(other, int):
            on = other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

        return type(self)(
            prime_field_inv(self.n, self.field_modulus) * on % self.field_modulus
        )

    def __rtruediv__(self: T_FQ, other: IntOrFQ) -> T_FQ:
        return self.__rdiv__(other)

    def __pow__(self: T_FQ, other: int) -> T_FQ:
        if other == 0:
            return type(self)(1)
        elif other == 1:
            return type(self)(self.n)
        elif other % 2 == 0:
            return (self * self) ** (other // 2)
        else:
            return ((self * self) ** int(other // 2)) * self

    def __eq__(self: T_FQ, other: IntOrFQ) -> bool:
        if isinstance(other, FQ):
            return self.n == other.n
        elif isinstance(other, int):
            return self.n == other
        else:
            raise TypeError(
                "Expected an int or FQ object, but got object of type {}"
                .format(type(other))
            )

    def __ne__(self: T_FQ, other: IntOrFQ) -> bool:
        return not self == other

    def __neg__(self: T_FQ) -> T_FQ:
        return type(self)(-self.n)

    def __repr__(self: T_FQ) -> str:
        return repr(self.n)

    def __int__(self: T_FQ) -> int:
        return self.n

    @classmethod
    def one(cls: Type[T_FQ]) -> T_FQ:
        return cls(1)

    @classmethod
    def zero(cls: Type[T_FQ]) -> T_FQ:
        return cls(0)


int_types_or_FQ = (int, FQ)


class FQP(object):
    """
    A class for elements in polynomial extension fields
    """
    degree = 0
    field_modulus = None  # type: int

    def __init__(self,
                 coeffs: Sequence[IntOrFQ],
                 modulus_coeffs: Sequence[IntOrFQ] = ()) -> None:
        if self.field_modulus is None:
            raise AttributeError("Field Modulus hasn't been specified")

        if len(coeffs) != len(modulus_coeffs):
            raise Exception(
                "coeffs and modulus_coeffs aren't of the same length"
            )
        # Encoding all coefficients in the corresponding type FQ
        self.FQP_corresponding_FQ_class = type(
            "FQP_corresponding_FQ_class",
            (FQ,),
            {'field_modulus': self.field_modulus}
        )  # type: Type[FQ]
        self.coeffs = tuple(
            self.FQP_corresponding_FQ_class(c) for c in coeffs
        )  # type: Tuple[IntOrFQ, ...]
        # The coefficients of the modulus, without the leading [1]
        self.modulus_coeffs = tuple(modulus_coeffs)  # type: Tuple[IntOrFQ, ...]
        # The degree of the extension field
        self.degree = len(self.modulus_coeffs)

    def __add__(self: T_FQP, other: T_FQP) -> T_FQP:
        if not isinstance(other, type(self)):
            raise TypeError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        return type(self)([x + y for x, y in zip(self.coeffs, other.coeffs)])

    def __sub__(self: T_FQP, other: T_FQP) -> T_FQP:
        if not isinstance(other, type(self)):
            raise TypeError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        return type(self)([x - y for x, y in zip(self.coeffs, other.coeffs)])

    def __mul__(self: T_FQP, other: Union[int, T_FQ, T_FQP]) -> T_FQP:
        if isinstance(other, int_types_or_FQ):
            return type(self)([c * other for c in self.coeffs])
        elif isinstance(other, FQP):
            b = [self.FQP_corresponding_FQ_class(0) for i in range(self.degree * 2 - 1)]
            for i in range(self.degree):
                for j in range(self.degree):
                    b[i + j] += self.coeffs[i] * other.coeffs[j]
            while len(b) > self.degree:
                exp, top = len(b) - self.degree - 1, b.pop()
                for i in range(self.degree):
                    b[exp + i] -= top * self.FQP_corresponding_FQ_class(self.modulus_coeffs[i])
            return type(self)(b)
        else:
            raise TypeError(
                "Expected an int or FQ object or FQP object, but got object of type {}"
                .format(type(other))
            )

    def __rmul__(self: T_FQP, other: Union[int, T_FQP]) -> T_FQP:
        return self * other

    def __div__(self: T_FQP, other: Union[int, T_FQP]) -> T_FQP:
        if isinstance(other, int_types_or_FQ):
            return type(self)([c / other for c in self.coeffs])
        elif isinstance(other, FQP):
            return self * other.inv()
        else:
            raise TypeError(
                "Expected an int or FQ object or FQP object, but got object of type {}"
                .format(type(other))
            )

    def __truediv__(self: T_FQP, other: Union[int, T_FQP]) -> T_FQP:
        return self.__div__(other)

    def __pow__(self: T_FQP, other: int) -> T_FQP:
        if other == 0:
            return type(self)([1] + [0] * (self.degree - 1))
        elif other == 1:
            return type(self)(self.coeffs)
        elif other % 2 == 0:
            return (self * self) ** (other // 2)
        else:
            return ((self * self) ** int(other // 2)) * self

    # Extended euclidean algorithm used to find the modular inverse
    def inv(self: T_FQP) -> T_FQP:
        lm, hm = (
            [1] + [0] * self.degree,
            [0] * (self.degree + 1),
        )
        low, high = (
            # Ignore mypy yelling about the inner types for  the tuples being incompatible
            cast(List[IntOrFQ], list(self.coeffs + (0,))),
            cast(List[IntOrFQ], list(self.modulus_coeffs + (1,))),
        )
        while deg(low):
            r = cast(List[IntOrFQ], list(poly_rounded_div(high, low)))
            r += [0] * (self.degree + 1 - len(r))
            nm = [x for x in hm]
            new = [x for x in high]

            if len(lm) != self.degree + 1:
                raise Exception("Length of lm is not {}".format(self.degree + 1))
            elif len(hm) != self.degree + 1:
                raise Exception("Length of hm is not {}".format(self.degree + 1))
            elif len(nm) != self.degree + 1:
                raise Exception("Length of nm is not {}".format(self.degree + 1))
            elif len(low) != self.degree + 1:
                raise Exception("Length of low is not {}".format(self.degree + 1))
            elif len(high) != self.degree + 1:
                raise Exception("Length of high is not {}".format(self.degree + 1))
            elif len(new) != self.degree + 1:
                raise Exception("Length of new is not {}".format(self.degree + 1))

            for i in range(self.degree + 1):
                for j in range(self.degree + 1 - i):
                    nm[i + j] -= lm[i] * int(r[j])
                    new[i + j] -= low[i] * int(r[j])
            lm, low, hm, high = nm, new, lm, low
        return type(self)(lm[:self.degree]) / low[0]

    def __repr__(self: T_FQP) -> str:
        return repr(self.coeffs)

    def __eq__(self: T_FQP, other: T_FQP) -> bool:     # type: ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        if not isinstance(other, type(self)):
            raise TypeError(
                "Expected an FQP object, but got object of type {}"
                .format(type(other))
            )

        for c1, c2 in zip(self.coeffs, other.coeffs):
            if c1 != c2:
                return False
        return True

    def __ne__(self: T_FQP, other: T_FQP) -> bool:     # type: ignore # https://github.com/python/mypy/issues/2783 # noqa: E501
        return not self == other

    def __neg__(self: T_FQP) -> T_FQP:
        return type(self)([-c for c in self.coeffs])

    @classmethod
    def one(cls: Type[T_FQP]) -> T_FQP:
        return cls([1] + [0] * (cls.degree - 1))

    @classmethod
    def zero(cls: Type[T_FQP]) -> T_FQP:
        return cls([0] * cls.degree)


class FQ2(FQP):
    """
    The quadratic extension field
    """
    degree = 2
    FQ2_MODULUS_COEFFS = None  # type: FQ2_modulus_coeffs_type

    def __init__(self, coeffs: Sequence[IntOrFQ]) -> None:
        if self.FQ2_MODULUS_COEFFS is None:
            raise AttributeError("FQ2 Modulus Coeffs haven't been specified")

        super().__init__(coeffs, self.FQ2_MODULUS_COEFFS)


class FQ12(FQP):
    """
    The 12th-degree extension field
    """
    degree = 12
    FQ12_MODULUS_COEFFS = None  # type: FQ12_modulus_coeffs_type

    def __init__(self, coeffs: Sequence[IntOrFQ]) -> None:
        if self.FQ12_MODULUS_COEFFS is None:
            raise AttributeError("FQ12 Modulus Coeffs haven't been specified")

        super().__init__(coeffs, self.FQ12_MODULUS_COEFFS)
