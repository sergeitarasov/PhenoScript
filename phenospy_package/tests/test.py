
from phenospy import *
help('phenospy')

yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
make_vscodeSnips(yaml_file)


#------
# Read data
# import yaml
import importlib.resources as importlib_resources
pkg = importlib_resources.files("phenospy")
pkg_data_file = pkg / "package-data" / "phs-config.yaml"

with open(pkg_data_file, 'r') as f_yaml:
    phs_yaml = yaml.safe_load(f_yaml)
print(phs_yaml)

printUniqueIRIs(pkg_data_file)

# python setup.py sdist
# pip install dist/phenospy-0.1.tar.gz --upgrade
# pip install /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/dist/phenospy-0.1.tar.gz --upgrade