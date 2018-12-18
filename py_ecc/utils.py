from typing import (
    cast,
    Tuple,
    Sequence,
    Union,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from py_ecc.field_elements import (  # noqa: F401
        FQ,
    )
    from py_ecc.optimized_field_elements import (  # noqa: F401
        FQ as optimized_FQ,
    )


IntOrFQ = Union[int, "FQ"]


def prime_field_inv(a: int, n: int) -> int:
    """
    Extended euclidean algorithm to find modular inverses for integers
    """
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


# Utility methods for polynomial math
def deg(p: Sequence[Union[int, "FQ", "optimized_FQ"]]) -> int:
    d = len(p) - 1
    while p[d] == 0 and d:
        d -= 1
    return d


def poly_rounded_div(a: Sequence[IntOrFQ],
                     b: Sequence[IntOrFQ]) -> Tuple[IntOrFQ]:
    dega = deg(a)
    degb = deg(b)
    temp = [x for x in a]
    o = [0 for x in a]
    for i in range(dega - degb, -1, -1):
        o[i] += int(temp[degb + i] / b[degb])
        for c in range(degb + 1):
            temp[c + i] -= o[c]
    return cast(Tuple[IntOrFQ], tuple(o[:deg(o) + 1]))
