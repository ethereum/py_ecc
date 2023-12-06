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
