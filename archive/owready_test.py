from owlready2 import *
import uuid


#-----------------------
# Arguments
#-----------------------

ontoPath = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/data'
ontoFile = 'colao_merged.owl'

#--- Read in Ontology
set_log_level(9)
onto_path.append(ontoPath)
onto = get_ontology(ontoFile)
onto.load(reload_if_newer=True)
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")

# rendering
def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)


# list of classes
for i in onto.classes():
    print(i.iri)

# list of properties
for i in onto.properties():
    print(i.iri)

#------ creating new instance

# obo.IAO_0000219 denotes
# obo.CDAO_0000138 TU
# obo.UBERON_0000468 multicellurlar organism
# obo.BFO_0000051 has part

UUID = str(uuid.uuid1())
N1=obo.UBERON_0000468(UUID)
N1.label='my fist instance'
UUID = str(uuid.uuid1())
N2 = obo.CDAO_0000138(UUID)
N2.label='my instance 2'
N1.IAO_0000219.append(N2)


outputFile = '/Users/taravser/Documents/My_papers/Phenex_Coleo/Jennifer/onto_test.owl'
onto.save(file = outputFile, format = "rdfxml")
