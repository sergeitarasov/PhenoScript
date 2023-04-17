# cd ~/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/examples/github_examples/Quick_start
# /Users/taravser/anaconda3/envs/Phenoscript/bin/python

from phenospy import *
import os

# Get the current directory
current_dir = os.getcwd()

# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'my_sicardi.phs')
yaml_file   = os.path.join(current_dir, 'phs-config.yaml')
save_dir    = os.path.join(current_dir, 'output/')
save_pref   = 'H_sicardi'

# -----------------------------------------
# Quick conversion: phs to OWL and XML
# -----------------------------------------
phsToOWL(phs_file, yaml_file, save_dir, save_pref)

# -----------------------------------------
# OWL to Markdown
# -----------------------------------------

# get owl file
owl_file = os.path.join(save_dir, save_pref + '.owl')

# Make NL graph
onto = owlToNLgraph(owl_file)

# Convert NL graph to Markdown
taxon = 'Helictopleurus sicardi'
file_md = os.path.join(current_dir, 'md', 'H_sicardi.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)
