import secrets
from time import time

from py_ecc.optimized_bls12_381 import (
    field_modulus as q,
    G1,
    G2,
    add,
    multiply,
    pairing as _pairing,
)
from py_ecc import bls
from constants import (
    data_path,
    msg,
    domain,
    P_G1,
    P_G2,
    Q_G1,
    Q_G2,
)
import json
from eth_utils import (
    is_hex,
    decode_hex,
)
import timeit


def _is_hex(value):
    return isinstance(value, str) and is_hex(value)


def convert(value):
    if isinstance(value, list) and _is_hex(value[0]):
        return [decode_hex(v) for v in value]
    elif _is_hex(value):
        return decode_hex(value)
    else:
        return value


with open(data_path) as f:
    d = {k: convert(v) for k, v in json.load(f).items()}

pubkeys = d["pubkeys"]
sigs = d["sigs"]
agg_sigs = d["agg_sigs"]
agg_keys = d["agg_keys"]


def bench(func, seconds=2, repeat=3):
    stmt = "{0}()".format(func.__name__)
    setup = "from __main__ import {0}".format(func.__name__)
    timer = timeit.Timer(stmt, setup=setup)
    for _ in range(repeat):
        total_time = 0
        count = 0
        while total_time < seconds:
            total_time += timer.timeit(1)
            count += 1
        yield total_time / count, count


def report(func):
    results = "\t".join(
        "{0}\tsecs / {1}\ttimes".format(seconds, count)
        for seconds, count in bench(func)
    )
    print(func.__name__, "\t", results)


def adding_G1():
    return add(P_G1, Q_G1)


def adding_G2():
    return add(P_G2, Q_G2)


def pairing():
    return _pairing(P_G2, Q_G1, final_exponentiate=False)


def aggregate_keys():
    return bls.aggregate_pubkeys(pubkeys)


def aggregate_sigs():
    return bls.aggregate_signatures(sigs)


def bls_verify():
    return bls.verify(msg, agg_keys, agg_sigs, domain)


if __name__ == '__main__':
    report(adding_G1)
    report(adding_G2)
    report(pairing)
    report(aggregate_keys)
    report(aggregate_sigs)
    report(bls_verify)
