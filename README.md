py_ecc
==========================
Elliptic curve crypto in python including secp256k1 and alt_bn128

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/ethereum/py_ecc) [![Build Status](https://circleci.com/gh/ethereum/py_ecc.svg?style=shield)](https://circleci.com/gh/ethereum/py_ecc) [![PyPI version](https://badge.fury.io/py/py-ecc.svg)](https://badge.fury.io/py/py-ecc)


## Quickstart
```sh
pip install py_ecc
```

## BLS Signatures

```python
from py_ecc import bls

private_key = 5566
public_key = bls.PrivToPub(private_key)

# Hash your message to 32 bytes
message_hash = b'\xab' * 32

# Signing
signature = bls.Sign(message_hash, private_key)

# Verifying
assert bls.Verify(message_hash, public_key, signature)
```

### Aggregating Signatures and Public Keys

```python
private_keys = [3, 14, 159]
public_keys = [bls.PrivToPub(key) for key in private_keys]
signatures = [bls.Sign(message_hash, key) for key in private_keys]

# Aggregating
agg_sig = bls.AggregateSignatures(signatures)
agg_pub = bls.AggregatePubkeys(public_keys)

# Verifying
assert bls.Verify(message_hash, agg_pub, agg_sig)
```

### Multiple Aggregation

```python
message_hash_1, message_hash_2 = b'\xaa' * 32, b'\xbb' * 32

msg_hashes = [message_hash_1, message_hash_2]
agg_pubs = [agg_pub_1, agg_pub_2]
agg_agg_sig = bls.AggregateSignatures([agg_sig_1, agg_sig_2])

assert bls.VerifyMultiple(agg_pubs, msg_hashes, agg_agg_sig)
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
