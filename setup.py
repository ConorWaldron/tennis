from setuptools import find_packages
from setuptools import setup

setup(
    name='tennis',
    version='0.0',
    description='tennis app',
    url='https://github.com/ConorWaldron/tennis.git',
    packages=find_packages(exclude=['scripts', 'tests']),
    python_requires='>3.7'
)