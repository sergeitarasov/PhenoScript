# Get to python

```bash
# go to dit
cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# activate
conda activate PhenoScript

## run conda env
/Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python
```

# Build python in normal mode

```{bash}

/Users/taravser/opt/anaconda3/envs/PhenoScript/bin/pip uninstall phenospy

python setup.py sdist

/Users/taravser/opt/anaconda3/envs/PhenoScript/bin/pip install dist/phenospy-0.12.tar.gz --upgrade

pip install /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/dist/phenospy-0.11.tar.gz --upgrade

```


# Build python for test pypi and pypi
[Help](https://realpython.com/pypi-publish-python-package/)



```bash
cd /Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package
python -m build
# check if description renders ok
twine check dist/*
# test pypi
twine upload --skip-existing -r testpypi dist/*
# pypi
twine upload --skip-existing dist/*

```

# Install

```bash
cd /Users/taravser/opt/anaconda3/bin/python

pip install /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/dist/phenospy-0.1.tar.gz --upgrade

```

