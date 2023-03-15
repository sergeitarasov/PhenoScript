
from owlready2 import *
import types
import warnings
from igraph import *
import matplotlib
from pyvis.network import Network
import networkx as nx

# ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/"
# ontoFile="my_instance.owl"

ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/Semantic_Descriptions/Gryonoides/output/"
ontoFile="my_gryo.owl"

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


#--------------------------
# Functions
#--------------------------

def tag2print(ind):
    if (ind.label.first() is not None):
        return ind.label.first()
    else:
        return ind.python_name

def getExtraInverseProps(ind):
    inv_props = []
    for inv in ind.get_inverse_properties():
        inv_props.append(inv[1].inverse)
    return inv_props


#--------------------------


#---- simple printing
ccount=0
for ind in onto.individuals():
    for prop in ind.get_properties():
        for value in prop[ind]:
            if (owl.AnnotationProperty not in prop.is_a):
                print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                ccount+=1
    print("\n")



#----- !!! Deactivate inverse properties
objPropsPairs=[]
for prop in onto.object_properties():
    print(prop, "<->", prop.inverse)
    objPropsPairs.append([prop, prop.inverse])
    if prop.inverse is not None:
        #print('YES')
        prop.inverse=[]

for prop in onto.object_properties():
    print(prop, "<->", prop.inverse)

#-----


# obo.UBERON_0007023.instances() # adult organism
# obo.CDAO_0000138.instances()
# obo.RO_0002200 # has phenotype
# obo.IAO_0000219 # denotes
spp=obo.CDAO_0000138.instances()
focal_sp=spp[0]
to_remove= focal_sp.IAO_0000219
focal_sp_phenotypes=[]
for i in focal_sp.RO_0002200:
    if i not in to_remove:
        focal_sp_phenotypes.append(i)

onto_net= Network(height='100%', width='100%', directed =True)
onto_net.barnes_hut()
nodes={}
edge_list=[]
edges=[]
ccount=0
id_data_node=0
# issubclass(prop, owl.ObjectProperty)
# owl.ObjectProperty in prop.is_a
# ind = focal_sp_phenotypes[0]
# ind =IRIS["https://orcid.org/0000-0001-5237-2330/17-08-2022-14-14-24/T4_brasiliensis"]


#for ind in onto.individuals():
for ind in focal_sp_phenotypes:
    print(ind)
    inv_props = getExtraInverseProps(ind)
    if ind not in nodes:
        nodes[ind] = len(nodes)
        onto_net.add_node(nodes[ind], label=ind.label.first())
    for prop in ind.get_properties():
        print("Working on:", prop)
        #prop=list(ind.get_properties())[0]
        #if (prop not in inv_props) and not issubclass(prop, owl.AnnotationProperty):
        if (prop not in inv_props):
            # If ObjectProperty
            if issubclass(prop, owl.ObjectProperty):
                for value in prop[ind]:
                    print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                    ccount += 1
                    if ind not in nodes:
                        nodes[ind]=len(nodes)
                        onto_net.add_node(nodes[ind], label=ind.label.first())
                    if value not in nodes:
                        nodes[value]=len(nodes)
                        onto_net.add_node(nodes[value], label=value.label.first())
                    edge_list.append([nodes[ind], nodes[value]])
                    edges.append(tag2print(prop))
                    print('adding edge')
                    onto_net.add_edge(nodes[ind], nodes[value], label="<" + tag2print(prop) + ">", color="#0000FF")
            # If DatatypeProperty
            elif issubclass(prop, owl.DatatypeProperty):
                for value in prop[ind]:
                    print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                    ccount += 1
                    if ind not in nodes:
                        nodes[ind]=len(nodes)
                        onto_net.add_node(nodes[ind], label=ind.label.first())
                    if isinstance(value, (int, float)):
                        data_value=value
                        value="_dn_" + str(id_data_node) + "="+ str(data_value)
                        nodes[value]=len(nodes)
                        onto_net.add_node(nodes[value], label=str(data_value))
                        id_data_node+=1
                    edge_list.append([nodes[ind], nodes[value]])
                    edges.append(tag2print(prop))
                    print('adding edge')
                    onto_net.add_edge(nodes[ind], nodes[value], label="<" + tag2print(prop) + ">", color="#0000FF")
            # If AnnotationProperty for Phenoscript
            #elif issubclass(prop, inf.Penoscript_annotations):
            elif issubclass(prop, inf.PhenoScript_implies_absence_of):
                for value in prop[ind]:
                    # for annotations value is iri, convert it to class
                    # value=IRIS[value]
                    print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                    ccount += 1
                    if ind not in nodes:
                        nodes[ind]=len(nodes)
                        onto_net.add_node(nodes[ind], label=ind.label.first())
                    if value not in nodes:
                        value = "_an_" + str(id_data_node) + "_" + str(value)
                        nodes[value]=len(nodes)
                        onto_net.add_node(nodes[value], label=str(value))
                    edge_list.append([nodes[ind], nodes[value]])
                    edges.append(tag2print(prop))
                    print('adding edge')
                    onto_net.add_edge(nodes[ind], nodes[value], label="<" + tag2print(prop) + ">", color="#0000FF")
            else:
                print("NOT FOUND:", prop)


