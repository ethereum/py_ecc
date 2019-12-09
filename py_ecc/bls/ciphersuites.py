from .hash_to_curve import (
    hash_to_G2,
)

ciphersuites = [
    'BLS_SIG_BLS12381G1-SHA256-SSWU-RO-_NUL_',
    'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_NUL_',
    'BLS_SIG_BLS12381G1-SHA256-SSWU-RO-_AUG_',
    'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_AUG_',
    'BLS_SIG_BLS12381G1-SHA256-SSWU-RO-_POP',
    'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP',
]

# Defaults: BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP
ciphersuite = 'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP'


def set_ciphersuite(new_ciphersuite: str):
    assert new_ciphersuite in ciphersuites
    ciphersuite = new_ciphersuite
    if 'G1' in ciphersuite:
        # TODO: Implement G1 hashing
        pass
    else:
        Sign = G2_sign
        Verify = G2_verify
