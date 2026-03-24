# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

# ---- new imports
# from pathlib import Path
import os

from phenospy.owl_xmlToOwl import *
from phenospy.phs_addXmlMeta import *
from phenospy.phs_grammar import *
from phenospy.phs_various_fun import *
from phenospy.phs_xml import *
from phenospy.phs_xmlTranslateTerms import *
from phenospy.snips_makeFromYaml import *
from phenospy.snips_readFromJSON import *

# -----------------------------------------
# Converts phs file to owl
# -----------------------------------------

# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
# phs_file    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Gryonoides/phs/gryo.phs'
# yaml_file   = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
# save_dir    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/'
# save_pref   = 'gryo'

def phsToOWL(phs_file, yaml_file, save_dir, save_pref):
    #
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
    print(f"{Fore.BLUE}Saving XML...{Style.RESET_ALL}")
    with open(xml_save, 'w') as f:
        f.write(xml_final)
        f.close()
    print(f"{Fore.GREEN}Done! XML is saved to:{Style.RESET_ALL}",  xml_save)
    # -----------------------------------------
    # XML to OWL
    # -----------------------------------------
    # tree = ET.parse(xml_save)
    tree = ET.ElementTree(ET.fromstring(xml_final))
    # set_log_level(0)
    xmlToOwl(tree, owl_save)
    #
    #-----------------------
    # Load saved owl file with RDFLib
    #-----------------------
    from rdflib import Graph
    
    print(f"{Fore.BLUE}Loading OWL into RDFLib...{Style.RESET_ALL}")
    g = Graph()
    g.parse(owl_save, format="xml")
    print(f"{Fore.GREEN}Done loading RDFLib graph.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Triples in graph:{Style.RESET_ALL} {len(g)}")

    # #-----------------------
    # # Apply SPARQL update
    # #-----------------------
    print(f"{Fore.BLUE}Applying SPARQL update...{Style.RESET_ALL}")
    ru_path = os.path.join(get_phenospyPath(), "package-data", "sparql-update-owl", "card.ru")
    with open(ru_path, "r", encoding="utf-8") as f:
        update_query = f.read()
    print(repr(update_query[:300]))
    g.update(update_query)
    print(f"{Fore.GREEN}Done applying update.{Style.RESET_ALL}")

    # #-----------------------
    # # Save updated graph
    # #-----------------------
    ttl_save = os.path.join(save_dir, save_pref + '.owl')
    #out_file = "out.ttl"
    print(f"{Fore.BLUE}Saving updated graph:{Style.RESET_ALL} {ttl_save}")
    #g.serialize(destination=ttl_save, format="turtle")
    g.serialize(destination=ttl_save, format="xml")
    print(f"{Fore.GREEN}Done saving updated graph.{Style.RESET_ALL}")