nodes
edge_list
edges

index_remove=[]
for i in range(0, len(edges)):
    #print(i)
    if edges[i]=='part of':
        #print(edge_list[i])
        rev=[edge_list[i][1], edge_list[i][0]]
        if rev in edge_list:
            print(edge_list[i], "<->", rev)
            index_remove.append(i)

edge_list = [ele for idx, ele in enumerate(edge_list) if idx not in index_remove]
edges = [ele for idx, ele in enumerate(edges) if idx not in index_remove]


#-- SAVE

onto_net.show(ontoPath+'onto_net.html')


#import matplotlib.pyplot as plt
#plt.show()

igraph_nodes=[]
for n in nodes:
    print(str(n))
    igraph_nodes.append(n)

g = Graph(edges=edge_list,  directed=True)
#g.vs['label'] = igraph_nodes
g.vs['label'] = list(nodes)
g.es['label'] = edges
plot(g, ontoPath+"onto_graph.png")
#g.save("output/onto_graph.gml", format="graphml")

g_comps=g.clusters(mode='weak')
plot(g_comps, ontoPath+"onto_graph.png")
g.summary(verbosity=1)

for i in g_comps:
    print(i)

for i in g_comps.subgraphs():
    print(i)


plot(g_comps.subgraphs()[0], ontoPath+"onto_graph_CYCLE.png")

comps_sorted=[]
for i in g_comps.subgraphs():
    print(i)
    sort=i.topological_sorting(mode='out')
    print(sort)
    print(i.vs['label'])
    #
    labels_sorted=i.vs['label']
    labels_sorted = [labels_sorted[i] for i in sort]
    comps_sorted.append(labels_sorted)
    print(labels_sorted)

components=comps_sorted[0]
ind0=components[0]
ind0=components[1]
xx=traverseOnto(components[0])
print(xx)
print(str(ind0) + xx)

starting_entity=comps_sorted[0][0]
traverseOnto(starting_entity)
ind0=starting_entity

#--------------------------------------------
#--------------------- NEW TRAVERSE

txt = "%s = %s, unit: %s%s" % \
      (getLabelPhsAnnotation(item['Q']),
       # getLabelPhsAnnotation(item['E0']),
       item['Val'],
       getLabelPhsAnnotation(item['Unit']),
       render_Unit_loc(item['Unit_loc']))
print(txt)
# inf.PhenoScript_NL
item['E0'].PhenoScript_NL.append(txt)


