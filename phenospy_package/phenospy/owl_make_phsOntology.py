
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()
from owl_xml2owl_fun import *


onto_phs = get_ontology('https://github.com/sergeitarasov/PhenoScript')


with onto_phs:
    class Phenoscript_annotations(AnnotationProperty): pass
    class PhenoScript_original_class(Phenoscript_annotations): pass
    class PhenoScript_implies_absence_of(Phenoscript_annotations): pass
    class PhenoScript_NL(Phenoscript_annotations): pass
    class PhenoScript_original_assertion(Phenoscript_annotations): pass


# onto_phs.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phenoscript.owl', format = "rdfxml")