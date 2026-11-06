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


N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


@pytest.mark.parametrize(
    "bad_priv",
    (
        b"",
        b"\x00" * 32,
        N.to_bytes(32, "big"),
        (N + 1).to_bytes(32, "big"),
        b"\xff" * 32,
        b"\x01" + b"\x00" * 32,
    ),
    ids=("empty", "zero", "N", "N+1", "2**256-1", "2**256"),
)
def test_out_of_range_private_key_is_rejected(bad_priv):
    with pytest.raises(ValueError, match="private key"):
        privtopub(bad_priv)
    with pytest.raises(ValueError, match="private key"):
        ecdsa_raw_sign(b"\x35" * 32, bad_priv)


@pytest.mark.parametrize(
    "good_priv",
    (
        b"\x01",
        (1).to_bytes(32, "big"),
        (N - 1).to_bytes(32, "big"),
        b"\x00" + (N - 1).to_bytes(32, "big"),
    ),
    ids=("1-short", "1", "N-1", "N-1-33-bytes"),
)
def test_boundary_private_keys_are_accepted(good_priv):
    pub = privtopub(good_priv)
    v, r, s = ecdsa_raw_sign(b"\x35" * 32, good_priv)
    assert ecdsa_raw_recover(b"\x35" * 32, (v, r, s)) == pub
