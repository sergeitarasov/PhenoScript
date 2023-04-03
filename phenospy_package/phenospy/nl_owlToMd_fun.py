from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()
from phenospy.owl_owlready_config import *


# -----------------------------------------
# Make NL Graph for Md rendering from OWL: high-level wrapper
# -----------------------------------------
def owlToNLgraph(owl_file):
    # -----------------------------------------
    # Arguments
    # -----------------------------------------
    # set_log_level(0)
    print(f"{Fore.BLUE}Reading OWL:{Style.RESET_ALL}", owl_file)
    onto = get_ontology(owl_file).load(reload_if_newer=True, reload=True)
    # -----------------------------------------
    # Namespaces
    # -----------------------------------------
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')
    import phenospy.nl_fun
    # -----------------------------------------
    # Make NL graph 
    # -----------------------------------------
    phenospy.nl_fun.makeNLGraph_basic(onto)
    return onto


# -----------------------------------------
# Make NL desciptions in Md format
# -----------------------------------------
# ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')[0]
def NLgraphToMarkdown(onto, ind0, file_save=None, verbose=False):
    
    print(f"{Fore.BLUE}Converting NL graph to Markdown...{Style.RESET_ALL}")
    global visited_nodes, visited_triples
    visited_nodes=set()
    visited_triples=list()
    #
    import phenospy.nl_fun
    md = phenospy.nl_fun.traverseGraphForNL(onto, ind0, tabs='\t', tab_char='\t', visited_nodes=set())
    # print(md)
    md_out = md.replace("\t [", " [")
    md_out = md_out.replace("\t [", "\t- [")
    md_out = md_out.replace("\n [", "\n- [")
    # Add species name as comment
    header = '<!-- ' + ind0.label.first() + ' -->'
    md_out = header + md_out
    #print(md_out)
    #
    visited_nodes=set()
    phenospy.nl_fun.visited_triples=list()
    #
    if file_save is not None:
        print(f"{Fore.BLUE}Saving Markdown to:{Style.RESET_ALL}", file_save)
        fl = open(file_save, "w+")
        fl.writelines(md_out)
        fl.close()
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    if verbose==True:
        return md_out