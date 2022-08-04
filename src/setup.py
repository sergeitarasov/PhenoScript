import os

# Install those packages that are not installed

# packages=[
# 'blas',
# 'bottleneck',
# 'bzip2',
# 'ca-certificates',
# 'certifi',
# 'intel-openmp',
# 'libcxx',
# 'libffi',
# 'mkl',
# 'mkl-service',
# 'mkl_fft',
# 'mkl_random',
# 'ncurses',
# 'numexpr',
# 'numpy',
# 'numpy-base',
# 'openssl',
# 'owlready2',
# 'packaging',
# 'pandas',
# 'pyparsing=2.4.2',
# 'pytz',
# 'readline',
# 'setuptools',
# 'six',
# 'sqlite',
# 'tk',
# 'tzdata',
# 'wheel',
# 'xz',
# 'zlib'
# ]

packages=[
'numpy',
'owlready2',
'pandas',
'pyparsing==2.4.2',
]

# pack =packages[1]
for pack in packages:
    print(pack)
    try:
        import pack
    except:
        #print('ok')
        os.system("pip install " + pack)
