from setuptools import setup, find_packages

setup(
    name='PedigreeTools',
    version='0.1dev',
    description='Pedigree year of birth derivation',
    packages=find_packages(),
    install_requires=['inquirer'],
    author='Robin van Dijke',
    author_email='robin@vdijke.nl',
    license='MIT',
    long_description='A utility to calculate year of births for CSV based pedigree files based on a set of rules',
    python_requires='>=3.7',
    scripts=['bin/pedigree-tools'],
)
