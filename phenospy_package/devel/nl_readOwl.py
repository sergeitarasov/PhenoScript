# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

import sys
sys.path.append('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy')
import markdown
from owl_owlready_config import *


# -----------------------------------------
# Arguments
# -----------------------------------------
set_log_level(9)
# ontoFile='/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/examples/Grebennikovius/output/Grebennikovius.owl'
# onto = get_ontology(ontoFile).load(reload_if_newer=True, reload=True)

# -----------------------------------------
# Namespaces
# -----------------------------------------
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')

# -----------------------------------------
# Helpers
# -----------------------------------------

phenoscript_annotations = IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000001']
phs_implies_absence_of  = IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000003']
phs_NL                  = IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000004']
phs_original_assertion  = IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000005']
phs_original_class      = IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000002']

phenoscript_annotations.python_name = 'phenoscript_annotations'
phs_implies_absence_of.python_name  = 'phs_implies_absence_of'
phs_NL.python_name                  = 'phs_NL'
phs_original_assertion.python_name  = 'phs_original_assertion'
phs_original_class.python_name      = 'phs_original_class'