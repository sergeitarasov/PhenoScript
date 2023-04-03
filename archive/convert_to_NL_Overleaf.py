from owlready2 import *
import markdown

# ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/"
# ontoFile="my_instance.owl"

# ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/Semantic_Descriptions/Gryonoides/output/"
# ontoFile="my_gryo.owl"

ontoPath='/Users/taravser/Documents/My_papers/pheno-repo/Phenoscript/phs_output/'
ontoFile='bees.owl'
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
inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")
pato= onto.get_namespace("http://purl.obolibrary.org/obo/pato#")




# does not work
#Obo = onto.get_namespace("http://purl.obolibrary.org/OBO/")
#Obo.BFO_0000051
#-------------------------------


# add absence
for ind in onto.individuals():
    print(ind)
    if (len(ind.PhenoScript_implies_absence_of)>0):
        #print(ind, "---", ind.PhenoScript_implies_absence_of)
        abs_class=ind.PhenoScript_implies_absence_of[0]
        txt=" [%s](%s): absent" % (abs_class.label.first(), abs_class.iri)
        print(txt)
        ind.PhenoScript_NL.append(txt)

# SPARQL
#----------------


# female_organism:G_brasiliensis > abdominal_tergum_5:T5_brasiliensis > medial_region:medr5_brasiliensis >> length .is_quality_measured_as measurement_datum:medr5m_brasiliensis .has_measurement_unit_label length << abdominal_tergum_5:T5_brasiliensis;
# female_organism:G_brasiliensis > measurement_datum:medr5m_brasiliensis .has_measurement_value 0.75;

obo.RO_0000053.iri
obo.RO_0000053.label

# obo.PATO_0000122 # length
# obo.RO_0000053 # has_characterristi
# obo.IAO_0000417 # is qual measured as
# obo.IAO_0000004 # has measurement value
# obo.IAO_0000039 # has measurement unit label
# obo.RO_0000052 # characteristic of
query=list(default_world.sparql("""
           SELECT ?E0 ?Q ?Val ?x ?Unit ?Unit_loc
           WHERE {?E0 obo:RO_0000053 ?Q .
            ?Q obo:IAO_0000417 ?x .
            ?x obo:IAO_0000004 ?Val .
            ?x obo:IAO_0000039 ?Unit .
            optional {
                ?Unit obo:RO_0000052 ?Unit_loc .
                }
            }
"""))



query

for item in query:
    print(item[0])


#dict_templ={"E0":None, "Q":None, "Val":None, "x":None, "Unit":None, "Unit_loc":None}
sparql=[]
for item in query:
    print(item)
    dict_templ = {"E0": None, "Q": None, "Val": None, "x": None, "Unit": None, "Unit_loc": None}
    dict_templ['E0']= item[0]
    dict_templ['Q'] = item[1]
    dict_templ['Val'] = item[2]
    dict_templ['x'] = item[3]
    dict_templ['Unit'] = item[4]
    if len(item)==6:
        dict_templ['Unit_loc'] = item[5]
    sparql.append(dict_templ)

sparql


for item in sparql:
    print(item['E0'])

# --- Create annotations

def getLabelPhsAnnotation(ind):
    if ind is not None:
        return "[%s](%s)" % (ind.PhenoScript_original_class[0].label.first(), ind.PhenoScript_original_class[0].iri)

def render_Unit_loc(ind):
    if ind is not None:
        # return " of " + ind.PhenoScript_original_class[0].label.first() + ";"
        return " of [%s](%s);" % (ind.PhenoScript_original_class[0].label.first(), ind.PhenoScript_original_class[0].iri)
    else:
        return ";"

for item in sparql:
    # Q of E0 = Val, measured in Unit of Unit_loc.
    # Q(L)=Val, unit: Unit(Unit_loc)
    #print(item)
    #txt="%s of %s = %s, unit: %s%s" % \
    txt = " %s = %s, unit: %s%s" % \
    (getLabelPhsAnnotation(item['Q']),
    #getLabelPhsAnnotation(item['E0']),
    item['Val'],
    getLabelPhsAnnotation(item['Unit']),
    render_Unit_loc(item['Unit_loc']))
    print(txt)
    # inf.PhenoScript_NL
    item['E0'].PhenoScript_NL.append(txt)
    print("NL:", item['E0'].PhenoScript_NL)



## DELETE
sparql

def destroy_entitieS(list):
    for entity in list:
        destroy_entity(entity)


for item in sparql:
    destroy_entitieS([item['Q'], item['Unit']])
    if item['x'] is not None:
        print(item['x'])
        destroy_entity(item['x'])


# --- Present queries:
# obo.BFO_0000051 has part

#FILTER NOT EXISTS { ?y owl:ObjectProperty ?z }

query=list(default_world.sparql("""
           SELECT ?x ?y
           WHERE {
            ?x a owl:NamedIndividual .
            ?y a owl:NamedIndividual .
            ?x obo:BFO_0000051 ?y .
            }
"""))

