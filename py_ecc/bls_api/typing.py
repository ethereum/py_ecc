# This module will not be included in the PR.
# These types should be replaced with those in eth-typing

from typing import (
    NewType,
)

Hash32 = NewType("Hash32", bytes)
BLSPubkey = NewType('BLSPubkey', bytes)  # bytes48
BLSSignature = NewType('BLSSignature', bytes)  # bytes96
