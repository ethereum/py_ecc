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

LARGE_NUMBER = 10000

N_VALIDATORS = 100
print("Gen priv keys")
privkeys = [secrets.randbelow(q) for i in range(N_VALIDATORS)]
print("Gen pub keys")
pubkeys = [bls.privtopub(key) for key in privkeys]
msg = b'ab'*32
domain = 5566
print("Signing")
sigs = [bls.sign(message_hash=msg, privkey=key, domain=domain) for key in privkeys]
print("Agg sigs")
agg_sigs = bls.aggregate_signatures(sigs)
print("Agg keys")
agg_keys = bls.aggregate_pubkeys(pubkeys)

P_G1 = multiply(G1, 100)
Q_G1 = multiply(G1, 5566)

P_G2 = multiply(G2, 100)
Q_G2 = multiply(G2, 5566)


def profile(fn):

    a = time()
    n_sample = fn()
    total_time = time() - a
    avg_time = total_time/n_sample
    print(f"{fn.__name__} avg {avg_time} seconds")


def adding_G1():
    for i in range(LARGE_NUMBER):
        add(P_G1, Q_G1)
    return LARGE_NUMBER


def adding_G2():
    for i in range(LARGE_NUMBER):
        add(P_G2, Q_G2)
    return LARGE_NUMBER


def _pairing():
    ln = int(LARGE_NUMBER/1000)
    for i in range(ln):
        pairing(P_G2, Q_G1, final_exponentiate=False)
    return ln

def aggregate_keys():
    agg_keys = bls.aggregate_pubkeys(pubkeys)
    return 1

def bls_verify():
    for i in range(10):
        bls.verify(msg, agg_keys, agg_sigs, domain)
    return 10

if __name__ == '__main__':
    profile(adding_G1)
    profile(adding_G2)
    profile(_pairing)
    profile(aggregate_keys)
    profile(bls_verify)
    # adding_G1 avg 3.800830841064453e-05 seconds
    # adding_G2 avg 0.00018580918312072753 seconds
    # _pairing avg 0.12307929992675781 seconds
    # aggregate_keys avg 0.041207075119018555 seconds
    # bls_verify avg 1.0701230764389038 seconds