from typing import (
    Sequence,
)
from math import (
    ceil,
    log2,
)
import abc
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    ValidationError,
)

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
)

from .hash import (
    hkdf_expand,
    hkdf_extract,
    i2osp,
    os2ip,
)
from .hash_to_curve import hash_to_G2
from .g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
)


class BaseG2Ciphersuite(abc.ABC):
    DST = b''

    @staticmethod
    def SkToPk(privkey: int) -> BLSPubkey:
        return G1_to_pubkey(multiply(G1, privkey))

    @staticmethod
    def KeyGen(IKM: bytes, key_info: bytes = b'') -> int:
        prk = hkdf_extract(b'BLS-SIG-KEYGEN-SALT-', IKM + b'\x00')
        l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
        okm = hkdf_expand(prk, key_info + i2osp(l, 2), l)
        x = os2ip(okm) % curve_order
        return x

    @staticmethod
    def KeyValidate(PK: BLSPubkey) -> bool:
        try:
            pubkey_to_G1(PK)
        except ValidationError:
            return False
        return True

    @staticmethod
    def _CoreSign(SK: int, message: bytes, DST: bytes) -> BLSSignature:
        message_point = hash_to_G2(message, DST)
        signature_point = multiply(message_point, SK)
        return G2_to_signature(signature_point)

    @staticmethod
    def _CoreVerify(PK: BLSPubkey, message: bytes, signature: BLSSignature, DST: bytes) -> bool:
        try:
            assert BaseG2Ciphersuite.KeyValidate(PK)
            signature_point = signature_to_G2(signature)
            final_exponentiation = final_exponentiate(
                pairing(
                    signature_point,
                    G1,
                    final_exponentiate=False,
                ) * pairing(
                    hash_to_G2(message, DST),
                    neg(pubkey_to_G1(PK)),
                    final_exponentiate=False,
                )
            )
            return final_exponentiation == FQ12.one()
        except (ValidationError, ValueError, AssertionError):
            return False

    @staticmethod
    def Aggregate(signatures: Sequence[BLSSignature]) -> BLSSignature:
        accumulator = Z2  # Seed with the point at infinity
        for signature in signatures:
            signature_point = signature_to_G2(signature)
            accumulator = add(accumulator, signature_point)
        return G2_to_signature(accumulator)

    @staticmethod
    def _CoreAggregateVerify(PKs: Sequence[BLSPubkey], messages: Sequence[bytes],
                             signature: BLSSignature, DST: bytes) -> bool:
        try:
            signature_point = signature_to_G2(signature)
            accumulator = FQ12.one()
            for pk, message in zip(PKs, messages):
                pubkey_point = pubkey_to_G1(pk)
                message_point = hash_to_G2(message, DST)
                accumulator *= pairing(message_point, pubkey_point, final_exponentiate=False)
            accumulator *= pairing(signature_point, neg(G1), final_exponentiate=False)
            return final_exponentiate(accumulator) == FQ12.one()

        except (ValidationError, ValueError, AssertionError):
            return False

    @classmethod
    def Sign(cls, SK: int, message: bytes) -> BLSSignature:
        return cls._CoreSign(SK, message, cls.DST)

    @classmethod
    def Verify(cls, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return cls._CoreVerify(PK, message, signature, cls.DST)

    @abc.abstractclassmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        ...


class G2Basic(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_'

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        if len(messages) != len(set(messages)):  # Messages are not unique
            return False
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)


class G2MessageAugmentation(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_AUG_'

    @classmethod
    def Sign(cls, SK: int, message: bytes) -> BLSSignature:
        PK = cls.SkToPk(SK)
        return cls._CoreSign(SK, PK + message, cls.DST)

    @classmethod
    def Verify(cls, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return cls._CoreVerify(PK, PK + message, signature, cls.DST)

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        messages = [pk + msg for pk, msg in zip(PKs, messages)]
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)


class G2ProofOfPossession(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_'
    POP_TAG = b'BLS_POP_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_'

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)

    @classmethod
    def PopProve(cls, SK: int) -> BLSSignature:
        pubkey = cls.SkToPk(SK)
        return cls._CoreSign(SK, pubkey, cls.POP_TAG)

    @classmethod
    def PopVerify(cls, PK: BLSPubkey, proof: BLSSignature) -> bool:
        return cls._CoreVerify(PK, PK, proof, cls.POP_TAG)

    @staticmethod
    def _AggregatePKs(PKs: Sequence[BLSPubkey]) -> BLSPubkey:
        accumulator = Z1  # Seed with the point at infinity
        for pk in PKs:
            pubkey_point = pubkey_to_G1(pk)
            accumulator = add(accumulator, pubkey_point)
        return G1_to_pubkey(accumulator)

    @classmethod
    def FastAggregateVerify(cls, PKs: Sequence[BLSPubkey],
                            message: bytes, signature: BLSSignature) -> bool:
        aggregate_pubkey = cls._AggregatePKs(PKs)
        return cls.Verify(aggregate_pubkey, message, signature)
