from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()
from phenospy.owl_owlready_config import *
from phenospy.nl_owlToMd_fun import *

# -----------------------------------------
# Arguments
# -----------------------------------------
owl_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/output/Grebennikovius.owl'

# -----------------------------------------
# Making NL graph
# -----------------------------------------
onto = owlToNLgraph(owl_file)

# -----------------------------------------
# NL graph to Markdown
# -----------------------------------------
fl_md = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test1.md'
ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')[0]
NLgraphToMarkdown(onto, ind0, file_save = fl_md, verbose =True)

fl_md = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test2.md'
ind0 = onto.search(label = 'org_Grebennikovius')[0]
NLgraphToMarkdown(onto, ind0, file_save = fl_md, verbose =True)