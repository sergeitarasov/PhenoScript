
import sys
sys.path.append('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy')

# ---- new imports
from pathlib import Path

from owl_xmlToOwl import *
from phs_addXmlMeta import *
# from phs_parser_fun import *
from phs_grammar import *
from phs_mainConvert import *
from phs_various_fun import *
from phs_xml import *
from phs_xmlTranslateTerms import *
from snips_makeFromYaml import *
from snips_readFromJSON import *

# from phs_test import *

# my_function()

# -----------------------------------------
# Make snippets
# -----------------------------------------
yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
make_vscodeSnips(yaml_file)


# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Gryonoides/phs/gryo.phs'
yaml_file   = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
save_dir    = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/'
save_pref   = 'gryo'

# -----------------------------------------
# Quick conversion
# -----------------------------------------
phsToOWL(phs_file, yaml_file, save_dir, save_pref)


# -----------------------------------------
# Manual conversion:
# -----------------------------------------
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

