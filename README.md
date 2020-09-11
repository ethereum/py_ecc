py_ecc
==========================
Elliptic curve crypto in python including secp256k1 and alt_bn128

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/ethereum/py_ecc) [![Build Status](https://circleci.com/gh/ethereum/py_ecc.svg?style=shield)](https://circleci.com/gh/ethereum/py_ecc) [![PyPI version](https://badge.fury.io/py/py-ecc.svg)](https://badge.fury.io/py/py-ecc)

## Quickstart

```sh
pip install py_ecc
```

## BLS Signatures

`py_ecc` implements the [IETF BLS draft standard v3](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-03) as per the inter-blockchain standardization agreement. The BLS standards specify [different ciphersuites](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-03#section-4) which each have different functionality to accommodate various use cases. The following ciphersuites are available from this library:

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
assert bls_pop.AggregateVerify(zip(public_keys, messages), agg_sig)
```

## Developer Setup

If you would like to hack on py_ecc, please check out the [Ethereum Development Tactical Manual](https://github.com/ethereum/ethereum-dev-tactical-manual) for information on how we do:

- Testing
- Pull Requests
- Code Style
- Documentation

## Got bug?

Feel free to create issue under https://github.com/ethereum/py_ecc/issues

## Copyright and Licensing

Project is licensed under the MIT license.

## Release setup

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
