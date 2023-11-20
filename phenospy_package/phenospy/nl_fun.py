from owlready2 import *
from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()

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

# global phenoscript_annotations
# global phs_implies_absence_of 
# global phs_NL                 
# global phs_original_assertion 
# global phs_original_class     

# -----------------------------------------
# Tmp 1: sparql Absolute and Relative Mesuarements
# -----------------------------------------

# obo.PATO_0000122 # length
# obo.RO_0000053 # has_characterristi
# obo.IAO_0000417 # is qual measured as
# obo.IAO_0000004 # has measurement value
# obo.IAO_0000039 # has measurement unit label
# obo.RO_0000052 # characteristic of
# obo.RO_0000053 # has characteristic, bearer of
# obo.BFO_0000051 has part
def sparql_tmpMeasurements(default_world):
    query=list(default_world.sparql("""
            SELECT ?E0 ?Q ?Val ?x ?Unit ?Unit_loc
            WHERE {?E0 obo:RO_0000053 ?Q .
                ?Q obo:IAO_0000417 ?x .
                ?x obo:IAO_0000004 ?Val .
                ?x obo:AISM_0000404 ?Unit .
                optional {
                    ?Unit obo:RO_0000052 ?Unit_loc .
                    }
                }
    """))
    return query


# Structure: dict_templ={"E0":None, "Q":None, "Val":None, "x":None, "Unit":None, "Unit_loc":None}
# [{'E0': org_Grebennikovius_basilewskyi, 'Q': length:_1e96f5_5-3, 'Val': 2.3,
#  'x': measurement datum:md-8ff5d4, 'Unit': millimeter:_1e96f5_5-7, 'Unit_loc': None}]
def tmpMeasureToDic(query):
    sparql=[]
    for item in query:
        # print(item)
        dict_templ = {"E0": None, "Q": None, "Val": None, "x": None, "Unit": None, "Unit_loc": None}
        dict_templ['E0']= item[0]
        dict_templ['Q'] = item[1]
        dict_templ['Val'] = item[2]
        dict_templ['x'] = item[3]
        dict_templ['Unit'] = item[4]
        if len(item)==6:
            dict_templ['Unit_loc'] = item[5]
        sparql.append(dict_templ)
    return sparql

# node to mardown used for tmp Measure
# def getLabelPhsAnnotation(ind):
def nodeToNL(ind):
    if ind is not None:
        return "[%s](%s)" % (ind.phs_original_class[0].label.first(), ind.phs_original_class[0].iri)

# Unit Locator to nl. used for tmp Measure
# measurement datum:md-8ff5d4, 'Unit': millimeter:_1e96f5_5-7, 'Unit_loc': None
# def render_Unit_loc(ind):
def UnitLocToNL(ind):
    if ind is not None:
        return " of [%s](%s);" % (ind.phs_original_class[0].label.first(), ind.phs_original_class[0].iri)
    else:
        return ";"

# dic_mesuare obtained from sparql query to NL in OWL
def dic_mesuare_ToNLinOWL(dic_mesuare):
    for item in dic_mesuare:
        txt = ", %s = %s, unit: %s%s" % \
        ( nodeToNL(item['Q']),
        item['Val'],
        nodeToNL(item['Unit']),
        UnitLocToNL(item['Unit_loc']) )
        # print(txt)
        item['E0'].phs_NL.append(txt)
        # print("NL:", item['E0'].phs_NL)
        # return(dic_mesuare)
    #
    # DELETE
    # dic_mesuare
    for item in dic_mesuare:
        # destroy_ListEntities([item['Q'], item['Unit']])
        destroy_ListEntities([item['Q']])
        if item['x'] is not None:
            # print(item['x'])
            destroy_entity(item['x'])

# destroy list entitities from sparql query
def destroy_ListEntities(list):
    for entity in list:
        destroy_entity(entity)


# -----------------------------------------
# SPARQL:  Relative Comparison
#   Pattern: Org1 > E1 >> Q1 |comp| Q2 << E2 < Org2
# -----------------------------------------

# Algorithm
# 1. Since sparql here does not quey non-existent props
#   run queries for |>| and |<| separately.
#   First check for the prop existence
# 2. Construct the relative comparison phs_NL only is spp are different.
#   i.e., Org1 != Org2
#   If spp are the same do nothing
# 3. delete inherence_in prop if Q2 inherence in E2: delete inherence_in
#