#--- add absence
for ind in onto.individuals():
    #print(ind)
    if (len(ind.PhenoScript_implies_absence_of)>0):
        #print(ind, "---", ind.PhenoScript_implies_absence_of)
        abs_class=ind.PhenoScript_implies_absence_of[0]
        txt=" %s: absent" % (abs_class.label.first())
        print(txt)
        ind.PhenoScript_NL.append(txt)



#_----
spp=obo.CDAO_0000138.instances()
focal_sp=spp[0]
focal_org = focal_sp.IAO_0000219[0]

parts_org=focal_org.BFO_0000051

# inf.PhenoScript_original_assertion[N1, Ed, N2] = True
for part in parts_org:
    ass=inf.PhenoScript_original_assertion[focal_org, obo.BFO_0000051, part]
    print(part, ass)
    if len(ass)==0:
        print(part, ass)

for i in onto.annotation_properties():
    print(i)

len(parts_org)
len(set(parts_org))
ind0=parts_org[20]

#PhenoScript_original_assertion
#inf.PhenoScript_original_class[focal_sp, obo.IAO_0000219, focal_org ] = "org assert"
#inf.PhenoScript_original_class[focal_sp, obo.IAO_0000219, focal_org ]

visited_triples=list()

for ind in parts_org:
    xx = traverseOnto(ind, visited_nodes=set())
    print(str(ind), xx)

visited_triples=list()
for ind in parts_org:
    xx = traverseOnto(ind, visited_nodes=set())
    if not xx == ';':
       print(str(renderNL(ind))+xx)

    #print(str(ind), xx)

ind0=query[0][0]
ind0=ind

def traverseOnto(ind0, tabs="\t", visited_nodes=set()):
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
            txt = txt + traverseOnto(value, tabs=tabs, visited_nodes=visited_nodes)
        return  txt
    if len(triples) > 1:
        for trip in triples:
            # trip= triples[0]
            prop = trip[1]
            value = trip[2]
            #txt = txt +"\n" + tabs + ("%s <%s> %s" % (ind0, prop, value))
            txt = txt + "\n" + tabs + ("%s%s%s" % (renderNL(ind0), renderNL(prop), renderNL(value)))
            if issubclass(prop, owl.ObjectProperty) and (value not in visited_nodes):
                #print(traverseOnto(value))
                #print("tabs")
                #visited_nodes.add(value)
                txt = txt + traverseOnto(value, tabs=tabs+"\t", visited_nodes=visited_nodes)
        return txt
    if len(triples) == 0:
        return ";"

x=value
x=obo.BFO_0000051
x='ada'
renderNL(x)
renderNL(Incr)


def renderNL(x):
    # if x is individual
    if isinstance(x, owl.Thing):
        return " %s" % x.PhenoScript_original_class[0]
    elif issubclass(x, owl.ObjectProperty) or issubclass(x, owl.DatatypeProperty):
        dict={obo.BFO_0000051 :',', obo.BFO_0000050 : ' of', obo.RO_0000053 : ':', obo.RO_0000052 : ' of', pato.increased_in_magnitude_relative_to : ' larger than',  pato.decreased_in_magnitude_relative_to : ' smaller than'}
        if x in dict:
            return dict[x]
        else:
            return " %s" % x.label.first()
    elif issubclass(x, owl.AnnotationProperty):
        return ""
    elif isinstance(x, (int, float)):
        return " %s" % str(x)
    elif isinstance(x, str):
        return x



#----------------------------------------------

