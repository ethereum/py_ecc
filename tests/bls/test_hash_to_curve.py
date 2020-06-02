"""
These are temporary tests to check the functionality of helper functions in `hash_to_G2`
They should be removed and replaced with a final version when hash to curve is complete.
"""
import pytest
from hashlib import sha256

from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.bls.constants import (
    POW_2_381,
    POW_2_382,
    POW_2_383,
)
from py_ecc.fields import (
    optimized_bls12_381_FQ as FQ,
    optimized_bls12_381_FQ2 as FQ2,
    optimized_bls12_381_FQ12 as FQ12,
    optimized_bls12_381_FQP as FQP,
)
from py_ecc.optimized_bls12_381 import (
    G1,
    G2,
    Z1,
    Z2,
    b,
    b2,
    is_on_curve,
    multiply,
    normalize,
    field_modulus as q,
    iso_map_G2,
)

DST = b'QUUX-V01-CS02-with-BLS12381G2_XMD:SHA-256_SSWU_RO_'


@pytest.mark.parametrize(
    'iso_x,iso_y,iso_z,g2_x,g2_y',
    [
        (FQ2([int('0888F3832AD680917A71A1816C939290473474982C647B0B196BA0EDF62A0BC1A15D3E87CF6A287137B16C057E1AC808', 16), int('0B3D6E7A20275C100B460A900B23F2D8D5E9A53C3E59066E8D968D07AB0787940C0AC8A6C8C118FAD9068A2ECF00ADD7', 16)]),  # Iso-x0
        FQ2([int('08696DF8BAF8C488B7CFCA14CB984D0B78C998C3431E41700B493AAF921F779AA7F3660B1F5D6AC3BA4EBC85A1132CF3', 16), int('053003D3ED23019E585CF255A58634CEDA4C362B2E1D75E2AE85F4D1EF9C400786256D4AEE443DD1C900DD72E4089F73', 16)]),  # Iso-y0
        FQ2([int('108F7DF15439154BF32D7E4D1B6FEFC4BEF7C39A16AACA469D249770AD7B9F4AD3EA3CE58333A3194177C2D14B5CD2BC', 16), int('09E2E891E7A7AB58D5BF93864000ADBF0B6C31A8E35AB6AEC3B0820C2E536D6F0D170840B0AAFB470A9FD9B2F7DE3C27', 16)]),  # Iso-z0
        FQ2([int('168A912067A8F06CEB1F5F59DCEC69CE47F5A2B1696DFD5E67F1CF675587AD3A19831842D2543957BEE44FE29592996E', 16), int('116F36861307AA38251CAA73AA44FA359732DD92A15CDC70B21E3F7B2A332F73F86801789C469FE3FBB24DEB18AD5F0C', 16)]),  # G2-x0
        FQ2([int('0D4976CD99F4AD7204BC5983F6CE590766852DB93E5BE6CAB4C28591013E132BC6100D42022D5B66CE68A64A6B2A9C24', 16), int('0C6BA0E076144119F2B272718EC04C3FB037C9AA2C4074E64BE233AB27C0397BE175B9FDA277DCE8841669F787161AD2', 16)])),  # G2-y0
        (FQ2([int('039C33A34D97134F01D334F13C76BD5BB803B853BE4221A826026BFC93B5CA39E74B51A15D00BF88DF4F655915553027', 16), int('08DA2162E554A644AECC1F904F2B140D0296B7AC85B4EE59313DCEDE58B375C2E677160BC97CF8114361ABBE7D4672CD', 16)]),  # Iso-x1
        FQ2([int('1201968136C60428FB9DF8004C4915DC5E502D20D32F9DD87BC38163A52E2729289490030235E61EAEA098B0E8D63BF8', 16), int('116524863E40B6437BBAB965CDB84614F2346F1AD40300E9B15C3BDDE498E1FC1F76346452D3CF25553E2A3B89D9C5B1', 16)]),  # Iso-y1
        FQ2([int('08C3BCEBE1FC7F9987AE406A78C3FC898AE0C8A2FF0139A523E3CE91263EAA617519FC1A1158AF39BBA705316C9C2678', 16), int('0C9E92BB5509704DA0B6825A3AA36BA68A877875258F17C315FEA1527A82C7975E8439E91644616DABFD28E1DB43C1D9', 16)]),  # Iso-z1
        FQ2([int('1990072F0029639467E5C5EF9F65B31F194C31586D56141A7906DE6EE2B40803E06A301F9EEE9C8B04FA6AF8C5950F64', 16), int('0910709BEC8515357CB68AE88EA0B7EC6D54190773CC82EDDA68180D62BA214737DC708A5DA815E8B872D3C5B31E5A00', 16)]),  # G2-x1
        FQ2([int('12416C8B9159A047D5F92A6A4E941156E29E2A489B671D2FC3D8ED60FFA5F53FE846ECFB0090211197EF3BA4C07424F9', 16), int('089977D619CEA9D6D11F7148E1CB7622E46153BF1B4D81944603AA72AEFA6CE7CF07550CB6B582D17440F5949D1214FA', 16)])),  # G2-y1
    ]
)
def test_iso_map_G2(iso_x, iso_y, iso_z, g2_x, g2_y):
    (result_x, result_y, result_z) = iso_map_G2(iso_x, iso_y, iso_z)

    result_x = result_x / result_z
    result_y = result_y / result_z

    assert g2_x == result_x
    assert g2_y == result_y


