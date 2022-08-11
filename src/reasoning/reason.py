from owlready2 import *
import types
import warnings
#import pdb # pdb.set_trace()
exec(open("./src/reasoning/runELK.py").read())
exec(open("./src/reasoning/pyFunctions.py").read())
#-----------------------
# Arguments
#-----------------------
ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/"
#onto_path.append(ontoPath)
ontoFile="my_instance.owl"

#--
def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
# set_render_func(render_using_iri)
# set_render_func()
set_log_level(9)
#-----------------------

# additional (default) Args
phs='{https://github.com/sergeitarasov/PhenoScript}'
ns = {'phs': 'https://github.com/sergeitarasov/PhenoScript'}


print('Reading data...\n')

#--- Read in Ontology
onto_path.append(ontoPath)
onto = get_ontology(ontoFile)
onto.load(reload_if_newer=True, reload=True)
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
#-------------------------------

#--------------------
# BFO_0000051 has_part
# BFO_0000050 part_of
# AISM_0000078 encircles
# AISM_0000079 encircled_by
#
#--------------------
#--- REASONING
topClass=obo.AISM_0000174
#obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")

with inf:
    class phs_Reasoning(Thing): pass
    class phs_Implies_Presence(phs_Reasoning): pass
    class phs_Implies_Absence(phs_Reasoning): pass

# New annotation props
with inf:
    class negates(AnnotationProperty): pass
    class phs_implies(AnnotationProperty): pass

inf.negates
inf.phs_implies

presSuperClasses = [phs_Implies_Presence]
absSuperClasses = [phs_Implies_Absence]
# x = topClass.descendants(include_self = False)
# i = next(iter(x))
for i in topClass.descendants(include_self = False):
    #print(i.label.first())
    lab=i.label.first()
    lab=lab.replace(" ", "_")
    with inf:
        # presence
        presClass = types.new_class("implies_presence_of_"+lab, tuple(presSuperClasses))
        presClass.label="implies_presence_of_"+lab
        presClass.equivalent_to.append(obo.BFO_0000051.some(i) )
        presClass.equivalent_to.append(obo.BFO_0000050.some(i))
        #
        presClass.equivalent_to.append(obo.AISM_0000078.some(i))
        presClass.equivalent_to.append(obo.AISM_0000079.some(i))
        #
        #presClass.equivalent_to.append(i)
        #
        # absences
        absClass = types.new_class("implies_absence_of_"+lab, tuple(absSuperClasses))
        absClass.label="implies_absence_of_"+lab
        absClass.equivalent_to.append( Not(obo.BFO_0000051.some(i) ) )
        absClass.equivalent_to.append(Not(obo.AISM_0000078.some(i)))
        #N2.is_a.append(obo.BFO_0000051.some(Not(obo.BFO_0000051.some(obo.HAO_0001017))))
        # annotation
        absClass.negates.append(presClass)
        absClass.phs_implies=['absence']
        presClass.negates.append(absClass)
        presClass.phs_implies = ['presence']

# turn off and on inverse
turnOffInverse(prop=obo.BFO_0000050, propInv=obo.BFO_0000051, ontoObj=onto)
turnOffInverse(prop=obo.AISM_0000078, propInv=obo.AISM_0000079, ontoObj=onto)


onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs.owl', format = "rdfxml")


runELK(input='./output/my_instance_phs.owl', output='./output/my_instance_phs_REASON.owl', PATH_TO_ELK="/Applications/ELK/elk.jar")

# # merge
# com='robot merge --input /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs_REASON1.owl ' \
#     '--input /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs.owl ' \
#     '--output /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs_REASON1.owl'
# os.system(com)

#------------- STEP 2

onto.destroy()
#--- Read in Ontology
ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/"
onto_path.append(ontoPath)
ontoFile2="my_instance_phs_REASON.owl"
onto2 = get_ontology(ontoFile2)
onto2.load(reload=True)
#onto2.imported_ontologies.append(onto)
obo2 = onto2.get_namespace("http://purl.obolibrary.org/obo/")
inf2=onto2.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")
#-------------------------------

len(list(inf2.phs_Implies_Presence.subclasses()))
presSubClasses=list(inf2.phs_Implies_Presence.subclasses())
ccount=0
for i in presSubClasses:
    neg_i=i.negates.first()
    print(ccount, i, '::', neg_i)
    ccount = ccount + 1
    #list(i.subclasses())
    #for i_subclass in i.subclasses():
    listDescendants=list(i.descendants(include_self=False))
    for i_subclass in listDescendants:
        #print(i_subclass)
        if (i_subclass.phs_implies == ['presence']):
            neg_i_subclass=i_subclass.negates.first()
            print('\t', i, '<Superclass of>', i_subclass, '-->', neg_i, '<Subclass of>', neg_i_subclass)
            try:
                if not issubclass(neg_i, neg_i_subclass):
                    print('Not subbl')
                    neg_i.is_a.append(neg_i_subclass)
                else:
                    print('!!!!!!!! IS subbl')
            except:
                warnings.warn('Negate classes')
                pass
    print("Done!")



#-------------------------

onto2.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs_REASON2.owl', format = "rdfxml")

runELK(input='./output/my_instance_phs_REASON2.owl', output='./output/my_instance_phs_REASON2.owl', PATH_TO_ELK="/Applications/ELK/elk.jar")


#--- Read in Ontology
#onto_path.append(ontoPath)
onto2.destroy()
ontoFile2="my_instance_phs_REASON2.owl"
onto2 = get_ontology(ontoFile2)
onto2.load(reload=True)
obo2 = onto2.get_namespace("http://purl.obolibrary.org/obo/")
inf2=onto2.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")
#-------------------------------

ins=[]
for i in onto2.individuals():
    ins.append(i)
    print(i, i.INDIRECT_is_a)




