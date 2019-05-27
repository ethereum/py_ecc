import argparse
import importlib
import secrets
import timeit


#
# Parse which module to benchmark
#
parser = argparse.ArgumentParser(
    description="Perform benchmark for the bls implementations",
)
parser.add_argument("module", help="which module you would like to test against", type=str)
args = parser.parse_args()
module_path = f"py_ecc.{args.module}.api"
api_module = importlib.import_module(module_path)

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
pubkeys = [api_module.privtopub(privkey) for privkey in privkeys]
signatures = [
    [api_module.sign(msg, privkey, domain) for privkey in privkeys]
    for msg in msgs
]
aggregate_multiple_sig = api_module.aggregate_signatures(
    [
        signature
        for msg_signatures in signatures
        for signature in msg_signatures
    ]
)
default_number_bench = 100


def bench(func, number=default_number_bench):
    setup = f"from __main__ import api_module, {func.__name__}"
    res = timeit.timeit(f"{func.__name__}()", setup=setup, number=number)
    print(f"{func.__name__}: {res}")


def privtopub():
    api_module.privtopub(privkeys[0])


def verify():
    api_module.verify(msgs[0], pubkeys[0], signatures[0][0], domain)


def aggregate_signatures():
    api_module.aggregate_signatures(signatures[0])


def aggregate_pubkeys():
    api_module.aggregate_pubkeys(pubkeys)


def verify_multiple():
    api_module.verify_multiple(
        pubkeys=pubkeys,
        message_hashes=msgs,
        signature=aggregate_multiple_sig,
        domain=domain,
    )


print(f"Module {module_path}")
bench(privtopub)
bench(verify)
bench(aggregate_signatures)
bench(aggregate_pubkeys)
bench(verify_multiple)