# Tests taken from: https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/blob/master/draft-irtf-cfrg-hash-to-curve.md#bls12381g2_xmdsha-256_sswu_ro_
@pytest.mark.parametrize('H', [sha256])
@pytest.mark.parametrize(
    'msg,x,y',
    [
        (b'',
        FQ2([0x0141ebfbdca40eb85b87142e130ab689c673cf60f1a3e98d69335266f30d9b8d4ac44c1038e9dcdd5393faf5c41fb78a, 0x05cb8437535e20ecffaef7752baddf98034139c38452458baeefab379ba13dff5bf5dd71b72418717047f5b0f37da03d]),
        FQ2([0x0503921d7f6a12805e72940b963c0cf3471c7b2a524950ca195d11062ee75ec076daf2d4bc358c4b190c0c98064fdd92, 0x12424ac32561493f3fe3c260708a12b7c620e7be00099a974e259ddc7d1f6395c3c811cdd19f1e8dbf3e9ecfdcbab8d6])),
        (b'abc',
        FQ2([0x02c2d18e033b960562aae3cab37a27ce00d80ccd5ba4b7fe0e7a210245129dbec7780ccc7954725f4168aff2787776e6, 0x139cddbccdc5e91b9623efd38c49f81a6f83f175e80b06fc374de9eb4b41dfe4ca3a230ed250fbe3a2acf73a41177fd8]),
        FQ2([0x1787327b68159716a37440985269cf584bcb1e621d3a7202be6ea05c4cfe244aeb197642555a0645fb87bf7466b2ba48, 0x00aa65dae3c8d732d10ecd2c50f8a1baf3001578f71c694e03866e9f3d49ac1e1ce70dd94a733534f106d4cec0eddd16])),
        (b'abcdef0123456789',
        FQ2([0x121982811d2491fde9ba7ed31ef9ca474f0e1501297f68c298e9f4c0028add35aea8bb83d53c08cfc007c1e005723cd0, 0x190d119345b94fbd15497bcba94ecf7db2cbfd1e1fe7da034d26cbba169fb3968288b3fafb265f9ebd380512a71c3f2c]),
        FQ2([0x05571a0f8d3c08d094576981f4a3b8eda0a8e771fcdcc8ecceaf1356a6acf17574518acb506e435b639353c2e14827c8, 0x0bb5e7572275c567462d91807de765611490205a941a5a6af3b1691bfe596c31225d3aabdf15faff860cb4ef17c7c3be])),
        (b'a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        FQ2([0x01a6ba2f9a11fa5598b2d8ace0fbe0a0eacb65deceb476fbbcb64fd24557c2f4b18ecfc5663e54ae16a84f5ab7f62534, 0x11fca2ff525572795a801eed17eb12785887c7b63fb77a42be46ce4a34131d71f7a73e95fee3f812aea3de78b4d01569]),
        FQ2([0x0b6798718c8aed24bc19cb27f866f1c9effcdbf92397ad6448b5c9db90d2b9da6cbabf48adc1adf59a1a28344e79d57e, 0x03a47f8e6d1763ba0cad63d6114c0accbef65707825a511b251a660a9b3994249ae4e63fac38b23da0c398689ee2ab52])),
    ]
)
def test_hash_to_G2(msg, x, y, H):
    point = hash_to_G2(msg, DST, H)
    assert is_on_curve(point, b2)

    # Affine
    result_x = point[0] / point[2] # X / Z
    result_y = point[1] / point[2] # Y / Z

    assert x == result_x
    assert y == result_y

@pytest.mark.parametrize('degree', [
    (1),
    (2),
    (12),
])
@pytest.mark.parametrize('value, expected', [
    (0x00, 0),
    (0x10, 0),
    (0x01, 1),
])
def test_FQ_sgn0(degree, value, expected):
    if degree == 1:
        x = FQ(value)
    elif degree == 2:
        x = FQ2([value, 0])
    elif degree == 12:
        x = FQ12([value] + [0] * 11)

    assert x.sgn0 == expected
    if value != 0:
        assert x.sgn0 != (-x).sgn0


@pytest.mark.parametrize('value, expected', [
    ([0x00, 0x00], 0),
    ([0x10, 0x00], 0),
    ([0x01, 0x00], 1),
    ([0x01, 0x01], 1),
    ([0x10, 0x10], 0),
])
def test_FQ2_sgn0(value, expected):
    x = FQ2(value)
    y = FQP(value, modulus_coeffs=FQ2.FQ2_MODULUS_COEFFS)
    assert x.sgn0 == y.sgn0 == expected