# comparative_prop = phs_ns.PHS_0000017.iri
def sparql_RelatComp(default_world, comparative_prop):
    # phs_ns.PHS_0000017.iri # has_trait
    # obo.RO_0015007 # increased in magnitude relative to
    # obo.RO_0015008 # deacreased in ...
    # obo.RO_0000053 # bearer of
    has_trait_iri = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000017'
    # !!! ?prop is used on purpose to have acess to the object indownstream scripts
    query = list(default_world.sparql("""
            SELECT DISTINCT ?Q1 ?Org1 ?Q2 ?E2 ?Org2 ?prop
            WHERE {
                ?Q1 a owl:NamedIndividual .
                ?Q2 a owl:NamedIndividual .
                ?Q1  <%s> ?Q2 .
                ?Q1  ?prop ?Q2 .
                ?E2 obo:RO_0000053 ?Q2 .
                ?Org1 <%s> ?Q1 .
                ?Org2 <%s> ?Q2 .
            }
    """ % (comparative_prop, has_trait_iri, has_trait_iri)))
    #print(query)
    return query

# -----------------------------------------
#  q1 |CompProp| q2. This functions removes |CompProp|
# between ind: q1 and q2. Creates a fake ind that is connected to q1
# -----------------------------------------
# CompProp = obo.RO_0015007
# q1 = IRIS['https://urn:uuid:a0f607de-cee2-11ed-a2ca-acde48001122/_1e96f5_13-5']
# q2 = IRIS['https://urn:uuid:a0f607de-cee2-11ed-a2ca-acde48001122/id-185304']
# txt = 'some txt'
def make_fakeInd(q1, q2, CompProp, txt):
    # remove annotation
    phs_original_assertion[q1, CompProp, q2] = []
    # remove CompProp link q1.CompProp
    CompProp[q1] = []
    # make fake individual
    CL = q1.is_a.first()
    fake_ind = CL('https://temp/tmp/')
    fake_ind.iri = 'https://temp/tmp/' + q1.label.first() + '/fake_ind'
    fake_ind.phs_original_class.append(CL)
    fake_ind.phs_NL.append(txt)
    # make a link between q1 and fake_ind
    CompProp[q1] = [fake_ind]
    phs_original_assertion[q1, CompProp, fake_ind] = True


def tmpRelatToDic(query):
    # [{'Q1': length:_1e96f5_13-5, 'Org1': org_Grebennikovius_basilewskyi, 
    #   'Q2': length:id-185304, 'E2': leg:_1e96f5_18-3, 'Org2': org_Grebennikovius}]
    dic_RelatComp=[]
    for item in query:
        # print(item)
        dict_templ = {"Q1": None, "Org1": None, "Q2": None, "E2": None, "Org2": None, "CompProp": None}
        dict_templ['Q1']= item[0]
        dict_templ['Org1'] = item[1]
        dict_templ['Q2'] = item[2]
        dict_templ['E2'] = item[3]
        dict_templ['Org2'] = item[4]
        dict_templ['CompProp'] = item[5]
        dic_RelatComp.append(dict_templ)
    return dic_RelatComp

def dic_Relat_ToNLinOWL(dic_RelatComp):
    # We need to:
    # 1. delete inherence_in prop if Q2 inherence in E2 delete inherence_in
    # 2. construct the relative comparison phs_NL only is spp are different
    # --
    # txt: Q2 of E2 in Org2
    # item = dic_RelatComp[0]
    # renderNL(item['CompProp'], onto)
    for item in dic_RelatComp:
        if (item['Org1'].iri != item['Org2'].iri):
            # txt = " %s of %s in _%s_" % \
            # ( nodeToNL(item['Q2']), nodeToNL(item['E2']), item['Org2'].label.first() )
            txt = " of %s in _%s_;" % \
            (nodeToNL(item['E2']), item['Org2'].label.first())
            # print(txt)
            # substitute Q1 with fake ind that is not connected to Q2
            make_fakeInd(q1=item['Q1'], q2=item['Q2'], 
            CompProp =item['CompProp'], txt=txt)


