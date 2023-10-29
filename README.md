# py_ecc

[![Join the conversation on Discord](https://img.shields.io/discord/809793915578089484?color=blue&label=chat&logo=discord&logoColor=white)](https://discord.gg/GHryRvPB84)
[![Build Status](https://circleci.com/gh/ethereum/py_ecc.svg?style=shield)](https://circleci.com/gh/ethereum/py_ecc)
[![PyPI version](https://badge.fury.io/py/py-ecc.svg)](https://badge.fury.io/py/py-ecc)
[![Python versions](https://img.shields.io/pypi/pyversions/py-ecc.svg)](https://pypi.python.org/pypi/py-ecc)

Elliptic curve crypto in python including secp256k1, alt_bn128, and bls12_381.

> **Warning**: This library contains some experimental codes that have **NOT** been audited.

Read more in the documentation below. [View the change log](https://github.com/ethereum/py_ecc/blob/main/CHANGELOG.rst)

## Quickstart

```sh
python -m pip install py_ecc
```

## BLS Signatures

`py_ecc` implements the [IETF BLS draft standard v4](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-04) as per the inter-blockchain standardization agreement. The BLS standards specify [different ciphersuites](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-04#section-4) which each have different functionality to accommodate various use cases. The following ciphersuites are available from this library:

- `G2Basic` also known as `BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_`
- `G2MessageAugmentation` also known as `BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_AUG_`
- `G2ProofOfPossession` also known as `BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_`

### Basic Usage

```python
from py_ecc.bls import G2ProofOfPossession as bls_pop

private_key = 5566
public_key = bls_pop.SkToPk(private_key)

message = b'\xab' * 32  # The message to be signed

# Signing
signature = bls_pop.Sign(private_key, message)

# Verifying
assert bls_pop.Verify(public_key, message, signature)
```

### Aggregating Signatures

```python
private_keys = [3, 14, 159]
public_keys = [bls_pop.SkToPk(key) for key in private_keys]
signatures = [bls_pop.Sign(key, message) for key in private_keys]

# Aggregating
agg_sig = bls_pop.Aggregate(signatures)

# Verifying signatures over the same message.
# Note this is only safe if Proofs of Possession have been verified for each of the public keys beforehand.
# See the BLS standards for why this is the case.
assert bls_pop.FastAggregateVerify(public_keys, message, agg_sig)
```

### Multiple Aggregation

```python
messages = [b'\xaa' * 42, b'\xbb' * 32, b'\xcc' * 64]
signatures = [bls_pop.Sign(key, message) for key, message in zip(private_keys, messages)]
agg_sig = bls_pop.Aggregate(signatures)

# Verify aggregate signature with different messages
assert bls_pop.AggregateVerify(public_keys, messages, agg_sig)
```

## Developer Setup

If you would like to hack on py_ecc, please check out the [Snake Charmers
Tactical Manual](https://github.com/ethereum/snake-charmers-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Documentation

We use [pre-commit](https://pre-commit.com/) to maintain consistent code style. Once
installed, it will run automatically with every commit. You can also run it manually
with `make lint`. If you need to make a commit that skips the `pre-commit` checks, you
can do so with `git commit --no-verify`.

### Development Environment Setup

You can set up your dev environment with:

```sh
git clone git@github.com:ethereum/py_ecc.git
cd py_ecc
virtualenv -p python3 venv
. venv/bin/activate
python -m pip install -e ".[dev]"
pre-commit install
```

### Release setup

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`. This is typically done from the
main branch, except when releasing a beta (in which case the beta is released from main,
and the previous stable branch is released from said branch).

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
