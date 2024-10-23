"""
These are temporary tests to check the functionality of helper functions in `hash_to_G2`
They should be removed and replaced with a final version when hash to curve is complete.
"""
import pytest
from hashlib import (
    sha256,
)

from py_ecc.bls.hash_to_curve import (
    hash_to_G1,
    hash_to_G2,
)
from py_ecc.fields import (
    optimized_bls12_381_FQ as FQ,
    optimized_bls12_381_FQ2 as FQ2,
    optimized_bls12_381_FQ12 as FQ12,
    optimized_bls12_381_FQP as FQP,
)
from py_ecc.optimized_bls12_381 import (
    b,
    b2,
    is_on_curve,
    iso_map_G2,
)

DST_G1 = b"QUUX-V01-CS02-with-BLS12381G1_XMD:SHA-256_SSWU_RO_"
DST_G2 = b"QUUX-V01-CS02-with-BLS12381G2_XMD:SHA-256_SSWU_RO_"


@pytest.mark.parametrize(
    "iso_x,iso_y,iso_z,g2_x,g2_y",
    [
        (
            FQ2(
                [
                    int(
                        "0888F3832AD680917A71A1816C939290473474982C647B0B196BA0EDF62A0BC1A15D3E87CF6A287137B16C057E1AC808",  # noqa: E501
                        16,
                    ),
                    int(
                        "0B3D6E7A20275C100B460A900B23F2D8D5E9A53C3E59066E8D968D07AB0787940C0AC8A6C8C118FAD9068A2ECF00ADD7",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-x0
            FQ2(
                [
                    int(
                        "08696DF8BAF8C488B7CFCA14CB984D0B78C998C3431E41700B493AAF921F779AA7F3660B1F5D6AC3BA4EBC85A1132CF3",  # noqa: E501
                        16,
                    ),
                    int(
                        "053003D3ED23019E585CF255A58634CEDA4C362B2E1D75E2AE85F4D1EF9C400786256D4AEE443DD1C900DD72E4089F73",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-y0
            FQ2(
                [
                    int(
                        "108F7DF15439154BF32D7E4D1B6FEFC4BEF7C39A16AACA469D249770AD7B9F4AD3EA3CE58333A3194177C2D14B5CD2BC",  # noqa: E501
                        16,
                    ),
                    int(
                        "09E2E891E7A7AB58D5BF93864000ADBF0B6C31A8E35AB6AEC3B0820C2E536D6F0D170840B0AAFB470A9FD9B2F7DE3C27",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-z0
            FQ2(
                [
                    int(
                        "168A912067A8F06CEB1F5F59DCEC69CE47F5A2B1696DFD5E67F1CF675587AD3A19831842D2543957BEE44FE29592996E",  # noqa: E501
                        16,
                    ),
                    int(
                        "116F36861307AA38251CAA73AA44FA359732DD92A15CDC70B21E3F7B2A332F73F86801789C469FE3FBB24DEB18AD5F0C",  # noqa: E501
                        16,
                    ),
                ]
            ),  # G2-x0
            FQ2(
                [
                    int(
                        "0D4976CD99F4AD7204BC5983F6CE590766852DB93E5BE6CAB4C28591013E132BC6100D42022D5B66CE68A64A6B2A9C24",  # noqa: E501
                        16,
                    ),
                    int(
                        "0C6BA0E076144119F2B272718EC04C3FB037C9AA2C4074E64BE233AB27C0397BE175B9FDA277DCE8841669F787161AD2",  # noqa: E501
                        16,
                    ),
                ]
            ),
        ),  # G2-y0
        (
            FQ2(
                [
                    int(
                        "039C33A34D97134F01D334F13C76BD5BB803B853BE4221A826026BFC93B5CA39E74B51A15D00BF88DF4F655915553027",  # noqa: E501
                        16,
                    ),
                    int(
                        "08DA2162E554A644AECC1F904F2B140D0296B7AC85B4EE59313DCEDE58B375C2E677160BC97CF8114361ABBE7D4672CD",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-x1
            FQ2(
                [
                    int(
                        "1201968136C60428FB9DF8004C4915DC5E502D20D32F9DD87BC38163A52E2729289490030235E61EAEA098B0E8D63BF8",  # noqa: E501
                        16,
                    ),
                    int(
                        "116524863E40B6437BBAB965CDB84614F2346F1AD40300E9B15C3BDDE498E1FC1F76346452D3CF25553E2A3B89D9C5B1",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-y1
            FQ2(
                [
                    int(
                        "08C3BCEBE1FC7F9987AE406A78C3FC898AE0C8A2FF0139A523E3CE91263EAA617519FC1A1158AF39BBA705316C9C2678",  # noqa: E501
                        16,
                    ),
                    int(
                        "0C9E92BB5509704DA0B6825A3AA36BA68A877875258F17C315FEA1527A82C7975E8439E91644616DABFD28E1DB43C1D9",  # noqa: E501
                        16,
                    ),
                ]
            ),  # Iso-z1
            FQ2(
                [
                    int(
                        "1990072F0029639467E5C5EF9F65B31F194C31586D56141A7906DE6EE2B40803E06A301F9EEE9C8B04FA6AF8C5950F64",  # noqa: E501
                        16,
                    ),
                    int(
                        "0910709BEC8515357CB68AE88EA0B7EC6D54190773CC82EDDA68180D62BA214737DC708A5DA815E8B872D3C5B31E5A00",  # noqa: E501
                        16,
                    ),
                ]
            ),  # G2-x1
            FQ2(
                [
                    int(
                        "12416C8B9159A047D5F92A6A4E941156E29E2A489B671D2FC3D8ED60FFA5F53FE846ECFB0090211197EF3BA4C07424F9",  # noqa: E501
                        16,
                    ),
                    int(
                        "089977D619CEA9D6D11F7148E1CB7622E46153BF1B4D81944603AA72AEFA6CE7CF07550CB6B582D17440F5949D1214FA",  # noqa: E501
                        16,
                    ),
                ]
            ),
        ),  # G2-y1
    ],
)
def test_iso_map_G2(iso_x, iso_y, iso_z, g2_x, g2_y):
    (result_x, result_y, result_z) = iso_map_G2(iso_x, iso_y, iso_z)

    result_x = result_x / result_z
    result_y = result_y / result_z

    assert g2_x == result_x
    assert g2_y == result_y


# Tests taken from: https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/blob/master/draft-irtf-cfrg-hash-to-curve.md#bls12381g2_xmdsha-256_sswu_ro_  # blocklint: URL pragma  # noqa: E501
@pytest.mark.parametrize("H", [sha256])
@pytest.mark.parametrize(
    "msg,x,y",
    [
        (
            b"",
            FQ2(
                [
                    0x0141EBFBDCA40EB85B87142E130AB689C673CF60F1A3E98D69335266F30D9B8D4AC44C1038E9DCDD5393FAF5C41FB78A,  # noqa: E501
                    0x05CB8437535E20ECFFAEF7752BADDF98034139C38452458BAEEFAB379BA13DFF5BF5DD71B72418717047F5B0F37DA03D,  # noqa: E501
                ]
            ),
            FQ2(
                [
                    0x0503921D7F6A12805E72940B963C0CF3471C7B2A524950CA195D11062EE75EC076DAF2D4BC358C4B190C0C98064FDD92,  # noqa: E501
                    0x12424AC32561493F3FE3C260708A12B7C620E7BE00099A974E259DDC7D1F6395C3C811CDD19F1E8DBF3E9ECFDCBAB8D6,  # noqa: E501
                ]
            ),
        ),
        (
            b"abc",
            FQ2(
                [
                    0x02C2D18E033B960562AAE3CAB37A27CE00D80CCD5BA4B7FE0E7A210245129DBEC7780CCC7954725F4168AFF2787776E6,  # noqa: E501
                    0x139CDDBCCDC5E91B9623EFD38C49F81A6F83F175E80B06FC374DE9EB4B41DFE4CA3A230ED250FBE3A2ACF73A41177FD8,  # noqa: E501
                ]
            ),
            FQ2(
                [
                    0x1787327B68159716A37440985269CF584BCB1E621D3A7202BE6EA05C4CFE244AEB197642555A0645FB87BF7466B2BA48,  # noqa: E501
                    0x00AA65DAE3C8D732D10ECD2C50F8A1BAF3001578F71C694E03866E9F3D49AC1E1CE70DD94A733534F106D4CEC0EDDD16,  # noqa: E501
                ]
            ),
        ),
        (
            b"abcdef0123456789",
            FQ2(
                [
                    0x121982811D2491FDE9BA7ED31EF9CA474F0E1501297F68C298E9F4C0028ADD35AEA8BB83D53C08CFC007C1E005723CD0,  # noqa: E501
                    0x190D119345B94FBD15497BCBA94ECF7DB2CBFD1E1FE7DA034D26CBBA169FB3968288B3FAFB265F9EBD380512A71C3F2C,  # noqa: E501
                ]
            ),
            FQ2(
                [
                    0x05571A0F8D3C08D094576981F4A3B8EDA0A8E771FCDCC8ECCEAF1356A6ACF17574518ACB506E435B639353C2E14827C8,  # noqa: E501
                    0x0BB5E7572275C567462D91807DE765611490205A941A5A6AF3B1691BFE596C31225D3AABDF15FAFF860CB4EF17C7C3BE,  # noqa: E501
                ]
            ),
        ),
        (
            b"q128_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",  # noqa: E501
            FQ2(
                [
                    0x19A84DD7248A1066F737CC34502EE5555BD3C19F2ECDB3C7D9E24DC65D4E25E50D83F0F77105E955D78F4762D33C17DA,  # noqa: E501
                    0x0934ABA516A52D8AE479939A91998299C76D39CC0C035CD18813BEC433F587E2D7A4FEF038260EEF0CEF4D02AAE3EB91,  # noqa: E501
                ]
            ),
            FQ2(
                [
                    0x14F81CD421617428BC3B9FE25AFBB751D934A00493524BC4E065635B0555084DD54679DF1536101B2C979C0152D09192,  # noqa: E501
                    0x09BCCCFA036B4847C9950780733633F13619994394C23FF0B32FA6B795844F4A0673E20282D07BC69641CEE04F5E5662,  # noqa: E501
                ]
            ),
        ),
        (
            b"a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # noqa: E501
            FQ2(
                [
                    0x01A6BA2F9A11FA5598B2D8ACE0FBE0A0EACB65DECEB476FBBCB64FD24557C2F4B18ECFC5663E54AE16A84F5AB7F62534,  # noqa: E501
                    0x11FCA2FF525572795A801EED17EB12785887C7B63FB77A42BE46CE4A34131D71F7A73E95FEE3F812AEA3DE78B4D01569,  # noqa: E501
                ]
            ),
            FQ2(
                [
                    0x0B6798718C8AED24BC19CB27F866F1C9EFFCDBF92397AD6448B5C9DB90D2B9DA6CBABF48ADC1ADF59A1A28344E79D57E,  # noqa: E501
                    0x03A47F8E6D1763BA0CAD63D6114C0ACCBEF65707825A511B251A660A9B3994249AE4E63FAC38B23DA0C398689EE2AB52,  # noqa: E501
                ]
            ),
        ),
    ],
)
def test_hash_to_G2(msg, x, y, H):
    point = hash_to_G2(msg, DST_G2, H)
    assert is_on_curve(point, b2)

    # Affine
    result_x = point[0] / point[2]  # X / Z
    result_y = point[1] / point[2]  # Y / Z

    assert x == result_x
    assert y == result_y


@pytest.mark.parametrize(
    "degree",
    [
        (1),
        (2),
        (12),
    ],
)
@pytest.mark.parametrize(
    "value, expected",
    [
        (0x00, 0),
        (0x10, 0),
        (0x01, 1),
    ],
)
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


@pytest.mark.parametrize(
    "value, expected",
    [
        ([0x00, 0x00], 0),
        ([0x10, 0x00], 0),
        ([0x01, 0x00], 1),
        ([0x01, 0x01], 1),
        ([0x10, 0x10], 0),
    ],
)
def test_FQ2_sgn0(value, expected):
    x = FQ2(value)
    y = FQP(value, modulus_coeffs=FQ2.FQ2_MODULUS_COEFFS)
    assert x.sgn0 == y.sgn0 == expected


# --- G1 ---


# https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/blob/main/draft-irtf-cfrg-hash-to-curve.md#bls12381g1_xmdsha-256_sswu_ro_  # noqa: E501
@pytest.mark.parametrize("H", [sha256])
@pytest.mark.parametrize(
    "msg,x,y",
    [
        (
            b"",
            FQ(
                0x052926ADD2207B76CA4FA57A8734416C8DC95E24501772C814278700EED6D1E4E8CF62D9C09DB0FAC349612B759E79A1  # noqa: E501
            ),
            FQ(
                0x8BA738453BFED09CB546DBB0783DBB3A5F1F566ED67BB6BE0E8C67E2E81A4CC68EE29813BB7994998F3EAE0C9C6A265  # noqa: E501
            ),
        ),
        (
            b"abc",
            FQ(
                0x03567BC5EF9C690C2AB2ECDF6A96EF1C139CC0B2F284DCA0A9A7943388A49A3AEE664BA5379A7655D3C68900BE2F6903  # noqa: E501
            ),
            FQ(
                0x0B9C15F3FE6E5CF4211F346271D7B01C8F3B28BE689C8429C85B67AF215533311F0B8DFAAA154FA6B88176C229F2885D  # noqa: E501
            ),
        ),
        (
            b"abcdef0123456789",
            FQ(
                0x11E0B079DEA29A68F0383EE94FED1B940995272407E3BB916BBF268C263DDD57A6A27200A784CBC248E84F357CE82D98  # noqa: E501
            ),
            FQ(
                0x03A87AE2CAF14E8EE52E51FA2ED8EEFE80F02457004BA4D486D6AA1F517C0889501DC7413753F9599B099EBCBBD2D709  # noqa: E501
            ),
        ),
        (
            b"q128_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",  # noqa: E501
            FQ(
                0x15F68EAA693B95CCB85215DC65FA81038D69629F70AEEE0D0F677CF22285E7BF58D7CB86EEFE8F2E9BC3F8CB84FAC488  # noqa: E501
            ),
            FQ(
                0x1807A1D50C29F430B8CAFC4F8638DFEEADF51211E1602A5F184443076715F91BB90A48BA1E370EDCE6AE1062F5E6DD38  # noqa: E501
            ),
        ),
        (
            b"a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # noqa: E501
            FQ(
                0x082AABAE8B7DEDB0E78AEB619AD3BFD9277A2F77BA7FAD20EF6AABDC6C31D19BA5A6D12283553294C1825C4B3CA2DCFE  # noqa: E501
            ),
            FQ(
                0x05B84AE5A942248EEA39E1D91030458C40153F3B654AB7872D779AD1E942856A20C438E8D99BC8ABFBF74729CE1F7AC8  # noqa: E501
            ),
        ),
    ],
)
def test_hash_to_G1(msg, x, y, H):
    point = hash_to_G1(msg, DST_G1, H)
    assert is_on_curve(point, b)

    # Affine
    result_x = point[0] / point[2]  # X / Z
    result_y = point[1] / point[2]  # Y / Z

    assert x == result_x
    assert y == result_y
