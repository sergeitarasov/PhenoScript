# python setup.py sdist
# pip install dist/phenospy-0.1.tar.gz --upgrade

from phenospy import *

# Make snippets
yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
make_vscodeSnips(yaml_file)

# Create dictionaries from JSON snips in VS code
json_iri, json_type, json_lab = make_dicsFromSnips(yaml_file)

print(json_iri['_vlv_'])
print(json_iri['bfo-part_of'])
print(json_type['http://purl.obolibrary.org/obo/BFO_0000050'])
print(json_lab['http://purl.obolibrary.org/obo/BFO_0000050'])

