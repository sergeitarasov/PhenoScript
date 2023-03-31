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
# -----------------------------------------
# Traverse graph
# -----------------------------------------
print(f"{Fore.BLUE}Traversing RDF graph...{Style.RESET_ALL}")

ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')
ind0 = onto.search(label = 'org_Grebennikovius')
ind0 = ind0[0]
tabs="\t"

global visited_nodes, visited_triples
visited_nodes=set()
visited_triples=list()
#-----
# def makeNL(onto, ind0, file_save=None):
#     print(f"{Fore.BLUE}Rendering NL description as markdown...{Style.RESET_ALL}")
#     visited_nodes=set()
#     visited_triples=list()
#     md = traverseGraphForNL(onto, ind0, tabs='\t', tab_char='\t', visited_nodes=set())
#     # print(md)
#     md_out = md.replace("\t [", " [")
#     md_out = md_out.replace("\t [", "\t- [")
#     md_out = md_out.replace("\n [", "\n- [")
#     # Add species name as comment
#     header = '<!-- ' + ind0.label.first() + ' -->'
#     md_out = header + md_out
#     #print(md_out)
#     print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
#     if file_save is not None:
#         print(f"{Fore.BLUE}Saving markdown to:{Style.RESET_ALL}", file_save)
#         fl = open(file_save, "w+")
#         fl.writelines(md_out)
#         fl.close()
#     return md_out

# --- Save
print(f"{Fore.BLUE}Saving markdown to:{Style.RESET_ALL}")

DD_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test.md'
file1 = open(DD_file, "w+")
file1.writelines(md_out)
file1.close()

print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")

