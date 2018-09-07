'setup.py for car cost calculator GUI'

# pylint: disable=W0622
from codecs import open  # To use a consistent encoding
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='ccc-gui',
    version='0.1.0',
    description='Total cost of ownership calculator for cars',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/DC23/ccc-gui',
    author='DC23',
    author_email='jugglindan@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms='any',

    install_requires=[
        'car-cost-calculator',
        'numpy',
        'pandas',
    ],

    extras_require={
        'dev': [
            'bumpversion',
            'check-manifest',
            'pylint',
            'wheel',
            'yapf'
        ],
        'test': [
        ],
    },
)
