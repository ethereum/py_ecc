"""
These are temporary tests to check the functionality of helper functions in `hash_to_G2`
They should be removed and replaced with a final version when hash to curve is complete.
"""
from eth_utils import (
    big_endian_to_int,
)
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
@pytest.mark.parametrize(
    'msg,x,y,H',
    [
        (b'',
        FQ2([0x0d3b02ee071b12d1e79138c3900ca3da7b8021ac462fe6ed68080dc9a5f1c5de46b7fe171e8b3e4e7537e7746757aeca, 0x0d4733459fead6a1f30e5f92df08ecfd0db9bcd0f3e2f2de0f00c8f45e081420aa4392eade61eade57d7a68474672fc1]),
        FQ2([0x09cc6f7b3074f0c82510e65d8fc58f6033e03ba7358005a13e2bbd7f429b080f29731ef08c3780c9e3c746578b96b05c, 0x0011531b8e08900a4f6f612e1e27432961419ce6a5ee3ec904a53588982d36ec4ea37be80b6cb7d986b38faec67dbe44]),
        lambda x: sha256(x).digest()),
        (b'abc',
        FQ2([0x0b6d276d0bfbddde617a9ab4c175b07c9c4aecad2cdd6cc9ca541b61334a69c58680ef5692bbad03d2f572838df32b66, 0x139e9d78ff6d9d163f979d14a64c5e57f82f1ef7e42ece338b571a9e92c0666f0f6bf1a5fc21e2d32bcb6432eab7037c]),
        FQ2([0x022f9ee5d596d06c5f2f735c3c5f743978f79fd57bf7d4291e221227f490d3f276066de9f9edc89c57e048ef4cf0ef72, 0x14dd23517516a80d1d840e34f51dfb76946c7670fca0f36ad8ec9bde4ea82dfae119a21b076519bcc1c00152989a4d45]),
        lambda x: sha256(x).digest()),
        (b'abcdef0123456789',
        FQ2([0x0ded52c30aace28d3e9cc5c1b47861ae4dd4e9cd17622e0f5b9d584af0397cd0e3bae80d4ee2d9d4b18c390f63154dfd, 0x046701a03f361a0b8392ca387585f7ee6534dcec9450a035e39dc37387d5ca079b9557447f7d9cad0bd9671cb65ada02]),
        FQ2([0x07a5cf56c5ea1d69ad59c0e80cc16c0c1b27f02840b396eb0ea320f70e87f705c6fa70cfeb9719b14badbb058bec5a4c, 0x0674d1f7c9e8e84d8d7a07b40231257571c43160fd566e8d24459d17ca52f6068e1b63aaae5359d8869d4abc66de66b6]),
        lambda x: sha256(x).digest()),
        (b'a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        FQ2([0x0161130ef4aa2f60f751e6b3dd48ac6e994d2d2613897c5dd26945bc72f33cc2977e1255c3f2dc0f1440d15a71c29b40, 0x06db1818f132a61f5fe86d315faa8de4653049ac9cf7fbbc6d9987e5864d82a0156259d56192109bafddd5c30b9f01f5]),
        FQ2([0x00f7fab0fedc978b974a38a1755244727b8a4eb31073653fa949594645ad181880d20ff0c91c4375b7e451fe803c9847, 0x0964d550ee8752b6db99555ffcd442b4185267f31e3d57435ea73896a7a9fe952bd67f90fd75f4413212ac9640a7672c]),
        lambda x: sha256(x).digest()),
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
