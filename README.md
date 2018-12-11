py_ecc
==========================
Elliptic curve crypto in python including secp256k1 and alt_bn128

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/ethereum/py_ecc) ![Travis (.org) branch](https://img.shields.io/travis/ethereum/py_ecc/master.svg)[![PyPI version](https://badge.fury.io/py/py_ecc.svg)](https://badge.fury.io/py/py_ecc)


## Quickstart
```sh
pip install py_ecc
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
