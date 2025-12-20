import secrets
from time import time

from py_ecc.optimized_bls12_381 import (
    field_modulus as q,
    G1,
    G2,
    add,
    multiply,
    pairing,
)
from py_ecc import bls
import json


from eth_utils import encode_hex
from constants import (
    data_path,
    privkeys,
    domain,
    msg,
)


print("Gen pub keys")
pubkeys = [bls.privtopub(key) for key in privkeys]

print("Signing")
sigs = [bls.sign(message_hash=msg, privkey=key, domain=domain) for key in privkeys]
print("Agg sigs")
agg_sigs = bls.aggregate_signatures(sigs)
print("Agg keys")
agg_keys = bls.aggregate_pubkeys(pubkeys)


def convert(value):
    if isinstance(value, list) and isinstance(value[0], bytes):
        return [encode_hex(v) for v in value]
    elif isinstance(value, bytes):
        return encode_hex(value)
    else:
        return value


d = {
    "pubkeys": pubkeys,
    "sigs": sigs,
    "agg_sigs": agg_sigs,
    "agg_keys": agg_keys,
}
d_converted = {k: convert(v) for k, v in d.items()}

if __name__ == '__main__':
    with open(data_path, "w") as f:
        json.dump(d_converted, f, indent=4)
