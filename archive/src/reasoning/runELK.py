#!/usr/bin/env python

import os
import tempfile
from os import path
from pathlib import Path
from os import path
import shutil

#-------- Arguments
#PATH_TO_ELK="/Applications/ELK/elk.jar"

#-----------

# #python runELK.py -i /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance.owl  -o /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/out_ELK.owl
# parser = argparse.ArgumentParser(description='Reasoning with ELK',
#                                  usage='python phs.py -onto Onto.owl -phs PhS.phs  -o ./result -pre some_pref \n OR ./phs.py ... [if executable]',
#                                  epilog="To automatically install required packages use 'python src/setup.py'"
#                                  )
#
# parser.add_argument("-i",  "--input", help="input ontology", required=True)
# parser.add_argument("-o", "--output",  help="output ontology", required=True)
# args = parser.parse_args()

def runELK(input, output, merge=True, PATH_TO_ELK="/Applications/ELK/elk.jar"):
    #rootPath = os.path.dirname(os.path.realpath(__file__))
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = Path(tmpdirname)
        print(temp_dir, temp_dir.exists())

    file1 = path.join(temp_dir, 'phs_robot.ofn')
    file2 = path.join(temp_dir, 'phs_elk_out.ofn')
    #file3 = path.join(temp_dir, 'phs_merged.ofn')
    #
    # 1. convert using robot from owl to ofn since ELK uses ofn
    # robot convert --input my_instance_phs.owl --output my_instance_phs.ofn
    print('running ROBOT: from owl to ofn\n')
    com1 = 'robot convert --input ' + input + ' --output ' + file1
    os.system(com1)

    # 2. run ELK
    print('running ELK\n')
    # java -jar elk-standalone.jar -i my_instance_phs.ofn --realize -o taxonomy.owl
    com1 = 'java -jar ' + PATH_TO_ELK + ' -i ' + file1 + ' --realize' + ' -o ' + file2
    os.system(com1)

    # 3. Back from own to OWL
    print('running ROBOT: from ofn to OWL\n')
    if merge==True:
        print('running ROBOT: merging input with ELK output\n')
        com1 = 'robot merge --input ' + file2 + ' --input ' + input + ' --output ' + output
        print(com1)
        os.system(com1)
    else:
        com1 = 'robot convert --input ' + file2 + ' --output ' + output
        print(com1)
        os.system(com1)
    print('DONE!\n')
    # Remove temp dir
    shutil.rmtree(temp_dir)













