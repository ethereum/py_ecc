import argparse
import secrets
import timeit

from py_ecc.bls_chia import api as bls_chia_api
from py_ecc.bls import api as pyecc_api


#
# Choose module to benchmark
#
parser = argparse.ArgumentParser(
    description="Perform benchmark for the bls implementations",
)
parser.add_argument("module", help="which module you would like to test against", type=str)
args = parser.parse_args()
if args.module == "py_ecc":
    module = pyecc_api
elif args.module == "chia":
    module = bls_chia_api
else:
    raise ValueError(f"{args.module} is not supported")


#
# Setup
#
num_keys = 20
privkeys = [
    # FIXME: should be 8*32, workaround errors with smaller privkeys
    secrets.randbits(7 * 32) for _ in range(num_keys)
]
msgs = [
    secrets.randbits(8 * 32).to_bytes(32, 'big') for _ in range(num_keys)
]
domain = 5566
pubkeys = [module.privtopub(privkey) for privkey in privkeys]
signatures = [
    [module.sign(msg, privkey, domain) for privkey in privkeys]
    for msg in msgs
]
aggregate_multiple_sig = module.aggregate_signatures(
    [
        signature
        for msg_signatures in signatures
        for signature in msg_signatures
    ]
)
default_number_bench = 100


def bench(func, number=default_number_bench):
    # stmt = f"{func.__name__}()".format(func.__name__)
    setup = f"from __main__ import bls_chia_api, pyecc_api, {func.__name__}"
    res = timeit.timeit(f"{func.__name__}()", setup=setup, number=number)
    print(f"{func.__name__}: {res}")


def privtopub():
    module.privtopub(privkeys[0])


def verify():
    module.verify(msgs[0], pubkeys[0], signatures[0][0], domain)


def aggregate_signatures():
    module.aggregate_signatures(signatures[0])


def aggregate_pubkeys():
    module.aggregate_pubkeys(pubkeys)


def verify_multiple():
    module.verify_multiple(
        pubkeys=pubkeys,
        message_hashes=msgs,
        signature=aggregate_multiple_sig,
        domain=domain,
    )


bench(privtopub)
bench(verify)
bench(aggregate_signatures)
bench(aggregate_pubkeys)
bench(verify_multiple)
