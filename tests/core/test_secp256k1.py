import pytest
import binascii

from py_ecc.secp256k1 import (
    ecdsa_raw_recover,
    ecdsa_raw_sign,
    privtopub,
)

priv = binascii.unhexlify(
    "792eca682b890b31356247f2b04662bff448b6bb19ea1c8ab48da222c894ef9b"
)
pub = (
    20033694065814990006010338153307081985267967222430278129327181081381512401190,
    72089573118161052907088366229362685603474623289048716349537937839432544970413,
)


def test_privtopub():
    assert privtopub(priv) == pub


def test_ecdsa_raw_sign():
    v, r, s = ecdsa_raw_sign(b"\x35" * 32, priv)
    assert ecdsa_raw_recover(b"\x35" * 32, (v, r, s)) == pub


def test_issue_4_bug():
    unsigned_message = (
        "6a74f15f29c3227c5d1d2e27894da58d417a484ef53bc7aa57ee323b42ded656"
    )
    v = 28
    r = int("5897c2c7c7412b0a555fb6f053ddb6047c59666bbebc6f5573134e074992d841", 16)
    s = int("1c71d1c62b74caff8695a186e2a24dd701070ba9946748318135e3ac0950b1d4", 16)
    ecdsa_raw_recover(unsigned_message, (v, r, s))


SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Smallest r above N that is still the x coordinate of a curve point
R_ABOVE_N = SECP256K1_N + 2


def test_ecdsa_raw_recover_out_of_range_r_is_a_curve_point():
    # Sanity check for the test below: R_ABOVE_N passes the on-curve check,
    # so it can only be rejected by the range check.
    p = 2**256 - 2**32 - 977
    assert pow((R_ABOVE_N**3 + 7) % p, (p - 1) // 2, p) == 1


@pytest.mark.parametrize(
    "s_offset", (SECP256K1_N, 2 * SECP256K1_N, 2**256, -SECP256K1_N)
)
def test_ecdsa_raw_recover_rejects_s_out_of_range(s_offset):
    # s + k * N used to recover the same public key as s, because s was only
    # checked modulo N.
    msghash = b"\x35" * 32
    v, r, s = ecdsa_raw_sign(msghash, priv)
    assert ecdsa_raw_recover(msghash, (v, r, s)) == pub
    with pytest.raises(ValueError):
        ecdsa_raw_recover(msghash, (v, r, s + s_offset))


@pytest.mark.parametrize(
    "r, s",
    (
        (R_ABOVE_N, 5),
        (SECP256K1_N, 5),
        (-1, 5),
        (5, 0),
        (5, SECP256K1_N),
    ),
)
def test_ecdsa_raw_recover_rejects_r_or_s_out_of_range(r, s):
    with pytest.raises(ValueError):
        ecdsa_raw_recover(b"\x35" * 32, (27, r, s))
