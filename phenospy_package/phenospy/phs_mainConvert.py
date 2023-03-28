# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

# ---- new imports
# from pathlib import Path
import os
from phs_various_fun import *
from phs_grammar import *
from phs_xml import *
from snips_readFromJSON import *
from phs_addXmlMeta import *
from phs_xmlTranslateTerms import *
from snips_makeFromYaml import *
from owl_xmlToOwl import *


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