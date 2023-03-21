# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

#
#------------

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()

# import types
import warnings
import xml.etree.ElementTree as ET
from datetime import date
# from owl_owlready_config import *
from owl_xml2owl_fun import *



# -----------------------------------------
# Arguments
# -----------------------------------------


phsXML = "/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs_xml.xml"
# onto_phs = get_ontology('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phenoscript.owl').load()

# -----------------------------------------
# Read XML
# -----------------------------------------
tree = ET.parse(phsXML)
root = tree.getroot()

# -----------------------------------------
# Create ontology
# -----------------------------------------
# base_iri = root.find(".//base-iri", ns)
base_iri = root.find("./phs-config-yaml/base-iri", ns)
# print(base_iri.text)

# onto = get_ontology(base_iri.text)
onto = get_ontology('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phenoscript.owl').load()
# onto = get_ontology('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/test.owl').load()
# onto.base_iri = base_iri.text

obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
# phso = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript')
# inf = onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")


# -----------------------------------------
# Add ontology metadata
# -----------------------------------------
onto.metadata.comment.append('aucr 1')


# -----------------------------------------
# Create classes
# -----------------------------------------

make_all_classes(root, onto)

onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/test.owl', format = "rdfxml")
onto.destroy()

onto = get_ontology('/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/test.owl').load()
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
#-----------------------
# Make nodes
#-----------------------

# get unique nodes
print('Creating nodes...\n')

nodeID=[]
# get unique nodes except those that have phs:fromNegativeEdge='True'
for node in root.iter(phs+'node'):
    # root.findall(".//phs:node", ns)
    # root.findall(".//phs:node[@phs:fromNegativeEdge='False']", ns)
    is_negEdge = eval(node.get(phs + 'fromNegativeEdge'))
    if is_negEdge==False:
        nodeID.append(node.get(phs + 'node_id'))


# get unique
nodeIDunique=list(set(nodeID))

# create new nodes
# ni = nodeIDunique[1]
#destroy_entity(newNode)
#onto.destroy()
for ni in nodeIDunique:
    node = root.find(".//phs:node[@phs:node_id='%s']" % ni, ns)
    #print(node)
    nodeClass = node.get(phs + 'iri')
    # this piece of code uses a workaround for iri cuz Owlready does not assign it correctly
    # when using the direct approach newNode = IRIS[nodeClass](ni)
    # create new node
    # newNode = IRIS[nodeClass]('https://temp/tmp')
    nodeClassObj=IRIS[nodeClass]
    newNode = nodeClassObj('https://temp/tmp')
    newNode.iri=ni
    #print(newNode.iri)

    # getting labels
    # label = node.find(".//phs:node_property[.='rdfs:label']", ns)
    # if (label is not None):
    #     #print(label.text, label.get(phs + 'value'))
    #     newNode.label = label.get(phs + 'value')
    # elif (label is None):
    #     className=IRIS[nodeClass].label
    #     newNode.label = className[0]+':'+ ni.rsplit('/', 1)[-1]
    
    className=IRIS[nodeClass].label
    newNode.label = className[0]+':'+ ni.rsplit('/', 1)[-1]

    # getting catalog number
    # catalogNumber_value = node.find(".//phs:node_property[.='catalogNumber']", ns)
    # if (catalogNumber_value is not None):
    #     newNode.catalogNumber = catalogNumber_value.get(phs + 'value')

    # add annotations
    newNode.created_by = "phenospy v. " + phsVersion
    # add date
    today = date.today()
    dt_string = today.strftime("%d/%m/%Y")
    newNode.creation_date = dt_string
    # add original class annotation
    # newNode.PhenoScript_original_class.append(nodeClassObj)
    newNode.PHS_0000002.append(nodeClassObj)




#-----------------------
# Make edges between nodes
##  ............................................................................
##  Compile N E N: phs:node pos=1 -> E pos=2 -> (phs:node | phs:nested_node | phs:list_node)  pos=3    ####
#-----------------------

print('Adding edges between nodes...\n')

# make mapping to extract parents quickly
parent_map = {c:p for p in root.iter() for c in p}
#parent_map[nodePos1[0]]

# select node triple_pos=1
nodePos1=root.findall(".//phs:node[@phs:triple_pos='1']", ns)
#len(nodePos1)

