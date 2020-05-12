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

DST = b'BLS12381G2_XMD:SHA-256_SSWU_RO_TESTGEN'


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
        FQ2([0x0a650bd36ae7455cb3fe5d8bb1310594551456f5c6593aec9ee0c03d2f6cb693bd2c5e99d4e23cbaec767609314f51d3, 0x0fbdae26f9f9586a46d4b0b70390d09064ef2afe5c99348438a3c7d9756471e015cb534204c1b6824617a85024c772dc]),
        FQ2([0x0d8d49e7737d8f9fc5cef7c4b8817633103faf2613016cb86a1f3fc29968fe2413e232d9208d2d74a89bf7a48ac36f83, 0x02e5cf8f9b7348428cc9e66b9a9b36fe45ba0b0a146290c3a68d92895b1af0e1f2d9f889fb412670ae8478d8abd4c5aa])),
        (b'abc',
        FQ2([0x1953ce6d4267939c7360756d9cca8eb34aac4633ef35369a7dc249445069888e7d1b3f9d2e75fbd468fbcbba7110ea02, 0x03578447618463deb106b60e609c6f7cc446dc6035f84a72801ba17c94cd800583b493b948eff0033f09086fdd7f6175]),
        FQ2([0x0882ab045b8fe4d7d557ebb59a63a35ac9f3d312581b509af0f8eaa2960cbc5e1e36bb969b6e22980b5cbdd0787fcf4e, 0x0184d26779ae9d4670aca9b267dbd4d3b30443ad05b8546d36a195686e1ccc3a59194aea05ed5bce7c3144a29ec047c4])),
        (b'abcdef0123456789',
        FQ2([0x17b461fc3b96a30c2408958cbfa5f5927b6063a8ad199d5ebf2d7cdeffa9c20c85487204804fab53f950b2f87db365aa, 0x195fad48982e186ce3c5c82133aefc9b26d55979b6f530992a8849d4263ec5d57f7a181553c8799bcc83da44847bdc8d]),
        FQ2([0x174a3473a3af2d0302b9065e895ca4adba4ece6ce0b41148ba597001abb152f852dd9a96fb45c9de0a43d944746f833e, 0x005cdf3d984e3391e7e969276fb4bc02323c5924a4449af167030d855acc2600cf3d4fab025432c6d868c79571a95bef])),
        (b'a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        FQ2([0x0a162306f3b0f2bb326f0c4fb0e1fea020019c3af796dcd1d7264f50ddae94cacf3cade74603834d44b9ab3d5d0a6c98, 0x123b6bd9feeba26dd4ad00f8bfda2718c9700dc093ea5287d7711844644eb981848316d3f3f57d5d3a652c6cdc816aca]),
        FQ2([0x15c1d4f1a685bb63ee67ca1fd96155e3d091e852a684b78d085fd34f6091e5249ddddbdcf2e7ec82ce6c04c63647eeb7, 0x05483f3b96d9252dd4fc0868344dfaf3c9d145e3387db23fa8e449304fab6a7b6ec9c15f05c0a1ea66ff0efcc03e001a])),
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
