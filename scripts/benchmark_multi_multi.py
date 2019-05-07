from random import sample
from py_ecc.bls import (
    aggregate_pubkeys,
    aggregate_signatures,
    sign,
    privtopub,
    verify_multiple,
    verify_multiple_multiple,
)
import time

domain = 0
validator_indices = tuple(range(1000))
privkeys = tuple(2**i for i in validator_indices)
pubkeys = [privtopub(k) for k in privkeys]

MAX_ATTESTATIONS = 128
TARGET_COMMITTEE_SIZE = 128


class Attestation:
    def __init__(self, msg_1, msg_2):
        msg_1_validators = sample(validator_indices, TARGET_COMMITTEE_SIZE//2)
        msg_2_validators = sample(validator_indices, TARGET_COMMITTEE_SIZE//2)
        self.agg_pubkeys = [
            aggregate_pubkeys([pubkeys[i] for i in msg_1_validators]),
            aggregate_pubkeys([pubkeys[i] for i in msg_2_validators]),
        ]
        self.msgs = [msg_1, msg_2]
        msg_1_sigs = [sign(msg_1, privkeys[i], domain) for i in msg_1_validators]
        msg_2_sigs = [sign(msg_2, privkeys[i], domain) for i in msg_2_validators]
        self.sig = aggregate_signatures([
            aggregate_signatures(msg_1_sigs),
            aggregate_signatures(msg_2_sigs),
        ])


att = Attestation(b'\x12' * 32, b'\x34' * 32)
atts = (att,) * MAX_ATTESTATIONS


def profile_verify_multiple():
    t = time.time()
    for att in atts:
        assert verify_multiple(
            pubkeys=att.agg_pubkeys,
            message_hashes=att.msgs,
            signature=att.sig,
            domain=domain,
        )
    print(time.time() - t)


def profile_verify_multiple_multiple():
    t = time.time()
    assert verify_multiple_multiple(
        signatures=[att.sig for att in atts],
        pubkeys_and_messages=[[att.agg_pubkeys, att.msgs] for att in atts],
        domain=domain,
    )
    print(time.time() - t)


if __name__ == '__main__':
    print("profile_verify_multiple")
    profile_verify_multiple()
    print("profile_verify_multiple_multiple")
    profile_verify_multiple_multiple()
