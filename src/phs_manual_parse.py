import os
from pathlib import Path

os.getcwd()
#os.chdir('./src')

path_src="./src/"

exec(open(path_src+"phs_xml.py").read())
exec(open(path_src+"phs_parser.py").read())
exec(open(path_src+"phs_lbs2iri.py").read())


#txt = Path('data/Gryonoides.phs').read_text()
txt = Path('data/test.phs').read_text()

# check if brackets are balanced
isBalanced(txt)

# parse
# count read OTU objects
global var_countOTU
var_countOTU=nodeIdGenerator(prefix='', starting_id=1)
out=grammar1.parseString(txt)
#print(out)

# to PhenoScript xml
out_xml=phenoscriptParse(out, instance_IRI='https://orcid.org/0000-0001-5237-2330/')
print(out_xml)

# save PhenoScript xml
#print(out_xml, file=open('results/phs_Gryo.xml','w'))
print(out_xml, file=open('results/phs_test.xml','w'))

#---- Translate IRIs
# get phs Dictionary
fl='results/dictionary/Gryo_dic.csv'
iriDic=labels2IRI(fl)
#iriDic.translate('bearer_of')

# read from string and translate
doc = ET.fromstring(out_xml)
tree = ET.ElementTree(doc)
ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
root1 = tree.getroot()
translatePhs(root1, iriDic)
#tree.write('phs_Gryo.xml', encoding="utf-8")
tree.write('results/phs_test_translated.xml', encoding="utf-8")

# # read in file and translate
# tree = ET.parse('results/phs_Gryo.xml')
# ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
# root1 = tree.getroot()
# translatePhs(root1, iriDic)
# tree.write('phs_Gryo.xml', encoding="utf-8")




