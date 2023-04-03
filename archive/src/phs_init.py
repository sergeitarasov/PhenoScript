import os
from pathlib import Path
#os.getcwd()
#os.chdir('./src')

#path_src="./src/"
exec(open(path_src+"phs_xml.py").read())
exec(open(path_src+"phs_parser.py").read())
exec(open(path_src+"phs_lbs2iri.py").read())

#PhenoScriptToXML(file_phs='data/phs/colao_AP.phs', file_phsDic=file_phsDic, xml_out='out.xml', instance_IRI=INSTANCE_IRI)

# The function below is the general wrapper

# file_phs='data/Gryonoides.phs'
# file_phsDic='results/dictionary/Gryo_dic.csv'
# xml_out='results/phs_Gryo.xml'
# instance_IRI='https://orcid.org/0000-0001-5237-2330/'
# 
# PhenoScriptToXML(file_phs='data/Gryonoides.phs', file_phsDic='results/dictionary/Gryo_dic.csv',
#   xml_out='results/phs_Gryo.xml', instance_IRI='https://orcid.org/0000-0001-5237-2330/')
def PhenoScriptToXML(file_phs, file_phsDic, xml_out, instance_IRI):
    #-----------------------------------------
    # Parse phs file
    #-----------------------------------------
    print('Reading in PhenoScript file', file_phs, '...',  flush=True)
    txt = Path(file_phs).read_text()
    # check if brackets are balanced
    isbalan=isBalanced(txt)
    print('-', isbalan,  flush=True)
    
    # parse
    # count read OTU objects
    global var_countOTU
    var_countOTU=nodeIdGenerator(prefix='', starting_id=1)
    print('Parsing PhenoScript file ...', flush=True)
    print('The following OTUs found:', flush=True)
    out=grammar1.parseString(txt)
    #print(out)
    
    # to PhenoScript xml
    print('Converting PhenoScript to XML ...', flush=True)
    out_xml=phenoscriptParse(out, instance_IRI)
    #print(out_xml)
    
    #-----------------------------------------
    # Take phs XML and translate terms to IRIs
    #-----------------------------------------
    # get phs Dictionary
    print('Reading in PhenoScript Dictionary ...', flush=True)
    fl=file_phsDic
    iriDic=labels2IRI(fl)
    #iriDic.translate('bearer_of')
    
    # read from string and translate
    print('Translating terms to IRIs ...', flush=True)
    doc = ET.fromstring(out_xml)
    tree = ET.ElementTree(doc)
    ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
    root1 = tree.getroot()
    translatePhs(root1, iriDic)
    print('Saving file ...', flush=True)
    tree.write(xml_out, encoding="utf-8")
    print('DONE! The instances are saved to:', xml_out, flush=True)