# RO_0002201 # phenotype of
# every node that should be marks with 'prsent' does not have any single node that is PhenoScript_original_assertion or inf.PhenoScript_NL
# so if node has those assertions it is not our customer. we look for those that have no
presesnt_tag=set()
for trip in query:
    n1=trip[0]
    n2=trip[1]
    has_out_edge=False
    for prop in n2.get_properties():
        if not issubclass(prop, obo.RO_0002201):
            for n3 in prop[n2]:
                asrt = inf.PhenoScript_original_assertion[n2, prop, n3]
                if len(asrt)>0 or issubclass(prop, inf.PhenoScript_NL):
                    #if issubclass(prop, owl.ObjectProperty) or issubclass(prop, owl.DatatypeProperty):
                    #print(n2, prop, "is", asrt)
                    has_out_edge = True
    if has_out_edge == False:
        print(n2, prop, "is", asrt)
        presesnt_tag.add(n2)



for ind in presesnt_tag:
    txt = ": present"
    print(ind, txt)
    ind.PhenoScript_NL.append(txt)

#---------------------

spp=obo.CDAO_0000138.instances()
focal_sp=spp[0]
focal_org = focal_sp.IAO_0000219[0]

parts_org=focal_org.BFO_0000051

# taxon name
for i in focal_sp.IAO_0000219:
    print(i, i.is_a)
    if (len(i.is_a[0].has_rank) > 0):
        sp_name = '# ' +  i.is_a[0].label.first() + '\n\n'


# DD is the final description
DD = ''
visited_triples=list()
for ind in parts_org:
    xx = traverseOntoMark_Overleaf(ind, visited_nodes=set())
    if not xx == ';':
        DD = DD + (str(renderNL(ind))+xx) + '\n'
        print(str(renderNL(ind))+xx)

print(DD)
type(DD)
len(DD)
xx = DD.replace("\t [", "\t- [")
xx = xx.replace("\n [", "\n- [")
xx = '-'+xx
xx = sp_name + xx
print(xx)



# --- Save
#DD_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/Semantic_Descriptions/Gryonoides/NL/out.txt'
DD_file = '/Users/taravser/Documents/My_papers/pheno-repo/Phenoscript/NL/bees.md'
file1 = open(DD_file, "w+")
file1.writelines(xx)
file1.close()


# to markdown
markdown.markdownFromFile(input=DD_file, output='/Users/taravser/Documents/My_papers/pheno-repo/Phenoscript/NL/bees.html')



def traverseOntoMark_Overleaf(ind0, tabs="\t", visited_nodes=set()):
    global visited_triples
    #print(visited_triples)
    txt=""
    visited_nodes.add(ind0)
    triples=[]
    for prop in ind0.get_properties():
        if not issubclass(prop, owl.AnnotationProperty):
            #print(prop)
            for value in prop[ind0]:
                asrt=inf.PhenoScript_original_assertion[ind0, prop, value]
                triple = [ind0, prop, value]
                if len(asrt) > 0 and (triple not in visited_triples): # should be also True for asrt
                    #triple = [ind0, prop, value]
                    #print(asrt)
                    triples.append(triple)
                    visited_triples.append(triple)
        #elif issubclass(prop, inf.PhenoScript_NL) or issubclass(prop, inf.PhenoScript_implies_absence_of):
        elif issubclass(prop, inf.PhenoScript_NL):
            for value in prop[ind0]:
                triple = [ind0, prop, value]
                if (triple not in visited_triples):
                    #triple = [ind0, prop, value]
                    triples.append(triple)
                    visited_triples.append(triple)
    if len(triples)==1:
        prop=triples[0][1]
        value=triples[0][2]
        #txt = txt + (" <%s> %s" % (prop, value))
        txt = txt + ("%s%s" % (renderNL(prop), renderNL(value)))
        if issubclass(prop, owl.ObjectProperty) and (value not in visited_nodes):
            #print(traverseOnto(value))
            #visited_nodes.add(value)
            txt = txt + traverseOntoMark_Overleaf(value, tabs=tabs, visited_nodes=visited_nodes)
        return  txt
    if len(triples) > 1:
        for trip in triples:
            # trip= triples[0]
            prop = trip[1]
            value = trip[2]
            #txt = txt +"\n" + tabs + ("%s <%s> %s" % (ind0, prop, value))
            txt = txt + "\n" + tabs + ("%s%s%s" % (renderNL(ind0), renderNL(prop), renderNL(value)))
            if issubclass(prop, owl.ObjectProperty) and (value not in visited_nodes):
                txt = txt + traverseOntoMark_Overleaf(value, tabs=tabs+"\t", visited_nodes=visited_nodes)
        return txt
    if len(triples) == 0:
        return ";"


def renderNL(x):
    # if x is individual
    if isinstance(x, owl.Thing):
        return " [%s](%s)" % (x.PhenoScript_original_class[0], x.PhenoScript_original_class[0].iri)
    elif issubclass(x, owl.ObjectProperty) or issubclass(x, owl.DatatypeProperty):
        dict={obo.BFO_0000051 :',', obo.BFO_0000050 : ' of', obo.RO_0000053 : ':', obo.RO_0000052 : ' of', pato.increased_in_magnitude_relative_to : ' larger than',  pato.decreased_in_magnitude_relative_to : ' smaller than'}
        if x in dict:
            return dict[x]
        else:
            return " [%s](%s)" % (x.label.first(), x.iri)
    elif issubclass(x, owl.AnnotationProperty):
        return ""
    elif isinstance(x, (int, float)):
        return " %s" % str(x)
    elif isinstance(x, str):
        return x