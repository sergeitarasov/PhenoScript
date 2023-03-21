# import os
# os.getcwd()
# os.chdir('./src')

# ---- new imports
from pathlib import Path
from phs_various_fun import *
# from phs_parser_fun import *
from phs_grammar import *
from phs_xml import *
from snips_readFromJSON import *
from phs_addXmlMeta import *
from phs_xmlTranslateTerms import *


# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
file_phs = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Gryonoides/phs/gryo.phs'  # 'data/Gryonoides.phs'
yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'

base_iri = 'https://' + 'urn:uuid:' + str(uuid.uuid1())  # https://urn:uuid:2348c8b6-c31c-11ed-876a-acde48001122

xml_save = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data' \
           '/phs_xml.xml'

# -----------------------------------------
# Read yaml
# -----------------------------------------

print(f"{Fore.BLUE}Reading yaml file...{Style.RESET_ALL}")
with open(yaml_file, 'r') as f_yaml:
    phs_yaml = yaml.safe_load(f_yaml)
# print(phs_yaml)
print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")


# -----------------------------------------
# Read phs file
# -----------------------------------------
print('Reading in PhenoScript file', file_phs, '...', flush=True)
txt = Path(file_phs).read_text()
print(txt)
# check if brackets are balanced
is_balan = is_balanced(txt)
print('-', is_balan, flush=True)

# -----------------------------------------
# Parse phs file
# -----------------------------------------

print('Parsing PhenoScript file ...', flush=True)
print('The following OTUs found:', flush=True)
out = grammar1.parseString(txt)
print(out)
# global var_countOTU reset
var_countOTU.reset(prefix='', starting_id=1)

# -----------------------------------------
# phs to XML
# -----------------------------------------
print('Converting PhenoScript to XML ...', flush=True)
out_xml = phenoscript2xml(out, base_iri)
print(out_xml)

# -----------------------------------------
# Translate XML terms into IRIs from ontology
#  and add translation to XML
# -----------------------------------------

tree = ET.ElementTree(ET.fromstring(out_xml))
ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
root = tree.getroot()

dic_iri, dic_type, dic_lab = make_dicsFromSnips(yaml_file)
snipsDic = snipsLabelDictionary(dic_iri, dic_type, dic_lab)

xmlTranslateTerms(root, snipsDic)

# -----------------------------------------
# Add Meta
# -----------------------------------------

#tree = ET.ElementTree(ET.fromstring(root))
#ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
root = tree.getroot()
xml_add_YamlMeta(root, phs_yaml, base_iri)

# Pretty-print the combined XML tree
xml_string = ET.tostring(root, encoding='unicode')
xml_string = xmldom.parseString(xml_string).toprettyxml(indent="\t", newl="\n", encoding=None)
xml_string = "\n".join([ll.rstrip() for ll in xml_string.splitlines() if ll.strip()])
print(xml_string)

# -----------------------------------------
# Save
# -----------------------------------------

# tree.write(xml_save, encoding="utf-8")
print('Saving file ...', flush=True)
with open(xml_save, 'w') as f:
    f.write(xml_string)
    f.close()

print('DONE! The instances are saved to:', xml_save, flush=True)



