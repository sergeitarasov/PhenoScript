# /Users/taravser/anaconda3/envs/PhenoScript/bin/python

from owlready2 import *
import os

set_log_level(9)

onto_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phenoscript.owl'
owl_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test_temp.owl'

onto = get_ontology(onto_file).load()

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)



# with tempfile.NamedTemporaryFile() as f:
#     onto.save(file=f.name, format="rdfxml")
#     # print("Ontology saved to:", f.name)
#     f.close()
#     onto.destroy()
#     onto = get_ontology(f.name).load()


temp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
onto.save(file=temp.name, format="rdfxml")
temp.close()
onto.destroy()
onto = get_ontology(temp.name).load()
os.unlink(temp.name)


temp.name

onto.save(file = owl_file, format = "rdfxml")