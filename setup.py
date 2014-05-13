import sys
import codecs
from setuptools import setup
import jsonrpcake


requirements = [
    'jsonrpc-ns>=0.5',
    'Pygments>=1.5'
]
try:
    #noinspection PyUnresolvedReferences
    import argparse  # NOQA
except ImportError:
    requirements.append('argparse>=1.2.1')

if 'win32' in str(sys.platform).lower():
    # Terminal colors for Windows
    requirements.append('colorama>=0.2.4')


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='jsonrpcake',
    version='1.1.0',
    description=jsonrpcake.__doc__.strip(),
    long_description=long_description(),
    author='Joe Hillenbrand',
    author_email='joehillen@gmail.com',
    license=jsonrpcake.__licence__,
    packages=['jsonrpcake'],
    entry_points={
        'console_scripts': [
            'jsonrpc = jsonrpcake.__main__:main',
        ],
    },
    install_requires=requirements,
)
