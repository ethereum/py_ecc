import pytest

from py_ecc.bls import (
    G2Basic,
    G2MessageAugmentation,
    G2ProofOfPossession,
)
from py_ecc.bls.g2_primitives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
)
from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    multiply,
    normalize,
)


def test_decompress_G2_with_no_modular_square_root_found():
    with pytest.raises(ValueError, match="Failed to find a modular squareroot"):
        signature_to_G2(b"\xA0" + b"\x11" * 95)


def test_G2_signature_encode_decode():
    G2_point = multiply(G2, 42)
    signature = G2_to_signature(G2_point)
    assert normalize(signature_to_G2(signature)) == normalize(G2_point)


def test_G1_pubkey_encode_decode():
    G1_point = multiply(G1, 42)
    pubkey = G1_to_pubkey(G1_point)
    assert normalize(pubkey_to_G1(pubkey)) == normalize(G1_point)


@pytest.mark.parametrize("prefix", [b"\x00", b"\x01", b"\xff\xff"])
def test_pubkey_to_G1_rejects_longer_encodings(prefix):
    pubkey = G1_to_pubkey(multiply(G1, 42))
    with pytest.raises(ValueError, match="Public key must be 48 bytes"):
        pubkey_to_G1(prefix + pubkey)


def test_pubkey_to_G1_rejects_shorter_encodings():
    pubkey = G1_to_pubkey(multiply(G1, 42))
    with pytest.raises(ValueError, match="Public key must be 48 bytes"):
        pubkey_to_G1(pubkey[:47])


@pytest.mark.parametrize(
    "transform",
    [
        lambda sig: b"\x00" + sig,
        lambda sig: sig[:48] + b"\x00" + sig[48:],
        lambda sig: sig[:95],
    ],
)
def test_signature_to_G2_rejects_other_lengths(transform):
    signature = G2_to_signature(multiply(G2, 42))
    with pytest.raises(ValueError, match="Signature must be 96 bytes"):
        signature_to_G2(transform(signature))


@pytest.mark.parametrize(
    "ciphersuite", [G2Basic, G2MessageAugmentation, G2ProofOfPossession]
)
@pytest.mark.parametrize("prefix", [b"\x00", b"\x01"])
def test_KeyValidate_rejects_longer_pubkeys(ciphersuite, prefix):
    pubkey = ciphersuite.SkToPk(42)
    assert ciphersuite.KeyValidate(pubkey)
    assert not ciphersuite.KeyValidate(prefix + pubkey)
