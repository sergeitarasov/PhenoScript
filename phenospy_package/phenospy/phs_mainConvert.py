# ---- new imports
# from pathlib import Path
import os
import rdflib

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

def phsToOWL(phs_file, yaml_file, save_dir, save_pref, keep_raw=False, enrich_gbif=False):
    #
    xml_save = os.path.join(save_dir, save_pref + '.xml')
    owl_save = os.path.join(save_dir, save_pref + '_raw.owl')
    # ----------------------------------------
    # Parse phs file
    # -----------------------------------------
    out = parsePHS(phs_file, enrich_gbif)
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


    #-----------------------
    # Load saved owl file with RDFLib
    #-----------------------   
    print(f"{Fore.BLUE}Loading OWL into RDFLib...{Style.RESET_ALL}")
    g = rdflib.Graph()
    g.parse(owl_save, format="xml")
    print('DONE')
    #-----------------------
    # Apply SPARQL update
    #-----------------------
    print(f"{Fore.BLUE}Applying SPARQL update...{Style.RESET_ALL}")
    sparql_path = os.path.join(get_phenospyPath(), "package-data", "sparql-update", "update-owl-core.ru")
    with open(sparql_path, "r", encoding="utf-8") as f:
        update_query = f.read()
    g.update(update_query)
    #-----------------------
    # Save updated graph
    #-----------------------
    updated_owl_save = os.path.join(save_dir, save_pref + '.owl')
    g.serialize(destination=updated_owl_save, format="xml")
    print(f"{Fore.GREEN}Done saving updated graph:{Style.RESET_ALL} {updated_owl_save}")
    # -----------------------------------------
    # Optionally delete _raw.owl file
    # -----------------------------------------
    if not keep_raw:
        if os.path.exists(owl_save):
            os.remove(owl_save)