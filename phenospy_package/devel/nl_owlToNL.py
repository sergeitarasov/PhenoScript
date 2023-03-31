# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

import sys
sys.path.append('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy')

from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()

import os
import markdown
from owl_owlready_config import *

# -----------------------------------------
# Arguments
# -----------------------------------------
set_log_level(9)
ontoFile='/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/output/Grebennikovius.owl'
onto = get_ontology(ontoFile).load(reload_if_newer=True, reload=True)


# -----------------------------------------
# Namespaces
# -----------------------------------------
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')
from nl_fun import *

# -----------------------------------------
# Make NL graph 
# -----------------------------------------
makeNLGraph(onto)

fl_md = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test1.md'
ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')[0]
makeNL(onto, ind0, file_save = fl_md)

fl_md = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test2.md'
ind0 = onto.search(label = 'org_Grebennikovius')[0]
makeNL(onto, ind0, file_save = fl_md)


