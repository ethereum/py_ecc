from typing import (
    cast,
)

from py_ecc.field_elements import (
    FQ,
    FQ2,
    FQ12,
)

from py_ecc.optimized_field_elements import (
    FQ as optimized_FQ,
    FQ2 as optimized_FQ2,
    FQ12 as optimized_FQ12,
)

from py_ecc.typing import (
    Point2D,
)


curve_properties = {
    "bn128": {
        # Order of the curve
        "curve_order": 21888242871839275222246405745257275088548364400416034343698204186575808495617,  # noqa: E501
        # Curve is y**2 = x**3 + 3
        "b": FQ(3, "bn128"),
        # Twisted curve over FQ**2
        "b2": FQ2([3, 0], "bn128") / FQ2([9, 1], "bn128"),
        # Extension curve over FQ**12; same b value as over FQ
        "b12": FQ12([3] + [0] * 11, "bn128"),
        # Generator for curve over FQ
        "G1": cast(Point2D[FQ], (FQ(1, "bn128"), FQ(2, "bn128"))),
        # Generator for twisted curve over FQ2
        "G2": (
            FQ2([
                10857046999023057135944570762232829481370756359578518086990519993285655852781,
                11559732032986387107991004021392285783925812861821192530917403151452391805634,
            ], "bn128"),
            FQ2([
                8495653923123431417604973247489272438418190587263600148770280649306958101930,
                4082367875863433681332203403145435568316851327593401208105741076214120093531,
            ], "bn128"),
        ),
        # Point at infinity over FQ
        "Z1": None,
        # Point at infinity for twisted curve over FQ2
        "Z2": None,
        "ate_loop_count": 29793968203157093288,
        "log_ate_loop_count": 63,
        "pseudo_binary_encoding": [
            0, 0, 0, 1, 0, 1, 0, -1, 0, 0, 1, -1, 0, 0, 1, 0,
            0, 1, 1, 0, -1, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 1,
            1, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 1,
            1, 0, 0, -1, 0, 0, 0, 1, 1, 0, -1, 0, 0, 1, 0, 1, 1,
        ],
    },
    "bls12_381": {
        # Order of the curve
        "curve_order": 52435875175126190479447740508185965837690552500527637822603658699938581184513,  # noqa: E501
        # Curve is y**2 = x**3 + 4
        "b": FQ(4, "bls12_381"),
        # Twisted curve over FQ**2
        "b2": FQ2((4, 4), "bls12_381"),
        # Extension curve over FQ**12; same b value as over FQ
        "b12": FQ12((4,) + (0,) * 11, "bls12_381"),
        # Generator for curve over FQ
        "G1": (
            FQ(3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507, "bls12_381"),  # noqa: E501
            FQ(1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569, "bls12_381"),  # noqa: E501
        ),
        # Generator for twisted curve over FQ2
        "G2": (
            FQ2([
                352701069587466618187139116011060144890029952792775240219908644239793785735715026873347600343865175952761926303160,  # noqa: E501
                3059144344244213709971259814753781636986470325476647558659373206291635324768958432433509563104347017837885763365758,  # noqa: E501
            ], "bls12_381"),
            FQ2([
                1985150602287291935568054521177171638300868978215655730859378665066344726373823718423869104263333984641494340347905,  # noqa: E501
                927553665492332455747201965776037880757740193453592970025027978793976877002675564980949289727957565575433344219582,  # noqa: E501
            ], "bls12_381"),
        ),
        # Point at infinity over FQ
        "Z1": None,
        # Point at infinity for twisted curve over FQ2
        "Z2": None,
        "ate_loop_count": 15132376222941642752,
        "log_ate_loop_count": 62,
        "pseudo_binary_encoding": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1
        ],
    },
}

