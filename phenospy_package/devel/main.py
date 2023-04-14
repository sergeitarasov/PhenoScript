# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

import sys
sys.path.append('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy')

import os
# ---- new imports
from owl_xmlToOwl import *
from phs_addXmlMeta import *
from phs_grammar import *
from phs_mainConvert import *
from phs_various_fun import *
from phs_xml import *
from phs_xmlTranslateTerms import *
from snips_makeFromYaml import *
from snips_readFromJSON import *
# from phs_parser_fun import *
# from pathlib import Path

# nl descriptions
from nl_owlToMd_fun import *

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
# Quick conversions:
#
# -----------------------------------------
# Quick conversion: phs to owl
# -----------------------------------------
phsToOWL(phs_file, yaml_file, save_dir, save_pref)


# -----------------------------------------
# owl to Md
# -----------------------------------------

# get owl file
owl_file = os.path.join(save_dir, save_pref + '.owl')

# Making NL graph
onto = owlToNLgraph(owl_file)

# NL graph to Markdown
taxon = 'org_Grebennikovius_basilewskyi'
file_md = os.path.join(save_dir, 'md', taxon + '.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =True)

taxon = 'org_Grebennikovius'
file_md = os.path.join(save_dir, 'md', taxon + '.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =True)




# ----------------------------------------------------------------------------------
# Slow, Manual conversion:
# ----------------------------------------------------------------------------------
xml_save = os.path.join(save_dir, save_pref + '.xml')
owl_save = os.path.join(save_dir, save_pref + '.owl')
# ----------------------------------------
# Parse phs file
# -----------------------------------------
out = parsePHS(phs_file)
# -----------------------------------------
# phs to XML
# -----------------------------------------
xml_str, base_iri = phenoscriptToXML(out)
xml_final = xmlTranslateTermsMeta(xml_str, base_iri, yaml_file)
# -----------------------------------------
# Save XML
# -----------------------------------------
with open(xml_save, 'w') as f:
    f.write(xml_final)
    f.close()
# -----------------------------------------
# XML to OWL
# -----------------------------------------
# tree = ET.parse(xml_save)
tree = ET.ElementTree(ET.fromstring(xml_final))
# set_log_level(0)
xmlToOwl(tree, owl_save)

