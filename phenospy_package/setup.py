from setuptools import setup, find_packages

setup(
    name='phenospy',
    version='0.12',
    packages=find_packages(exclude=['tests*', 'devel*', 'build*']),
    license='MIT',
    description='Tools for making and processing computable phenotype descriptions',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=['Owlready2',
                      'PyYAML',
                      'colorama',
                      'pyparsing==2.4.2'],
    include_package_data=True,
    url='https://github.com/sergeitarasov/PhenoScript',
    author='Sergei Tarasov',
    author_email='sergei.tarasov@helsinki.fi',
    project_urls={
        "Project Logo": "https://raw.githubusercontent.com/sergeitarasov/PhenoScript/main/Phenoscript_logo.png",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    
)