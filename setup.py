# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

extras_require = {
    'test': [
        "pytest===3.2.2",
        "pytest-xdist"
    ],
    'lint': [
        "flake8==3.4.1",
        "mypy==0.641",
    ],
}


extras_require['dev'] = (
    extras_require['test'] +
    extras_require['lint']
)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='py_ecc',
    version='1.4.5',
    description='Elliptic curve crypto in python including secp256k1 and alt_bn128',
    long_description=readme,
    long_description_content_type='Elliptic curve crypto in python including secp256k1 and alt_bn128',
    author='Vitalik Buterin',
    author_email='',
    url='https://github.com/ethereum/py_ecc',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'py_ecc': ['py.typed']},
    install_requires=[
    ],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
