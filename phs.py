#!/usr/bin/env python

import argparse
from os import path
from pathlib import Path
from owlready2 import *

#import types
#import pdb # pdb.set_trace()


#  python phs.py -onto data/ontologies/colao_merged.owl -phs data/phs/colao_AP.phs  -o ./out -pre colao
#  ./phs.py -onto data/ontologies/colao_merged.owl -phs data/phs/colao_AP.phs  -o ./out -pre colao
parser = argparse.ArgumentParser(description='Convert PhenoScript to OWL',
                                 usage='python phs.py -onto Onto.owl -phs PhS.phs  -o ./result -pre some_pref \n OR ./phs.py ... [if executable]',
                                 epilog="To automatically install required packages use 'python src/setup.py'"
                                 )

parser.add_argument("-onto",  "--onto", help="input ontology", required=True)
parser.add_argument("-phs", "--phs",  help="input PhenoScript file", required=True)
parser.add_argument("-o", "--output", type=Path, default=Path(__file__).absolute().parent, help="output directory: use ./dir for relative path")
parser.add_argument("-pre", "--pref", default='phs_output', help="prefix for output files: Phenoscript XML and ontology files")
args = parser.parse_args()

#print(os.path.dirname(os.path.realpath(__file__)))
# print(args.onto)
# print(args.phs)
# print(args.output)
# print(args.pref)

# -----------------------------------------
# Necessary variables
# -----------------------------------------
rootPath=os.path.dirname(os.path.realpath(__file__))
#path_src="./src/"
path_src=path.join(rootPath, "src/")

# Check whether the output dir exists or not
# Create a new directory if it does not exist
isExist = os.path.exists(args.output)
if not isExist:
    os.makedirs(args.output)


# -----------------------------------------
# From phs to Phenoscript XML
# -----------------------------------------
# Read global arguments
exec(open(rootPath+"/phs_Global_Args.txt").read())
# Read phs to Phenoscript XML
exec(open(path_src+"phs_init.py").read())


file_phsDic = path.join(PATH_TO_ATOM, 'phs_dictionary.csv')
xml_out = path.join(args.output, args.pref + '.xml')
#print(xml_out)
PhenoScriptToXML(file_phs=args.phs, file_phsDic=file_phsDic, xml_out=xml_out, instance_IRI=INSTANCE_IRI)


# -----------------------------------------
# From Phenoscript XML to OWL
# -----------------------------------------
phsXML= xml_out
ontoPath= args.onto.rsplit('/', 1)[0]
ontoFile= args.onto.rsplit('/', 1)[-1]
outputFile=path.join(args.output, args.pref + '.owl')

exec(open(path_src+"phsToOntology.py").read())