# -----------------------------------------
# Pattern: chracter: present
# -----------------------------------------
def add_presentTag_ToNLinOWL(default_world):
    global phenoscript_annotations, phs_implies_absence_of, phs_NL 
    global phs_original_assertion, phs_original_class
    # get all pairs: x has part y
    # obo.BFO_0000051 has part
    query_x_hp_y = list(default_world.sparql("""
            SELECT DISTINCT ?y
            WHERE {
                ?x a owl:NamedIndividual .
                ?y a owl:NamedIndividual .
                ?x obo:BFO_0000051 ?y .
                }
    """))
    # Old code
    # presesent_tag=set()
    # for trip in query_x_hp_y:
    #     n1=trip[0] # x
    #     n2=trip[1] # y
    #     has_out_edge=False
    #     # n2.get_properties()
    #     for prop in n2.get_properties():
    #         if not issubclass(prop, phs_linksTraits):
    #             for n3 in prop[n2]:
    #                 asrt = phs_original_assertion[n2, prop, n3]
    #                 print(n2, prop, n3, asrt)
    #                 if len(asrt)>0 or issubclass(prop, phs_NL):
    #                     #if issubclass(prop, owl.ObjectProperty) or issubclass(prop, owl.DatatypeProperty):
    #                     #print(n2, prop, "is", asrt)
    #                     has_out_edge = True
    #     if has_out_edge == False:
    #         print(n2, prop, "is", asrt)
    #         presesent_tag.add(n2)

    # every node that should be marks with 'present' does not have any single node that is phs_original_assertion or phs_NL
    # so if node has those assertions it is not our customer. we look for those that have no.
    # ---
    # 1. from sparql, get all pairs: x has part y
    # 2. for each y get triples: y prop z
    # 3. check if for all props:  y prop z is not phs_original_assertion and phs_NL
    # 4. Select y if all Flase are returned at step 3

    presesent_tag=set()
    for item in query_x_hp_y:
        y = item[0]
        has_out_edges = []
        # get all props from y
        for prop in y.get_properties():
            # get triple: y prop z
            for z in prop[y]:
                is_original_assert = bool(phs_original_assertion[y, prop, z])
                # print(y, prop, z, is_original_assert)
                if (is_original_assert == False) and not issubclass(prop, phs_NL):
                    has_out_edges.append(False)
                else:
                    has_out_edges.append(True)
        # if all props return false for a given y then it's what we need
        if all(not item for item in has_out_edges):
            # print(y)
            presesent_tag.add(y)
    #
    # add 'present' tag to NL in OWL
    for ind in presesent_tag:
        txt = ": present;"
        # print(ind, txt)
        ind.phs_NL.append(txt)



# -----------------------------------------
# Make NL Graph for Md rendering
# -----------------------------------------
def makeNLGraph_basic(onto):
    global phenoscript_annotations, phs_implies_absence_of, phs_NL 
    global phs_original_assertion, phs_original_class
    # -----------------------------------------
    # Namespaces
    # -----------------------------------------
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')

    # -----------------------------------------
    # Add absence
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding absence traits...{Style.RESET_ALL}")

    # for ind in onto.individuals():
    #     #print(ind)
    #     if (len(ind.phs_implies_absence_of)>0):
    #         # print(ind, "---", ind.phs_implies_absence_of)
    #         abs_class=ind.phs_implies_absence_of[0]
    #         txt=" [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
    #         # print(txt)
    #         ind.phs_NL.append(txt)
    
    for ind in onto.individuals():
        #print(ind)
        if (len(ind.phs_implies_absence_of)>0):
            #print(len(ind.phs_implies_absence_of))
            #print(ind, "---", ind.phs_implies_absence_of)
            for index in range(0, len(ind.phs_implies_absence_of)):
                abs_class=ind.phs_implies_absence_of[index]
                #print('\t', abs_class)
                txt=", [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
                ind.phs_NL.append(txt)

    # -----------------------------------------
    # Pattern: add chracter prsence
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding presence traits...{Style.RESET_ALL}")
    add_presentTag_ToNLinOWL(default_world)

    # -----------------------------------------
    # SPARQL:  Absolute and Relative Mesuarements
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding Absolute and Relative Mesuarements...{Style.RESET_ALL}")
    
    # check is meserument entities are present, othervise sparql does not work
    is_mesure_present = IRIS['http://purl.obolibrary.org/obo/IAO_0000417']
    if bool(is_mesure_present):
        query_tmpMesuare = sparql_tmpMeasurements(default_world)
        dic_mesuare = tmpMeasureToDic(query_tmpMesuare)
        # dic_mesuare obtained from sparql query to NL in OWL
        dic_mesuare_ToNLinOWL(dic_mesuare)

    # -----------------------------------------
    # SPARQL:  Relative Comparison
    #   Pattern: Org1 > E1 >> Q1 |comp| Q2 << E2 < Org2
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding Relative Comparison traits...{Style.RESET_ALL}")

    # Check existence and if existence render it to NL
    # increased in magnitude relative to
    compProp = obo.RO_0015007
    if bool(compProp):
        query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015007.iri)
        dic_RelatComp = tmpRelatToDic(query_RelatComp)
        dic_Relat_ToNLinOWL(dic_RelatComp)
    #
    # decreased in magnitude relative to
    compProp = obo.RO_0015008
    if bool(compProp):
        query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015008.iri)
        dic_RelatComp = tmpRelatToDic(query_RelatComp)
        dic_Relat_ToNLinOWL(dic_RelatComp)
    #
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")


# -----------------------------------------
# Traverse graph
# -----------------------------------------

global visited_triples
visited_triples = list()

