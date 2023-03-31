# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel
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
#ontoFile= '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test1.owl'
onto = get_ontology(ontoFile).load(reload_if_newer=True, reload=True)


# -----------------------------------------
# Namespaces
# -----------------------------------------
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')
from nl_fun import *

# -----------------------------------------
# Add absence
# -----------------------------------------
print(f"{Fore.BLUE}Adding absence traits...{Style.RESET_ALL}")

for ind in onto.individuals():
    #print(ind)
    if (len(ind.phs_implies_absence_of)>0):
        print(ind, "---", ind.phs_implies_absence_of)
        abs_class=ind.phs_implies_absence_of[0]
        txt=" [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
        print(txt)
        ind.phs_NL.append(txt)

# -----------------------------------------
# Pattern: add chracter prsence
# -----------------------------------------
print(f"{Fore.BLUE}Adding preence traits...{Style.RESET_ALL}")
add_presentTag_ToNLinOWL(default_world)

# -----------------------------------------
# SPARQL:  Absolute and Relative Mesuarements
# -----------------------------------------
print(f"{Fore.BLUE}Adding Absolute and Relative Mesuarements...{Style.RESET_ALL}")
query_tmpMesuare = sparql_tmpMeasurements(default_world)
dic_mesuare = tmpMeasureToDic(query_tmpMesuare)
# dic_mesuare obtained from sparql query to NL in OWL
dic_mesuare_ToNLinOWL(dic_mesuare)

# -----------------------------------------
# SPARQL:  Relative Comparison
#   Pattern: Org1 > E1 >> Q1 |comp| Q2 << E2 < Org2
# -----------------------------------------
print(f"{Fore.BLUE}Adding Relative Comparison traits...{Style.RESET_ALL}")

# Check existence and if existence render it to NL
# increased in magnitude relative to

compProp = obo.RO_0015007
if bool(compProp):
    query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015007.iri)
    dic_RelatComp = tmpRelatToDic(query_RelatComp)
    dic_Relat_ToNLinOWL(dic_RelatComp)

# decreased in magnitude relative to
compProp = obo.RO_0015008
if bool(compProp):
    query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015008.iri)
    dic_RelatComp = tmpRelatToDic(query_RelatComp)
    dic_Relat_ToNLinOWL(dic_RelatComp)


# makeNLGraph(onto)
# -----------------------------------------
# Traverse graph
# -----------------------------------------
print(f"{Fore.BLUE}Traversing RDF graph...{Style.RESET_ALL}")

ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')
ind0 = onto.search(label = 'org_Grebennikovius')
ind0 = ind0[0]
tabs="\t"
visited_nodes=set()
visited_triples=list()
#-----

md = traverseGraphForNL(onto, ind0, tabs='\t', tab_char='\t', visited_nodes=set())
print(md)
md
type(md)
xx = md.replace("\t [", " [")
xx = xx.replace("\t [", "\t- [")
xx = xx.replace("\n [", "\n- [")
print(xx)


# --- Save
print(f"{Fore.BLUE}Saving markdown to:{Style.RESET_ALL}")

DD_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test.md'
file1 = open(DD_file, "w+")
file1.writelines(xx)
file1.close()

print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")

