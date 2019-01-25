from .field_elements import (
    FQ,
    FQP,
    FQ2,
    FQ12,
)

from .optimized_field_elements import (
    FQ as optimized_FQ,
    FQP as optimized_FQP,
    FQ2 as optimized_FQ2,
    FQ12 as optimized_FQ12,
)


# Create seperate classes for all Fields for each curve

bn128_FQ = type("bn128_FQ", (FQ,), {'curve_name': "bn128"})
bn128_FQP = type("bn128_FQP", (FQP,), {'curve_name': "bn128"})
bn128_FQ2 = type("bn128_FQ2", (FQ2,), {'curve_name': "bn128"})
bn128_FQ12 = type("bn128_FQ12", (FQ12,), {'curve_name': "bn128"})

bls12_381_FQ = type("bls12_381_FQ", (FQ,), {'curve_name': "bls12_381"})
bls12_381_FQP = type("bls12_381_FQP", (FQP,), {'curve_name': "bls12_381"})
bls12_381_FQ2 = type("bls12_381_FQ2", (FQ2,), {'curve_name': "bls12_381"})
bls12_381_FQ12 = type("bls12_381_FQ12", (FQ12,), {'curve_name': "bls12_381"})

optimized_bn128_FQ = type(
    "optimized_bn128_FQ",
    (optimized_FQ,),
    {'curve_name': "bn128"}
)
optimized_bn128_FQP = type(
    "optimized_bn128_FQP",
    (optimized_FQP,),
    {'curve_name': "bn128"}
)
optimized_bn128_FQ2 = type(
    "optimized_bn128_FQ2",
    (optimized_FQ2,),
    {'curve_name': "bn128"}
)
optimized_bn128_FQ12 = type(
    "optimized_bn128_FQ12",
    (optimized_FQ12,),
    {'curve_name': "bn128"}
)

optimized_bls12_381_FQ = type(
    "optimized_bls12_381_FQ",
    (optimized_FQ,),
    {'curve_name': "bls12_381"}
)
optimized_bls12_381_FQP = type(
    "optimized_bls12_381_FQP",
    (optimized_FQP,),
    {'curve_name': "bls12_381"}
)
optimized_bls12_381_FQ2 = type(
    "optimized_bls12_381_FQ2",
    (optimized_FQ2,),
    {'curve_name': "bls12_381"}
)
optimized_bls12_381_FQ12 = type(
    "optimized_bls12_381_FQ12",
    (optimized_FQ12,),
    {'curve_name': "bls12_381"}
)
