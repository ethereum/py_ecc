py_ecc v8.0.0-beta.1 (2024-10-22)
---------------------------------

Breaking Changes
~~~~~~~~~~~~~~~~

- Updated typing across the library (`#143 <https://github.com/ethereum/py_ecc/issues/143>`__)
- Set ``ecdsa_raw_recover`` to only accept ``v`` values of 27 or 28 (`#145 <https://github.com/ethereum/py_ecc/issues/145>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Add docstrings to ``secp256k1`` (`#141 <https://github.com/ethereum/py_ecc/issues/141>`__)


Features
~~~~~~~~

- Added ``__lt__`` to ``FQ`` classes (`#143 <https://github.com/ethereum/py_ecc/issues/143>`__)
- Add hash-to-curve functions for the G1 curve (`#146 <https://github.com/ethereum/py_ecc/issues/146>`__)


Internal Changes - for py_ecc Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Replace non-test instances of ``assert`` statments with better validation (`#142 <https://github.com/ethereum/py_ecc/issues/142>`__)


Performance Improvements
~~~~~~~~~~~~~~~~~~~~~~~~

- Lazy-load submodules to reduce initial import time (`#135 <https://github.com/ethereum/py_ecc/issues/135>`__)


py_ecc v7.0.1 (2024-04-23)
--------------------------

Internal Changes - for py_ecc Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Template updates, notably adding python 3.12 support (`#138 <https://github.com/ethereum/py_ecc/issues/138>`__)


Miscellaneous Changes
~~~~~~~~~~~~~~~~~~~~~

- `#139 <https://github.com/ethereum/py_ecc/issues/139>`__


py_ecc v7.0.0 (2023-12-06)
--------------------------

Breaking Changes
~~~~~~~~~~~~~~~~

- Drop support for python 3.6 and 3.7 (`#130 <https://github.com/ethereum/py_ecc/issues/130>`__)


Features
~~~~~~~~

- Add support for python 3.11 (`#130 <https://github.com/ethereum/py_ecc/issues/130>`__)


Internal Changes - for py_ecc Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Merge changes from python project template, including using pre-commit for linting and change the name of the ``master`` branch to ``main`` (`#130 <https://github.com/ethereum/py_ecc/issues/130>`__)


6.0.0
-----

2021-12-16

* Fix x1 point check (https://github.com/ethereum/py_ecc/pull/121)
* Bump eth-typing dependency requirement (https://github.com/ethereum/py_ecc/pull/123)
* Bump eth-utils dependency requirement (https://github.com/ethereum/py_ecc/pull/123)
* Drop support for Python 3.5 (https://github.com/ethereum/py_ecc/pull/123)
* Add support for Python 3.9 and 3.10 (https://github.com/ethereum/py_ecc/pull/123)


5.2.0
-----

2021-03-09

* Fix prime_field_inv edge case (https://github.com/ethereum/py_ecc/pull/114)
* Extract `subgroup_check` from `signature_to_G2` (https://github.com/ethereum/py_ecc/pull/116)
* Add G1 and G2 point value check (https://github.com/ethereum/py_ecc/pull/117)
* Fix README example (https://github.com/ethereum/py_ecc/pull/115)


5.1.0
-----

2020-11-16

* Fix BLS G1 and G2 deserialization https://github.com/ethereum/py_ecc/pull/110
* Fix to follow IETF BLS draft 04 point at infinity checking procedure https://github.com/ethereum/py_ecc/pull/107


5.0.0
-----

2020-10-01

* Implement IETF BLS draft 04 (https://github.com/ethereum/py_ecc/pull/103)


4.1.0
-----

2020-09-23

* Implement IETF BLS draft 03 (https://github.com/ethereum/py_ecc/pull/102)
* Optimize BLS-12-381: Miller loop is now 33% faster (https://github.com/ethereum/py_ecc/pull/100)
* Improve final exponentiation efficiency (https://github.com/ethereum/py_ecc/pull/101)


4.0.0
-----

2020-05-13

* Implement IETF hash-to-curve draft 07 (https://github.com/ethereum/py_ecc/pull/94)


3.1.0
-----

2020-05-12

* Fix optimized_swu + update error messages (https://github.com/ethereum/py_ecc/pull/97)


3.0.0
-----

2020-05-12

* Implement IETF BLS signature draft 02 + hash-to-curve draft 06 (https://github.com/ethereum/py_ecc/pull/87)
* Fixes Typing errors for points at infinity (NoneTypes) (https://github.com/ethereum/py_ecc/pull/89)

2.0.0
-----

2020-01-08

* Implement [IETF BLS signature draft 00](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-00)


1.7.1
-----

2019-07-12

* Introduce the `Domain` type as an alias for `bytes` of size 8 in BLS package.

1.7.0
-----

2019-05-23

* Update hash function for BLS Signatures https://github.com/ethereum/py_ecc/pull/70

1.6.0
-----

2019-03-14


* Add BLS Signature APIs https://github.com/ethereum/py_ecc/pull/52
* Maintenance: several refactors to reduce duplicated code
  * https://github.com/ethereum/py_ecc/pull/41
  * https://github.com/ethereum/py_ecc/pull/61
  * https://github.com/ethereum/py_ecc/pull/56
  * https://github.com/ethereum/py_ecc/pull/63

1.4.8
-----

2019-02-14

* Bugfix Optimized FQP curves to run modulus on integers during initialization
* Bugfix check against elliptic curve points at infinity
* Testing tool upgrades

1.4.2
-----

* Bugfix for `safe_ord` helper function.
