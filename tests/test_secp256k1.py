from py_ecc.secp256k1 import privtopub, ecdsa_raw_sign, ecdsa_raw_recover
import binascii

priv = binascii.unhexlify('792eca682b890b31356247f2b04662bff448b6bb19ea1c8ab48da222c894ef9b')
pub = (20033694065814990006010338153307081985267967222430278129327181081381512401190L, 72089573118161052907088366229362685603474623289048716349537937839432544970413L)

assert privtopub(priv) == pub
v, r, s = ecdsa_raw_sign(b'\x35' * 32, priv)
assert ecdsa_raw_recover(b'\x35' * 32, (v, r, s)) == pub
print('secp256k1 tests passed')