# def traverseOntoMark_Overleaf
def traverseGraphForNL(onto, ind0, tabs="\t", tab_char="\t", visited_nodes=set()):
    global visited_triples
    global phenoscript_annotations, phs_implies_absence_of, phs_NL 
    global phs_original_assertion, phs_original_class
    #print(visited_triples)
    txt=""
    visited_nodes.add(ind0)
    triples=[]
    # prop = list(ind0.get_properties())[7]
    for prop in ind0.get_properties():
        if not issubclass(prop, owl.AnnotationProperty):
            # print('HERE', prop)
            for value in prop[ind0]:
                asrt = phs_original_assertion[ind0, prop, value]
                triple = [ind0, prop, value]
                if len(asrt) > 0 and (triple not in visited_triples): # should be also True for asrt
                    #triple = [ind0, prop, value]
                    #print(asrt)
                    triples.append(triple)
                    visited_triples.append(triple)
        #elif issubclass(prop, inf.PhenoScript_NL) or issubclass(prop, inf.PhenoScript_implies_absence_of):
        elif issubclass(prop, phs_NL):
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
        txt = txt + ("%s%s" % (renderNL(prop, onto), renderNL(value, onto)))
        if issubclass(prop, owl.ObjectProperty) and (value not in visited_nodes):
            #print(traverseOnto(value))
            #visited_nodes.add(value)
            txt = txt + traverseGraphForNL(onto, value, tabs=tabs, tab_char = tab_char, visited_nodes=visited_nodes)
        return  txt
    if len(triples) > 1:
        # trip = triples[0]
        for trip in triples:
            # trip= triples[0]
            prop = trip[1]
            value = trip[2]
            #txt = txt +"\n" + tabs + ("%s <%s> %s" % (ind0, prop, value))
            txt = txt + "\n" + tabs + ("%s%s%s" % (renderNL(ind0, onto), renderNL(prop, onto), renderNL(value, onto)))
            if issubclass(prop, owl.ObjectProperty) and (value not in visited_nodes):
                # txt = txt + traverseOntoMark_Overleaf(value, tabs=tabs+"\t", visited_nodes=visited_nodes)
                txt = txt + traverseGraphForNL(onto, value, tabs=tabs+tab_char, tab_char = tab_char, visited_nodes=visited_nodes)
        return txt
    if len(triples) == 0:
        # print('TRIPR len=0')
        return ";"



def check_string_pattern_complete(s):
    if (s.startswith(',') or s.startswith(':')):
        return True
    return False

# -----------------------------------------
# Render NL when traversing graph
# -----------------------------------------
# obo.RO_0015007 increased_in_magnitude_relative_to http://purl.obolibrary.org/obo/RO_0015007
# obo.RO_0015008 decreased in magnitude relative to http://purl.obolibrary.org/obo/RO_0015008
def renderNL(x, onto):
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    # if x is individual
    if isinstance(x, owl.Thing):
        return " [%s](%s)" % (x.phs_original_class[0], x.phs_original_class[0].iri)
    elif issubclass(x, owl.ObjectProperty) or issubclass(x, owl.DatatypeProperty):
        #
        dict={obo.BFO_0000051 :',', obo.BFO_0000050 : ' of', obo.RO_0000053 : ':', obo.RO_0000052 : ' of', 
        obo.RO_0015007 : ' [larger than](http://purl.obolibrary.org/obo/RO_0015007)',  
        obo.RO_0015008 : ' [smaller than](http://purl.obolibrary.org/obo/RO_0015008)'}
        #
        if x in dict:
            return dict[x]
        else:
            return " [%s](%s)" % (x.label.first(), x.iri)
    elif issubclass(x, owl.AnnotationProperty):
        return ""
    elif isinstance(x, (int, float)):
        return " %s;" % str(x)
    elif isinstance(x, str):
        #return x
        #return "%s" % x
        if check_string_pattern_complete(x):
           return "%s" % x
        else:
            return  " %s" % x


# -----------------------------------------
# Make NL desciptions in Md format
# -----------------------------------------
# ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')[0]
# def makeMarkdown(onto, ind0, file_save=None, verbose=False):
#     print(f"{Fore.BLUE}Rendering NL description as markdown...{Style.RESET_ALL}")
#     global visited_nodes, visited_triples
#     visited_nodes=set()
#     visited_triples=list()
#     md = traverseGraphForNL(onto, ind0, tabs='\t', tab_char='\t', visited_nodes=set())
#     # print(md)
#     md_out = md.replace("\t [", " [")
#     md_out = md_out.replace("\t [", "\t- [")
#     md_out = md_out.replace("\n [", "\n- [")
#     # Add species name as comment
#     header = '<!-- ' + ind0.label.first() + ' -->'
#     md_out = header + md_out
#     #print(md_out)
#     #
#     visited_nodes=set()
#     visited_triples=list()
#     #
#     if file_save is not None:
#         print(f"{Fore.BLUE}Saving markdown to:{Style.RESET_ALL}", file_save)
#         fl = open(file_save, "w+")
#         fl.writelines(md_out)
#         fl.close()
#     print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
#     if verbose==True:
#         return md_out