import importlib

from py_ecc import (
    _lazy_imports,
)


def test_import_and_version():
    import py_ecc

    assert isinstance(py_ecc.__version__, str)


def test_import_all_submodules():
    # test import of all submodules due to use of lazy imports
    for submod in _lazy_imports.values():
        importlib.import_module(submod)
