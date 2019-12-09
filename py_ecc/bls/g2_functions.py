def G2_sign(sk: int, message: bytes) -> BLSSignature:
    return G2_to_signature(
        multiply(
            hash_to_G2(message),
            sk,
        ))



def G2_privtopub(k: int) - BLSPubkey:
    return G1_to_pubkey(multiply(G1, k))

def verify(pk: BLSPubkey,
           message: bytes,
           signature: BLSSignature) -> bool:
    signature_point = signature_to_G2(signature)
    if not is_inf(multiply(signature_point, curve_order)):
        return False
    try:
        final_exponentiation = final_exponentiate(
            pairing(
                signature_point,
                G1,
                final_exponentiate=False,
            ) * pairing(
                hash_to_G2(message),
                neg(pubkey_to_G1(pk)),
                final_exponentiate=False,
            )
        )
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False


def G2_aggregate_signatures(signatures: Sequence[BLSSignature]) -> BLSSignature:
    o = Z2
    for s in signatures:
        o = add(o, signature_to_G2(s))
    return G2_to_signature(o)


def G2_aggregate_pubkeys(pks: Sequence[BLSPubkey]) -> BLSPubkey:
    o = Z1
    for p in pks:
        o = add(o, pubkey_to_G1(p))
    return G1_to_pubkey(o)


def G2_aggregate_verify(pks: Sequence[BLSPubkey],
                     messages: Sequence[bytes],
                     signature: BLSSignature) -> bool:
    len_msgs = len(messages)

    if len(pks) != len_msgs:
        raise ValidationError(
            "len(pks) (%s) should be equal to len(message) (%s)" % (
                len(pks), len_msgs
            )
        )

    signature_point = signature_to_G2(signature)
    if not is_inf(multiply(signature_point, curve_order)):
        return False

    try:
        o = FQ12([1] + [0] * 11)
        for m_pubs in set(messages):
            # aggregate the pubs
            group_pub = Z1
            for i in range(len_msgs):
                if messages[i] == m_pubs:
                    group_pub = add(group_pub, pubkey_to_G1(pks[i]))

            o *= pairing(hash_to_G2(m_pubs), group_pub, final_exponentiate=False)
        o *= pairing(signature_point, neg(G1), final_exponentiate=False)

        final_exponentiation = final_exponentiate(o)
        return final_exponentiation == FQ12.one()
    except (ValidationError, ValueError, AssertionError):
        return False