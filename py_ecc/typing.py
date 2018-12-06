from typing import (
    Tuple,
    TypeVar,
    TYPE_CHECKING,
    Union,
)

from py_ecc.bn128.bn128_field_elements import (
    FQ,
    FQP,
    FQ2,
    FQ12,
)

if TYPE_CHECKING:
    from py_ecc.optimized_bn128.optimized_field_elements import (  # noqa: F401
        FQ as Optimized_FQ,
        FQP as Optimized_FQP,
        FQ2 as Optimized_FQ2,
        FQ12 as Optimized_FQ12,
    )


# Types For bn128 module
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


# Types For optimized_bn128_module
# These types are wrt FQ, FQ2, FQ12
Optimized_FQPoint2D = Tuple["Optimized_FQ", "Optimized_FQ"]
Optimized_FQ2Point2D = Tuple["Optimized_FQ2", "Optimized_FQ2"]
Optimized_FQ12Point2D = Tuple["Optimized_FQ12", "Optimized_FQ12"]
Optimized_FQPPoint2D = Tuple["Optimized_FQP", "Optimized_FQP"]

Optimized_FQPoint3D = Tuple["Optimized_FQ", "Optimized_FQ", "Optimized_FQ"]
Optimized_FQ2Point3D = Tuple["Optimized_FQ2", "Optimized_FQ2", "Optimized_FQ2"]
Optimized_FQ12Point3D = Tuple["Optimized_FQ12", "Optimized_FQ12", "Optimized_FQ12"]
Optimized_FQPPoint3D = Tuple["Optimized_FQP", "Optimized_FQP", "Optimized_FQP"]

Optimized_Field = TypeVar('Optimized_Field', "Optimized_FQ", "Optimized_FQP")
Optimized_Point2D = Tuple[Optimized_Field, Optimized_Field]
Optimized_Point3D = Tuple[Optimized_Field, Optimized_Field, Optimized_Field]
Optimized_GeneralPoint = Union[Point2D[Optimized_Field], Point3D[Optimized_Field]]