optimized_curve_properties = {
    "bn128": {
        # Order of the curve
        "curve_order": 21888242871839275222246405745257275088548364400416034343698204186575808495617,  # noqa: E501
        # Curve is y**2 = x**3 + 3
        "b": optimized_FQ(3, "bn128"),
        # Twisted curve over FQ**2
        "b2": optimized_FQ2([3, 0], "bn128") / optimized_FQ2([9, 1], "bn128"),
        # Extension curve over FQ**12; same b value as over FQ
        "b12": optimized_FQ12([3] + [0] * 11, "bn128"),
        # Generator for curve over FQ (optimized version)
        "G1": (
            optimized_FQ(1, "bn128"),
            optimized_FQ(2, "bn128"),
            optimized_FQ(1, "bn128")
        ),
        # Generator for twisted curve over FQ2 (optimized version)
        "G2": (
            optimized_FQ2([
                10857046999023057135944570762232829481370756359578518086990519993285655852781,
                11559732032986387107991004021392285783925812861821192530917403151452391805634
            ], "bn128"),
            optimized_FQ2([
                8495653923123431417604973247489272438418190587263600148770280649306958101930,
                4082367875863433681332203403145435568316851327593401208105741076214120093531,
            ], "bn128"),
            optimized_FQ2.one("bn128"),
        ),
        # Point at infinity over FQ (optimized version)
        "Z1": (
            optimized_FQ.one("bn128"),
            optimized_FQ.one("bn128"),
            optimized_FQ.zero("bn128")
        ),
        # Point at infinity for twisted curve over FQ2 (optimized version)
        "Z2": (
            optimized_FQ2.one("bn128"),
            optimized_FQ2.one("bn128"),
            optimized_FQ2.zero("bn128")
        ),
        "ate_loop_count": 29793968203157093288,
        "log_ate_loop_count": 63,
        "pseudo_binary_encoding": [
            0, 0, 0, 1, 0, 1, 0, -1, 0, 0, 1, -1, 0, 0, 1, 0,
            0, 1, 1, 0, -1, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 1,
            1, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 1,
            1, 0, 0, -1, 0, 0, 0, 1, 1, 0, -1, 0, 0, 1, 0, 1, 1,
        ],
    },
    "bls12_381": {
        # Order of the curve
        "curve_order": 52435875175126190479447740508185965837690552500527637822603658699938581184513,  # noqa: E501
        # Curve is y**2 = x**3 + 4
        "b": optimized_FQ(4, "bls12_381"),
        # Twisted curve over FQ**2
        "b2": optimized_FQ2((4, 4), "bls12_381"),
        # Extension curve over FQ**12; same b value as over FQ
        "b12": optimized_FQ12((4,) + (0,) * 11, "bls12_381"),
        # Generator for curve over FQ (optimized version)
        "G1": (
            optimized_FQ(3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507, "bls12_381"),  # noqa: E501
            optimized_FQ(1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569, "bls12_381"),  # noqa: E501
            optimized_FQ(1, "bls12_381"),
        ),
        # Generator for twisted curve over FQ2 (optimized version)
        "G2": (
            optimized_FQ2((
                352701069587466618187139116011060144890029952792775240219908644239793785735715026873347600343865175952761926303160,  # noqa: E501
                3059144344244213709971259814753781636986470325476647558659373206291635324768958432433509563104347017837885763365758,  # noqa: E501
            ), "bls12_381"),
            optimized_FQ2((
                1985150602287291935568054521177171638300868978215655730859378665066344726373823718423869104263333984641494340347905,  # noqa: E501
                927553665492332455747201965776037880757740193453592970025027978793976877002675564980949289727957565575433344219582,  # noqa: E501
            ), "bls12_381"),
            optimized_FQ2.one("bls12_381"),
        ),
        # Point at infinity over FQ (optimized version)
        "Z1": (
            optimized_FQ.one("bls12_381"),
            optimized_FQ.one("bls12_381"),
            optimized_FQ.zero("bls12_381")
        ),
        # Point at infinity for twisted curve over FQ2 (optimized version)
        "Z2": (
            optimized_FQ2.one("bls12_381"),
            optimized_FQ2.one("bls12_381"),
            optimized_FQ2.zero("bls12_381")
        ),
        "ate_loop_count": 15132376222941642752,
        "log_ate_loop_count": 62,
        "pseudo_binary_encoding": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1
        ],
    },
}
