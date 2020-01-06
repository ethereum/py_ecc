import pytest

from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    multiply,
    normalize,
)
from py_ecc.bls.g2_primatives import (
    subgroup_check,
    G2_to_signature,
    signature_to_G2,
    G1_to_pubkey,
    pubkey_to_G1,
)


def test_decompress_G2_with_no_modular_square_root_found():
    with pytest.raises(ValueError, match="Failed to find a modular squareroot"):
        signature_to_G2(b'\x11' * 96)


def test_G2_signature_encode_decode():
    G2_point = multiply(G2, 42)
    signature = G2_to_signature(G2_point)
    assert(normalize(signature_to_G2(signature)) == normalize(G2_point))


def test_G1_pubkey_encode_decode():
    G1_point = multiply(G1, 42)
    pubkey = G1_to_pubkey(G1_point)
    assert(normalize(pubkey_to_G1(pubkey)) == normalize(G1_point))
