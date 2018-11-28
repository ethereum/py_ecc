import hashlib
import hmac
import sys

from typing import (
    Any,
    cast,
    Tuple,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from py_ecc.typing import (  # noqa: F401
        PlainPoint2D,
        PlainPoint3D,
    )


if sys.version_info.major == 2:
    safe_ord = ord
else:
    def safe_ord(value: Any) -> int:    # type: ignore
        if isinstance(value, int):
            return value
        else:
            return ord(value)


# Elliptic curve parameters (secp256k1)
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = cast("PlainPoint2D", (Gx, Gy))


def bytes_to_int(x: bytes) -> int:
    o = 0
    for b in x:
        o = (o << 8) + safe_ord(b)      # type: ignore
    return o


# Extended Euclidean Algorithm
def inv(a: int, n: int) -> int:
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def to_jacobian(p: "PlainPoint2D") -> "PlainPoint3D":
    o = (p[0], p[1], 1)
    return cast("PlainPoint3D", o)


def jacobian_double(p: "PlainPoint3D") -> "PlainPoint3D":
    if not p[1]:
        return cast("PlainPoint3D", (0, 0, 0))
    ysq = (p[1] ** 2) % P
    S = (4 * p[0] * ysq) % P
    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P
    nx = (M**2 - 2 * S) % P
    ny = (M * (S - nx) - 8 * ysq ** 2) % P
    nz = (2 * p[1] * p[2]) % P
    return cast("PlainPoint3D", (nx, ny, nz))


def jacobian_add(p: "PlainPoint3D", q: "PlainPoint3D") -> "PlainPoint3D":
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % P
    U2 = (q[0] * p[2] ** 2) % P
    S1 = (p[1] * q[2] ** 3) % P
    S2 = (q[1] * p[2] ** 3) % P
    if U1 == U2:
        if S1 != S2:
            return cast("PlainPoint3D", (0, 0, 1))
        return jacobian_double(p)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % P
    H3 = (H * H2) % P
    U1H2 = (U1 * H2) % P
    nx = (R ** 2 - H3 - 2 * U1H2) % P
    ny = (R * (U1H2 - nx) - S1 * H3) % P
    nz = (H * p[2] * q[2]) % P
    return cast("PlainPoint3D", (nx, ny, nz))


def from_jacobian(p: "PlainPoint3D") -> "PlainPoint2D":
    z = inv(p[2], P)
    return cast("PlainPoint2D", ((p[0] * z**2) % P, (p[1] * z**3) % P))


def jacobian_multiply(a: "PlainPoint3D", n: int) -> "PlainPoint3D":   # type: ignore
    if a[1] == 0 or n == 0:
        return cast("PlainPoint3D", (0, 0, 1))
    if n == 1:
        return a
    if n < 0 or n >= N:
        return jacobian_multiply(a, n % N)
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n // 2))
    if (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n // 2)), a)


def multiply(a: "PlainPoint2D", n: int) -> "PlainPoint2D":
    return from_jacobian(jacobian_multiply(to_jacobian(a), n))


def add(a: "PlainPoint2D", b: "PlainPoint2D") -> "PlainPoint2D":
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))


# bytes32
def privtopub(privkey: bytes) -> "PlainPoint2D":
    return multiply(G, bytes_to_int(privkey))


def deterministic_generate_k(msghash: bytes, priv: bytes) -> int:
    v = b'\x01' * 32
    k = b'\x00' * 32
    k = hmac.new(k, v + b'\x00' + priv + msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b'\x01' + priv + msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return bytes_to_int(hmac.new(k, v, hashlib.sha256).digest())


# bytes32, bytes32 -> v, r, s (as numbers)
def ecdsa_raw_sign(msghash: bytes, priv: bytes) -> Tuple[int, int, int]:

    z = bytes_to_int(msghash)
    k = deterministic_generate_k(msghash, priv)

    r, y = multiply(G, k)
    s = inv(k, N) * (z + r * bytes_to_int(priv)) % N

    v, r, s = 27 + ((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s


def ecdsa_raw_recover(msghash: bytes, vrs: Tuple[int, int, int]) -> "PlainPoint2D":
    v, r, s = vrs
    if not (27 <= v <= 34):
        raise ValueError("%d must in range 27-31" % v)
    x = r
    xcubedaxb = (x * x * x + A * x + B) % P
    beta = pow(xcubedaxb, (P + 1) // 4, P)
    y = beta if v % 2 ^ beta % 2 else (P - beta)
    # If xcubedaxb is not a quadratic residue, then r cannot be the x coord
    # for a point on the curve, and so the sig is invalid
    if (xcubedaxb - y * y) % P != 0 or not (r % N) or not (s % N):
        raise ValueError("sig is invalid, %d cannot be the x coord for point on curve" % r)
    z = bytes_to_int(msghash)
    Gz = jacobian_multiply(cast("PlainPoint3D", (Gx, Gy, 1)), (N - z) % N)
    XY = jacobian_multiply(cast("PlainPoint3D", (x, y, 1)), s)
    Qr = jacobian_add(Gz, XY)
    Q = jacobian_multiply(Qr, inv(r, N))
    Q_jacobian = from_jacobian(Q)

    return Q_jacobian
