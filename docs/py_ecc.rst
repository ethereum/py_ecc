py\_ecc
=======

.. warning::

    This library contains some experimental code and has not been audited.

BLS Signatures
--------------

``py_ecc`` implements the `IETF BLS draft standard v4 <https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-04>`_ as per the inter-blockchain standardization agreement. The BLS standards specify `different ciphersuites <https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-04#section-4>`_ which each have different functionality to accommodate various use cases. The following ciphersuites are available from this library:

- ``G2Basic`` also known as ``BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_``
- ``G2MessageAugmentation`` also known as ``BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_AUG_``
- ``G2ProofOfPossession`` also known as ``BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_``

Basic Usage
-----------

.. code-block:: python

    from py_ecc.bls import G2ProofOfPossession as bls_pop

    private_key = 5566
    public_key = bls_pop.SkToPk(private_key)

    message = b'\xab' * 32  # The message to be signed

    # Signing
    signature = bls_pop.Sign(private_key, message)

    # Verifying
    assert bls_pop.Verify(public_key, message, signature)

Aggregating Signatures
----------------------

.. code-block:: python

    private_keys = [3, 14, 159]
    public_keys = [bls_pop.SkToPk(key) for key in private_keys]
    signatures = [bls_pop.Sign(key, message) for key in private_keys]

    # Aggregating
    agg_sig = bls_pop.Aggregate(signatures)

    # Verifying signatures over the same message.
    # Note this is only safe if Proofs of Possession have been verified for each of the public keys beforehand.
    # See the BLS standards for why this is the case.
    assert bls_pop.FastAggregateVerify(public_keys, message, agg_sig)

Multiple Aggregation
--------------------

.. code-block:: python

    messages = [b'\xaa' * 42, b'\xbb' * 32, b'\xcc' * 64]
    signatures = [bls_pop.Sign(key, message) for key, message in zip(private_keys, messages)]
    agg_sig = bls_pop.Aggregate(signatures)

    # Verify aggregate signature with different messages
    assert bls_pop.AggregateVerify(public_keys, messages, agg_sig)


py_ecc package
--------------

.. toctree::
    :maxdepth: 4

    py_ecc.bls
    py_ecc.bls12_381
    py_ecc.bn128
    py_ecc.optimized_bn128
    py_ecc.secp256k1
    py_ecc.fields
    py_ecc.optimized_bls12_381
