from typing import (
    Dict,
    Tuple,
)

from mypy_extensions import TypedDict


Curve_Field_Properties = TypedDict('Curve_Field_Properties',
                                   {
                                       'field_modulus': int,
                                       'fq2_modulus_coeffs': Tuple[int, ...],
                                       'fq12_modulus_coeffs': Tuple[int, ...],
                                   })
Field_Properties = Dict[str, Curve_Field_Properties]

field_properties = {
    "bn128": {
        "field_modulus": 21888242871839275222246405745257275088696311157297823662689037894645226208583,  # noqa: E501
        "fq2_modulus_coeffs": (1, 0),
        "fq12_modulus_coeffs": (82, 0, 0, 0, 0, 0, -18, 0, 0, 0, 0, 0),  # Implied + [1]
    },
    "bls12_381": {
        "field_modulus": 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787,  # noqa: E501
        "fq2_modulus_coeffs": (1, 0),
        "fq12_modulus_coeffs": (2, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0),  # Implied + [1]
    },
}   # type: Field_Properties
