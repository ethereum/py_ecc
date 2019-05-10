from pathlib import Path
import os
from py_ecc.optimized_bls12_381 import (
    field_modulus as q,
    G1,
    G2,
    add,
    multiply,
    pairing,
)
import secrets


data_path = Path(os.path.dirname(__file__)) / "fixtures" / "data.json"


N_VALIDATORS = 100
privkeys = [secrets.randbelow(q) for i in range(N_VALIDATORS)]

msg = b'\xab'*32
domain = 5566
P_G1 = multiply(G1, 100)
Q_G1 = multiply(G1, 5566)

P_G2 = multiply(G2, 100)
Q_G2 = multiply(G2, 5566)
