from typing import (
    Iterable,
    Tuple,
)
from math import (
    ceil,
    log2,
)
from abc import (
    ABC,
    abstractproperty,
)
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    big_endian_to_int,
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
)
from .hash_to_curve import hash_to_G2
from .g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
)


class BaseG2Ciphersuite(ABC):
    @abstractproperty
    def DST(self):
        pass

    @staticmethod
    def PrivToPub(privkey: int) -> BLSPubkey:
        return G1_to_pubkey(multiply(G1, privkey))

    @staticmethod
    def KeyGen(IKM: bytes) -> Tuple[BLSPubkey, int]:
        prk = hkdf_extract(b'BLS-SIG-KEYGEN-SALT-', IKM)
        l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
        okm = hkdf_expand(prk, b'', l)
        x = big_endian_to_int(okm) % curve_order
        return (BaseG2Ciphersuite.PrivToPub(x), x)

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
    def Aggregate(signatures: Iterable[BLSSignature]) -> BLSSignature:
        accumulator = Z2  # Seed with the point at infinity
        for signature in signatures:
            signature_point = signature_to_G2(signature)
            accumulator = add(accumulator, signature_point)
        return G2_to_signature(accumulator)

    @staticmethod
    def _CoreAggregateVerify(pairs: Iterable[Tuple[BLSPubkey, bytes]],
                             signature: BLSSignature, DST: bytes) -> bool:
        try:
            signature_point = signature_to_G2(signature)
            accumulator = FQ12([1] + [0] * 11)
            for pk, message in pairs:
                pubkey_point = pubkey_to_G1(pk)
                message_point = hash_to_G2(message, DST)
                accumulator *= pairing(message_point, pubkey_point, final_exponentiate=False)
            accumulator *= pairing(signature_point, neg(G1), final_exponentiate=False)
            return final_exponentiate(accumulator) == FQ12.one()

        except (ValidationError, ValueError, AssertionError):
            return False

    def Sign(self, SK: int, message: bytes) -> BLSSignature:
        return self._CoreSign(SK, message, self.DST)

    def Verify(self, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return self._CoreVerify(PK, message, signature, self.DST)

    def AggregateVerify(self, pairs: Iterable[Tuple[BLSPubkey, bytes]],
                        signature: BLSSignature) -> bool:
        pass


class G2Basic(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_NUL_'

    def AggregateVerify(self, pairs: Iterable[Tuple[BLSPubkey, bytes]],
                        signature: BLSSignature) -> bool:
        pairs = list(pairs)
        _, messages = zip(*pairs)
        if len(messages) != len(set(messages)):  # Messages are not unique
            return False
        return self._CoreAggregateVerify(pairs, signature, self.DST)


class G2MessageAugmentation(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_AUG_'

    def Sign(self, SK: int, message: bytes) -> BLSSignature:
        PK = self.PrivToPub(SK)
        return self._CoreSign(SK, PK + message, self.DST)

    def Verify(self, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return self._CoreVerify(PK, PK + message, signature, self.DST)

    def AggregateVerify(self, pairs: Iterable[Tuple[BLSPubkey, bytes]],
                        signature: BLSSignature) -> bool:
        pairs = list(pairs)
        pairs = [(pk, pk + msg) for pk, msg in pairs]
        return self._CoreAggregateVerify(pairs, signature, self.DST)


class G2PoP(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2-SHA256-SSWU-RO-_POP_'

    def AggregateVerify(self, pairs: Iterable[Tuple[BLSPubkey, bytes]],
                        signature: BLSSignature) -> bool:
        return self._CoreAggregateVerify(pairs, signature, self.DST)

    def PopProve(self, SK: int) -> BLSSignature:
        pubkey = self.PrivToPub(SK)
        return self._CoreSign(SK, pubkey, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')

    def PopVerify(self, PK: BLSPubkey, proof: BLSSignature) -> bool:
        return self._CoreVerify(PK, PK, proof, b'BLS_POP_BLS12381G2-SHA256-SSWU-RO-_POP_')

    @staticmethod
    def _AggregatePKs(PKs: Iterable[BLSPubkey]) -> BLSPubkey:
        accumulator = Z1  # Seed with the point at infinity
        for pk in PKs:
            pubkey_point = pubkey_to_G1(pk)
            accumulator = add(accumulator, pubkey_point)
        return G1_to_pubkey(accumulator)

    def FastAggregateVerify(self, PKs: Iterable[BLSPubkey],
                            message: bytes, signature: BLSSignature) -> bool:
        aggregate_pubkey = self._AggregatePKs(PKs)
        return self.Verify(aggregate_pubkey, message, signature)
