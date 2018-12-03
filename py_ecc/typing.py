from py_ecc.bn128.bn128_field_elements import (
    FQ,
    FQP,
    FQ2,
    FQ12,
)

from typing import (
    Tuple,
    TypeVar,
    Union,
)


# These types are wrt FQ, FQ2, FQ12
FQPoint2D = Tuple[FQ, FQ]
FQ2Point2D = Tuple[FQ2, FQ2]
FQ12Point2D = Tuple[FQ12, FQ12]
FQPPoint2D = Tuple[FQP, FQP]

FQPoint3D = Tuple[FQ, FQ, FQ]
FQ2Point3D = Tuple[FQ2, FQ2, FQ2]
FQ12Point3D = Tuple[FQ12, FQ12, FQ12]
FQPPoint3D = Tuple[FQP, FQP, FQP]

# These types are wrt Normal Integers
PlainPoint2D = Tuple[int, int]
PlainPoint3D = Tuple[int, int, int]

Field = TypeVar('Field', FQ, FQP)
Point2D = Tuple[Field, Field]
Point3D = Tuple[Field, Field, Field]
GeneralPoint = Union[Point2D[Field], Point3D[Field]]
