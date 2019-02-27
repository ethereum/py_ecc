from .field_elements import (
    FQ,
    FQP,
    FQ2,
    FQ12,
)

from .field_properties import (
    field_properties,
)

from .optimized_field_elements import (
    FQ as optimized_FQ,
    FQP as optimized_FQP,
    FQ2 as optimized_FQ2,
    FQ12 as optimized_FQ12,
)


# Create seperate classes for all Fields for each curve

bn128_FQ = type(
    "bn128_FQ",
    (FQ,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
    }
)
bn128_FQP = type(
    "bn128_FQP",
    (FQP,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
    }
)
bn128_FQ2 = type(
    "bn128_FQ2",
    (FQ2,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
        'FQ2_MODULUS_COEFFS': field_properties["bn128"]["fq2_modulus_coeffs"],
    }
)
bn128_FQ12 = type(
    "bn128_FQ12",
    (FQ12,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
        'FQ12_MODULUS_COEFFS': field_properties["bn128"]["fq12_modulus_coeffs"],
    }
)

bls12_381_FQ = type(
    "bls12_381_FQ",
    (FQ,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
    }
)
bls12_381_FQP = type(
    "bls12_381_FQP",
    (FQP,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
    }
)
bls12_381_FQ2 = type(
    "bls12_381_FQ2",
    (FQ2,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
        'FQ2_MODULUS_COEFFS': field_properties["bls12_381"]["fq2_modulus_coeffs"],
    }
)
bls12_381_FQ12 = type(
    "bls12_381_FQ12",
    (FQ12,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
        'FQ12_MODULUS_COEFFS': field_properties["bls12_381"]["fq12_modulus_coeffs"],
    }
)

optimized_bn128_FQ = type(
    "optimized_bn128_FQ",
    (optimized_FQ,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
    }
)
optimized_bn128_FQP = type(
    "optimized_bn128_FQP",
    (optimized_FQP,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
    }
)
optimized_bn128_FQ2 = type(
    "optimized_bn128_FQ2",
    (optimized_FQ2,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
        'FQ2_MODULUS_COEFFS': field_properties["bn128"]["fq2_modulus_coeffs"],
    }
)
optimized_bn128_FQ12 = type(
    "optimized_bn128_FQ12",
    (optimized_FQ12,),
    {
        'curve_name': "bn128",
        'field_modulus': field_properties["bn128"]["field_modulus"],
        'FQ12_MODULUS_COEFFS': field_properties["bn128"]["fq12_modulus_coeffs"],
    }
)

optimized_bls12_381_FQ = type(
    "optimized_bls12_381_FQ",
    (optimized_FQ,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
    }
)
optimized_bls12_381_FQP = type(
    "optimized_bls12_381_FQP",
    (optimized_FQP,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
    }
)
optimized_bls12_381_FQ2 = type(
    "optimized_bls12_381_FQ2",
    (optimized_FQ2,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
        'FQ2_MODULUS_COEFFS': field_properties["bls12_381"]["fq2_modulus_coeffs"],
    }
)
optimized_bls12_381_FQ12 = type(
    "optimized_bls12_381_FQ12",
    (optimized_FQ12,),
    {
        'curve_name': "bls12_381",
        'field_modulus': field_properties["bls12_381"]["field_modulus"],
        'FQ12_MODULUS_COEFFS': field_properties["bls12_381"]["fq12_modulus_coeffs"],
    }
)
