from setuptools import find_packages, setup

setup(
    name='tennis',
    version='1.0',
    description='tennis app',
    url='https://github.com/ConorWaldron/tennis.git',
    author='Conor Waldron',
    packages=find_packages(exclude=['scripts', 'tests']),
    python_requires='>3.7',
    install_requires=[
        'dash==2.7.1',
        'dash_bootstrap_components==1.3.0',
        'pandas==1.5.2',
    ]
)