onto_net= Network(height='100%', width='100%', directed =True)
onto_net.barnes_hut()
nodes={}
edge_list=[]
edges=[]
ccount=0
id_data_node=0
# issubclass(prop, owl.ObjectProperty)
# owl.ObjectProperty in prop.is_a
for ind in onto.individuals():
    print(ind)
    inv_props = getExtraInverseProps(ind)
    for prop in ind.get_properties():
        if (prop not in inv_props) and not issubclass(prop, owl.AnnotationProperty):
            # If ObjectProperty
            if issubclass(prop, owl.ObjectProperty):
                for value in prop[ind]:
                    print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                    ccount += 1
                    if ind not in nodes:
                        nodes[ind]=len(nodes)
                        onto_net.add_node(nodes[ind], label=ind.label.first())
                    if value not in nodes:
                        nodes[value]=len(nodes)
                        onto_net.add_node(nodes[value], label=value.label.first())
                    edge_list.append([nodes[ind], nodes[value]])
                    edges.append(tag2print(prop))
                    print('adding edge')
                    onto_net.add_edge(nodes[ind], nodes[value], label="<" + tag2print(prop) + ">", color="#0000FF")
            # If DatatypeProperty
            elif issubclass(prop, owl.DatatypeProperty):
                for value in prop[ind]:
                    print("%s. %s [%s] %s" % (ccount, ind, tag2print(prop), value), prop.is_a)
                    ccount += 1
                    if ind not in nodes:
                        nodes[ind]=len(nodes)
                        onto_net.add_node(nodes[ind], label=ind.label.first())
                    if isinstance(value, (int, float)):
                        data_value=value
                        value="_dn_" + str(id_data_node) + "="+ str(data_value)
                        nodes[value]=len(nodes)
                        onto_net.add_node(nodes[value], label=str(data_value))
                        id_data_node+=1
                    edge_list.append([nodes[ind], nodes[value]])
                    edges.append(tag2print(prop))
                    print('adding edge')
                    onto_net.add_edge(nodes[ind], nodes[value], label="<" + tag2print(prop) + ">", color="#0000FF")
            else:
                print("NOT FOUND")

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
        return ind.PhenoScript_original_class[0].label.first()

def render_Unit_loc(ind):
    if ind is not None:
        return " of " + ind.PhenoScript_original_class[0].label.first() + ";"
    else:
        return ";"

for item in sparql:
    # Q of E0 = Val, measured in Unit of Unit_loc.
    # Q(L)=Val, unit: Unit(Unit_loc)
    #print(item)
    #txt="%s of %s = %s, unit: %s%s" % \
    txt = "%s = %s, unit: %s%s" % \
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


query1
len(query1)

query2=list(default_world.sparql("""
           SELECT ?x ?y
           WHERE {
            ?x a owl:NamedIndividual .
            ?y a owl:NamedIndividual .
            ?x obo:BFO_0000051 ?y .
            ?y ?prop ?z .
            ?prop a owl:DatatypeProperty .
            }
"""))

query3=list(default_world.sparql("""
           SELECT ?x ?y
           WHERE {
            ?x a owl:NamedIndividual .
            ?y a owl:NamedIndividual .
            ?x obo:BFO_0000051 ?y .
            ?y ?prop ?z .
            ?prop a owl:ObjectProperty .
            }
"""))

query2
len(query2)
len(query3)


len(set(query2+query3))
query1-(query2+query3)

main_list = [item for item in (query2+query3) if item not in query1]
main_list =[item for item in query1 if item not in (query2+query3)]


main_list = list(set(list_2) - set(list_1))
#---- Remove Cycles


query=list(default_world.sparql("""
           SELECT ?x ?p1 ?p2 ?y
           WHERE {
            ?p1 a owl:ObjectProperty .
            ?p2 a owl:ObjectProperty .
            ?x a owl:NamedIndividual .
            ?y a owl:NamedIndividual .
            ?x ?p1 ?y .
            ?y ?p2 ?x .
            }
"""))


query=list(default_world.sparql("""
           SELECT ?x ?y
           WHERE {
            ?x obo:BFO_0000051 ?y .
            ?y obo:BFO_0000050 ?x .
            }
"""))

query

print("adc")
#---- Relative measurements

#  medial_region > depression >> diameter |<| diameter << depression < lateral_region < scutoscutellar_sulcus:sss_brasiliensis;
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




onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_DELETE.owl', format = "rdfxml")
#---------------