#----------------------
# nodeXML = nodePos1[2]
for nodeXML in nodePos1:
    parentXML=parent_map[nodeXML]
    edgeXML=parentXML.findall("./*[@phs:triple_pos='2']", ns)
    Pos3XML=parentXML.findall("./*[@phs:triple_pos='3']", ns)
    is_negEdge = eval(edgeXML[0].get(phs + 'negative_prop'))
    #
    if (is_negEdge==False):
        #
        #continue
        #print(is_negEdge)
        #
        if (Pos3XML[0].tag == phs + 'node'):
            # print('ok')
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            N2 = IRIS[Pos3XML[0].get(phs + 'node_id')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            if owl.FunctionalProperty in Ed.is_a:
                exec('N1.%s = N2' % Ed.name)
                # inf.PhenoScript_original_assertion[N1, Ed, N2] = True
                onto.PHS_0000005[N1, Ed, N2] = True
            else:
                exec('N1.%s.append(N2)' % Ed.name)
                onto.PHS_0000005[N1, Ed, N2] = True
            #
        elif (Pos3XML[0].tag == phs + 'list_node'):
            # print('list_node')
            #
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            childrenXML = Pos3XML[0].findall(".//phs:node[@phs:triple_pos='NO']", ns)

            for child in childrenXML:
                N2 = IRIS[child.get(phs + 'node_id')]
                if owl.FunctionalProperty in Ed.is_a:
                    exec('N1.%s = N2' % Ed.name)
                    onto.PHS_0000005[N1, Ed, N2] = True
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    onto.PHS_0000005[N1, Ed, N2] = True
            #
        elif (Pos3XML[0].tag == phs + 'nested_node'):
            # print('nested_node')
            #
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            childrenXML = Pos3XML[0].findall(".//phs:node", ns)
            #
            # get unique nodes based on their ids
            unique_childrenXML = xmlUniqueNodes(childrenXML, attr=phs + 'node_id')
            for child in unique_childrenXML:
                # print('child: ', child.attrib)
                N2 = IRIS[child.get(phs + 'node_id')]
                if owl.FunctionalProperty in Ed.is_a:
                    exec('N1.%s = N2' % Ed.name)
                    onto.PHS_0000005[N1, Ed, N2] = True
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    onto.PHS_0000005[N1, Ed, N2] = True
            #
        elif (Pos3XML[0].tag == phs + 'numeric_node'):
            # print(Pos3XML[0].attrib)
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            N2_type = Pos3XML[0].get(phs + 'numeric_type')
            N2_value = Pos3XML[0].get(phs + 'node_name')
            N2 = phsNumbersToOWL(N2_value, N2_type)
            # [owl.DatatypeProperty, owl.FunctionalProperty] obo.IAO_0000004.is_a
            if owl.FunctionalProperty in Ed.is_a:
                exec('N1.%s = N2' % Ed.name)
                onto.PHS_0000005[N1, Ed, N2] = True
            else:
                exec('N1.%s.append(N2)' % Ed.name)
                onto.PHS_0000005[N1, Ed, N2] = True
        
        elif (Pos3XML[0].tag == phs + 'quoted_node'):
            # print(Pos3XML[0].attrib)
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            N2 = Pos3XML[0].get(phs + 'node_name')
            if 'http://www.w3.org/2000/01/rdf-schema#label' in Ed.iri:
                exec('N1.%s = N2' % Ed.name)
                # onto.PHS_0000005[N1, Ed, N2] = True
            else:
                exec('N1.%s.append(N2)' % Ed.name)
                # onto.PHS_0000005[N1, Ed, N2] = True
            #
        else:
            #print('WARNING: something is wrong in "for nodeXML in nodePos1: ... else:"')
            warnings.warn('something is wrong  with Pos3XML[0].tag in "for nodeXML in nodePos1: ... else:"')
            #
    elif (is_negEdge == True):
        if (Pos3XML[0].tag == phs + 'node'):
            # print(is_negEdge)
            #
            N1 = IRIS[nodeXML.get(phs + 'node_id')]
            # N2 = IRIS[Pos3XML[0].get(phs + 'node_id')]
            classN2 = IRIS[Pos3XML[0].get(phs + 'iri')]
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            #
            # --------------------------------
            # obo.BFO_0000051  # has_part
            # --------------------------------
            # exec('N1.is_a.append( obo.BFO_0000051.some( Not(%s.some(classN2) ) ) )' % Ed)
            # exec('N1.is_a.append(Not(%s.some(classN2)))' % Ed)
            N1.is_a.append(Not(Ed.some(classN2)))
            # add annotation for absence
            # N1.PhenoScript_implies_absence_of.append(classN2)
            N1.PHS_0000003.append(classN2)

            # N2.is_a.append(obo.HAO_0001017) # this works
            # N2.is_a.append(obo.BFO_0000051.some(obo.HAO_0001017)) # this works
            # N2.is_a.append(obo.BFO_0000051.some( Not(obo.BFO_0000051.some(obo.HAO_0001017)) ))  # this works
        else:
            warnings.warn('Something is wrong with Pos3XML[0].tag in "for nodeXML in nodePos1: ... elif (is_negEdge == True): ...."')




#-----
onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/test.owl', format = "rdfxml")


