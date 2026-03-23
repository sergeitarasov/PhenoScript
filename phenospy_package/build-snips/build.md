# Get to python

```bash
# go to dit
# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
cd /Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# activate
conda activate PhenoScript

## run conda env
/Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python
```

# Development mode: code changes are available immediately

Use an editable install instead of building and reinstalling the tarball every time.

```bash
cd /Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package
conda activate PhenoScript

# remove old non-editable install if present
python -m pip uninstall phenospy

# install package in editable mode
python -m pip install -e .
```

After that, changes in `phenospy/*.py` are picked up the next time you run Python or the `phenospy` CLI.

Notes:

- Reinstall with `python -m pip install -e .` if you change `setup.py` dependencies or `console_scripts`.
- Restart the Python session only if you already imported the module in an interactive shell or notebook.

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
conda activate PhenoScript
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

