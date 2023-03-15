from snips_fun import *

def xmlTranslateTerms(root, snipsDic):
  print(f"{Fore.BLUE}Translating terms using JSON snippets...{Style.RESET_ALL}")
  snipsDic.resetCount()
  # nodes
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node'):
    # print(nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name'))
    label = nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name')
    iri, lab_org, type_snips = snipsDic.translate_lab(label)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}label_original', lab_org)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}type_onto', type_snips)
  
  # print('- translated nodes: %s; NA nodes: %s.' % (snipsDic.countLBS, snipsDic.countNA))
  print(f"{Fore.GREEN}* Nodes translated: %s{Style.RESET_ALL}" % snipsDic.countLBS)
  print(f"{Fore.RED}* Nodes untranslated: %s{Style.RESET_ALL}" % snipsDic.countNA)
  snipsDic.resetCount()
  
  # print untranslated terms
  snipsDic.print_untrans()
  snipsDic.reset_untrans()

  # edges
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}edge'):
    # print(nn.get('{https://github.com/sergeitarasov/PhenoScript}edge_name'))
    label = nn.get('{https://github.com/sergeitarasov/PhenoScript}edge_name')
    iri, lab_org, type_snips = snipsDic.translate_lab(label)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}label_original', lab_org)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}type_onto', type_snips)

  # print('- translated edges: %s; NA edges: %s.' % (snipsDic.countLBS, snipsDic.countNA))
  print(f"{Fore.GREEN}* Edges translated: %s{Style.RESET_ALL}" % snipsDic.countLBS)
  print(f"{Fore.RED}* Edges untranslated: %s{Style.RESET_ALL}" % snipsDic.countNA)
  snipsDic.resetCount()
  
  # print untranslated terms
  snipsDic.print_untrans()
  snipsDic.reset_untrans()
  
  # # phs:node_property
  # for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node_property'):
  #   #print(nn.text)
  #   #label=nn.text
  #   label=nn.get('{https://github.com/sergeitarasov/PhenoScript}value')
  #   iri=iriDic.translate(label)
  #   #print(iri)
  #   nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
  # print('- translated phs:node_property: %s; NA phs:node_property: %s.' % (iriDic.countLBS, iriDic.countNA))
  # iriDic.resetCount()
