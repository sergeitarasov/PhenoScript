# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

from phenospy import *
import os
# import phenospy

# versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

# -----------------------------------------
# Make snippets
# -----------------------------------------

# yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
# make_vscodeSnips(yaml_file)


# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/phs/Grebennikovius.phs'
yaml_file   = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/phs-config.yaml'
save_dir    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/output/'
save_pref   = 'Grebennikovius'

# -----------------------------------------
# Quick conversion: phs to OWL
# -----------------------------------------
phsToOWL(phs_file, yaml_file, save_dir, save_pref)



# -----------------------------------------
# OWL to Markdown
# -----------------------------------------

# get owl file
owl_file = os.path.join(save_dir, save_pref + '.owl')

# Making NL graph
onto = owlToNLgraph(owl_file)

# NL graph to Markdown
taxon = 'org_Grebennikovius_basilewskyi'
file_md = os.path.join(save_dir, 'md', taxon + '.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)

taxon = 'org_Grebennikovius'
file_md = os.path.join(save_dir, 'md', taxon + '.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)

taxon = 'my_species'
file_md = os.path.join(save_dir, 'md', taxon + '.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)
