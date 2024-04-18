def test_import_and_version():
    import py_ecc

    assert isinstance(py_ecc.__version__, str)
