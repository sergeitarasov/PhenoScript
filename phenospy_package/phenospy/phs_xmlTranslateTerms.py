import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET

from phenospy.phs_addXmlMeta import *
from phenospy.snips_fun import *
from phenospy.snips_readFromJSON import *


def xmlTranslateTerms(root, snipsDic):
  print(f"{Fore.BLUE}Translating terms using JSON snippets...{Style.RESET_ALL}")
  snipsDic.resetCount()
  toExit = False
  # nodes
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node'):
    # print(nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name'))
    label = nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name')
    iri, lab_org, type_snips = snipsDic.translate_lab(label)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}label_original', lab_org)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}type_onto', type_snips)
  
  # print(f"{Fore.GREEN}- Nodes translated: %s{Style.RESET_ALL}" % snipsDic.countLBS)
  if snipsDic.countNA == 0:
    print(f"{Fore.GREEN}- Good! Nodes: all translated!{Style.RESET_ALL}")
  else:
    print(f"{Fore.RED}- Warning! Untranslated nodes found: %s{Style.RESET_ALL}" % snipsDic.countNA)
    toExit = True
    snipsDic.print_untrans()
    snipsDic.reset_untrans()

  # print untranslated terms
  snipsDic.resetCount()

  

  # edges
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}edge'):
    # print(nn.get('{https://github.com/sergeitarasov/PhenoScript}edge_name'))
    label = nn.get('{https://github.com/sergeitarasov/PhenoScript}edge_name')
    iri, lab_org, type_snips = snipsDic.translate_lab(label)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}label_original', lab_org)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}type_onto', type_snips)

  # print(f"{Fore.GREEN}- Edges translated: %s{Style.RESET_ALL}" % snipsDic.countLBS)
  # print(f"{Fore.RED}- Edges untranslated: %s{Style.RESET_ALL}" % snipsDic.countNA)
  # snipsDic.resetCount()

  if snipsDic.countNA == 0:
    print(f"{Fore.GREEN}- Good! Edges: all translated!{Style.RESET_ALL}")
  else:
    print(f"{Fore.RED}- Warning! Untranslated edges found: %s{Style.RESET_ALL}" % snipsDic.countNA)
    toExit = True
    snipsDic.print_untrans()
    snipsDic.reset_untrans()
  
  # print untranslated terms
  snipsDic.resetCount()

  
  
  # phs:node_property

  # import itertools
  # nn = next(itertools.islice(root.iter('{https://github.com/sergeitarasov/PhenoScript}node_property'), 2, 3), 
  # None)
  skip_names = ['node_name', 'int', 'numeric_type', 'real']
  # 'int' not in skip_names
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node_property'):
    # print(nn.text)
    #label=nn.text
    if nn.text not in skip_names:
      # --- text
      # print(nn.text)
      iri, lab_org, type_snips = snipsDic.translate_lab(nn.text)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}var-iri', iri)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}var-label_original', lab_org)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}var-type_onto', type_snips)

      # --- values
      value = nn.get('{https://github.com/sergeitarasov/PhenoScript}value')
      # print(value)
      iri, lab_org, type_snips = snipsDic.translate_lab(value)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}value-iri', iri)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}value-label_original', lab_org)
      nn.set('{https://github.com/sergeitarasov/PhenoScript}value-type_onto', type_snips)
    #----
    # label=nn.get('{https://github.com/sergeitarasov/PhenoScript}value')
    # iri=iriDic.translate(label)
    # #print(iri)
    # nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
  
  # print('- translated phs:node_property: %s; NA phs:node_property: %s.' % (iriDic.countLBS, iriDic.countNA))
  # iriDic.resetCount()
  if snipsDic.countNA == 0:
    print(f"{Fore.GREEN}- Good! Node Properties: all translated!{Style.RESET_ALL}")
  else:
    print(f"{Fore.RED}- Warning! Untranslated Node Properties found: %s{Style.RESET_ALL}" % snipsDic.countNA)
    toExit = True
    snipsDic.print_untrans()
    snipsDic.reset_untrans()

  #
  snipsDic.resetCount()

  if toExit == True:
    print(f"{Fore.RED}Warning! Fix untralstated items and re-run.{Style.RESET_ALL}")
    exit()






# -----------------------------------------
# Translate XML and add metadata
# -----------------------------------------
def xmlTranslateTermsMeta(xml_str, base_iri, yaml_file):
    # -----------------------------------------
    # Read yaml
    # -----------------------------------------
    print(f"{Fore.BLUE}Reading yaml file...{Style.RESET_ALL}")
    with open(yaml_file, 'r') as f_yaml:
        phs_yaml = yaml.safe_load(f_yaml)
    # print(phs_yaml)
    print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

    # -----------------------------------------
    # Prepearing snippets
    # -----------------------------------------
    print(f"{Fore.BLUE}Preparing snippets for translation...{Style.RESET_ALL}")
    dic_iri, dic_type, dic_lab = make_dicsFromSnips(phs_yaml)
    snipsDic = snipsLabelDictionary(dic_iri, dic_type, dic_lab)

    # -----------------------------------------
    # Prepearing XML and translating
    # -----------------------------------------
    tree = ET.ElementTree(ET.fromstring(xml_str))
    ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
    root = tree.getroot()

    print(f"{Fore.BLUE}Translating XML...{Style.RESET_ALL}")
    xmlTranslateTerms(root, snipsDic)

    # -----------------------------------------
    # Add Meta
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding metadata to XML...{Style.RESET_ALL}")
    #tree = ET.ElementTree(ET.fromstring(root))
    #ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
    # root = tree.getroot()
    xml_add_YamlMeta(root, phs_yaml, base_iri)
    
    # -----------------------------------------
    # Pretty-print of the combined XML tree
    # -----------------------------------------
    xml_string = ET.tostring(root, encoding='unicode')
    xml_string = xmldom.parseString(xml_string).toprettyxml(indent="\t", newl="\n", encoding=None)
    xml_string = "\n".join([ll.rstrip() for ll in xml_string.splitlines() if ll.strip()])
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    return xml_string