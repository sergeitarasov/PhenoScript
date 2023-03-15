# remove pandas???

from setuptools import setup, find_packages

setup(
    name='phenospy',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Tools for computable phenotype descriptions',
    long_description=open('README.md').read(),
    install_requires=['owlready2',
                      'pyyaml',
                      'colorama',
                      'pandas',
                      'numpy',
                      'pyparsing==2.4.2'],
    include_package_data=True,
    url='https://github.com/sergeitarasov/PhenoScript',
    author='Sergei Tarasov',
    author_email='sergei.tarasov@helsinki.fi'
)