# cd /Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy
# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/python

#
#------------

from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

import os
import tempfile
import xml.etree.ElementTree as ET
# from datetime import date
import datetime

from phenospy.owl_xml2owl_fun import *
from phenospy.xml_recodeThis import *
from phenospy.phs_various_fun import *
#from xml_recodeThis import *

# -----------------------------------------
# Config: imported from owl_xml2owl_fun
# -----------------------------------------
# from owl_owlready_config import *

# -----------------------------------------
# Arguments
# -----------------------------------------

# phsXML = "/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs_xml.xml"
# owl_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/test.owl'
# tree = ET.parse(phsXML)
# set_log_level(0)
# xmlToOwl(tree, owl_file)

def xmlToOwl(tree, owl_file):
    print(f"{Fore.BLUE}Converting XML to OWL...{Style.RESET_ALL}")
    # -----------------------------------------
    # Read XML
    # -----------------------------------------
    # tree = ET.parse(phsXML)
    root = tree.getroot()

    # -----------------------------------------
    # Convert 'this' keyword
    # -----------------------------------------
    xmlRecodeThis(root, ns)

    # -----------------------------------------
    # Create ontology
    # -----------------------------------------
    # base_iri = root.find(".//base-iri", ns)
    base_iri = root.find("./phs-config-yaml/base-iri", ns)

    # onto.base_iri = base_iri.text
    base_iri_text = base_iri.text 
    onto = get_ontology(base_iri_text)

    # -----------------------------------------
    # Create classes
    # -----------------------------------------

    make_all_classes(root, onto)

    # -----------------------------------------
    # Save tmp file and then open
    # -----------------------------------------
    # Save the ontology to a temporary file
    # with tempfile.NamedTemporaryFile() as f:
    #     onto.save(file=f.name, format="rdfxml")
    #     # print("Ontology saved to:", f.name)
    #     onto.destroy()
    #     onto = get_ontology(f.name).load()
    # #
    temp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
    onto.save(file=temp.name, format="rdfxml")
    temp.close()
    onto.destroy()
    onto = get_ontology(temp.name).load()
    os.unlink(temp.name)
    #
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')

    # --------------------------------------------------------------------------------
    # Add phenoscript ontology and other terms
    # --------------------------------------------------------------------------------
    module_path = os.path.dirname(__file__)
    owl_file_path = os.path.join(module_path, "owl_make_phsOntology.py")

    with open(owl_file_path, "r") as f_phs:
        phs_make = f_phs.read()
    
    exec(phs_make, {"onto": onto}, globals())

    # -----------------------------------------
    # Add ontology metadata
    # -----------------------------------------
  
    this_Project = cls_project() # assign project to class "project"
    this_Project.iri = base_iri_text + '/project'
    this_Project.project_id.append(base_iri_text)
    # project title
    xml_project_title = root.find("./phs-config-yaml/project-title", ns)
    this_Project.title.append(xml_project_title.text)
    this_Project.label.append('project: ' + xml_project_title.text[:35] + '...') # truncate ptoject title for label
    this_Project.created_by = "phenospy-" + phsVersion
    this_Project.creation_date = datetime.datetime.now()

    yaml_authors = root.find("./phs-config-yaml/authors", ns)
    for author in yaml_authors:
        # auct_name = author.get('name') + ' ' + author.text
        auct_name = anyURI(author.text)
        onto.metadata.contributor.append(auct_name)
        this_Project.contributor.append(auct_name)
        label[this_Project, contributor, auct_name] = author.get('name')

    yaml_ontos = root.find("./phs-config-yaml/importOntologies", ns)
    for i in yaml_ontos:
        onto.metadata.purl_requires.append(anyURI(i.text))
        this_Project.purl_requires.append(anyURI(i.text))



    #-----------------------
    # Make nodes
    #-----------------------

    # get unique nodes
    print(f"{Fore.BLUE}Creating nodes...{Style.RESET_ALL}")


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
        
        className=IRIS[nodeClass].label
        newNode.label = className[0]+':'+ ni.rsplit('/', 1)[-1]

        # add annotations
        newNode.created_by = "phenospy-" + phsVersion
        # add date
        # today = date.today()
        # dt_string = today.strftime("%d/%m/%Y")
        # newNode.creation_date = dt_string
        newNode.creation_date = datetime.datetime.now()
        #
        # add original class annotation
        newNode.phs_original_class.append(nodeClassObj)
        newNode.purl_source.append(this_Project)
        #
        # add additional/extra class
        extra_classes = node.findall(".//phs:node_property[@phs:value-type_onto='C']", ns)
        if len(extra_classes) > 0:
            # print('Extra CLASS')
            for cl in extra_classes:
                # print(cl.get(phs + 'value-iri'))
                extraClass = IRIS[cl.get(phs + 'value-iri')]
                newNode.is_a.append(extraClass)
                newNode.phs_original_class.append(extraClass)




    #-----------------------
    # Make edges between nodes
    ##  ............................................................................
    ##  Compile N E N: phs:node pos=1 -> E pos=2 -> (phs:node | phs:nested_node | phs:list_node)  pos=3    ####
    #-----------------------

    print(f"{Fore.BLUE}Adding edges between nodes...{Style.RESET_ALL}")

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
                    phs_original_assertion[N1, Ed, N2] = True
                    # purl_source[N1, Ed, N2] = append(this_Project)
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
                    # purl_source[N1, Ed, N2] = this_Project
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
                        phs_original_assertion[N1, Ed, N2] = True
                    else:
                        exec('N1.%s.append(N2)' % Ed.name)
                        phs_original_assertion[N1, Ed, N2] = True
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
                        phs_original_assertion[N1, Ed, N2] = True
                    else:
                        exec('N1.%s.append(N2)' % Ed.name)
                        phs_original_assertion[N1, Ed, N2] = True
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
                    phs_original_assertion[N1, Ed, N2] = True
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
            
            elif (Pos3XML[0].tag == phs + 'quoted_node'):
                # print(Pos3XML[0].attrib)
                N1 = IRIS[nodeXML.get(phs + 'node_id')]
                Ed = IRIS[edgeXML[0].get(phs + 'iri')]
                N2 = Pos3XML[0].get(phs + 'node_name')
                if 'http://www.w3.org/2000/01/rdf-schema#label' in Ed.iri:
                    exec('N1.%s = N2' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
                elif (is_valid_uri(N2)):
                    # ins2.new_dp.append(anyURI('https://www.gbif.org/species/10360397'))
                    exec('N1.%s.append(anyURI(N2))' % Ed.name)
                    phs_original_assertion[N1, Ed, anyURI(N2)] = True
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
                #
            else:
                #print('WARNING: something is wrong in "for nodeXML in nodePos1: ... else:"')
                # warnings.warn('something is wrong  with Pos3XML[0].tag in "for nodeXML in nodePos1: ... else:"')
                print(f"{Fore.RED}something is wrong  with Pos3XML[0].tag in for nodeXML in nodePos1: ... else:!{Style.RESET_ALL}")

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
                N1.phs_implies_absence_of.append(classN2)

                # N2.is_a.append(obo.HAO_0001017) # this works
                # N2.is_a.append(obo.BFO_0000051.some(obo.HAO_0001017)) # this works
                # N2.is_a.append(obo.BFO_0000051.some( Not(obo.BFO_0000051.some(obo.HAO_0001017)) ))  # this works
            else:
                # warnings.warn('Something is wrong with Pos3XML[0].tag in "for nodeXML in nodePos1: ... elif (is_negEdge == True): ...."')
                print(f"{Fore.RED}Something is wrong with 'Pos3XML[0].tag in for nodeXML in nodePos1: ... elif (is_negEdge == True):'!{Style.RESET_ALL}")




    ##  ............................................................................
    ##  Compile N E N: (phs:nested_node | phs:list_node) pos=1 -> E pos=2 -> (phs:node) pos=3    ####

    print(f"{Fore.BLUE}Adding edges between nested and list nodes...{Style.RESET_ALL}")


    # select list or nested nodes, triple_pos=1
    nodePos1=root.findall(".//phs:nested_node[@phs:triple_pos='1']", ns) + root.findall(".//phs:list_node[@phs:triple_pos='1']", ns)

    # nodeXML = nodePos1[0]
    for nodeXML in nodePos1:
        parentXML=parent_map[nodeXML]
        edgeXML=parentXML.findall("./*[@phs:triple_pos='2']", ns)
        Pos3XML=parentXML.findall("./phs:node[@phs:triple_pos='3']", ns)
        is_negEdge = eval(edgeXML[0].get(phs + 'negative_prop'))
        #
        if (Pos3XML[0].tag == phs + 'node' and is_negEdge==False):
            N1_childrenXML = nodeXML.findall(".//phs:node", ns)
            N1_unique_childrenXML = xmlUniqueNodes(N1_childrenXML, attr=phs + 'node_id')
            Ed = IRIS[edgeXML[0].get(phs + 'iri')]
            N2=IRIS[Pos3XML[0].get(phs + 'node_id')]
            # child=N1_unique_childrenXML[0]
            for child in N1_unique_childrenXML:
                N1 = IRIS[child.get(phs + 'node_id')]
                if owl.FunctionalProperty in Ed.is_a:
                    exec('N1.%s = N2' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
                else:
                    exec('N1.%s.append(N2)' % Ed.name)
                    phs_original_assertion[N1, Ed, N2] = True
        else:
            # warnings.warn('something is wrong  with "Pos3XML[0].tag == phs + node and is_negEdge==False" when phs:triple_pos=1 is not a simple node')
            print(f"{Fore.RED}something is wrong  with 'Pos3XML[0].tag == phs + node and is_negEdge==False' when phs:triple_pos=1 is not a simple node!{Style.RESET_ALL}")



    ##  ............................................................................
    ##  Linking OTU and OPHUs: linksTraits    ####

    print(f"{Fore.BLUE}Linking OTU's DATA with TRAITS...{Style.RESET_ALL}")

    OTUs=root.findall(".//phs:otu_object", ns)
    # loop over otu_objects (i.e. species). in each otu_obj identify nodes that link all ophus
    # otu = OTUs[0]
    for otu in OTUs:
        # get all phs:node_property
        props=otu.findall(".//phs:otu_properties//phs:node_property", ns)
        # get all nodes in phs:ophu_list for the otu that are fromNegativeEdge='False'
        ophuList = otu.findall(".//phs:ophu_list", ns)
        ophuNodes_noFil = ophuList[0].findall(".//phs:node[@phs:fromNegativeEdge='False']", ns)
        
        # exclude those that have keyword 'exclude = True'
        ophuNodes = []
        for node in ophuNodes_noFil:
            node_exc = node.find(".//phs:node_property[@phs:var-iri='KeyWord:exclude'][@phs:value-iri='KeyWord:True']", ns)
            if node_exc is None:
                ophuNodes.append(node)
            # else :
            #     print(node_exc.get(phs+'var-iri'))  
        for p in props:
            if (p.text=='linksTraits') and (p.get(phs+'value-iri') == "KeyWord:True"):
                parentXML = parent_map[p]
                N1 = IRIS[parentXML.get(phs+'node_id')]
                # Ed=IRIS[p.get(phs+'iri')]
                Ed = has_trait
                #print(p.text, p.get(phs+'value'), p.get(phs+'iri'), parentXML.get(phs+'node_id'))
                #print(N1, Ed)
                for node in ophuNodes:
                    N2=IRIS[node.get(phs+'node_id')]
                    # if owl.FunctionalProperty in Ed.is_a:
                    #     exec('N1.%s = N2' % Ed)
                    #     phs_original_assertion[N1, Ed, N2] = True
                    # else:
                    exec('N1.%s.append(N2)' % Ed)
                    phs_original_assertion[N1, Ed, N2] = True
    
    ##  ............................................................................
    ##  Linking TRAITS and DATA Block with OTU Block and nodes    ####
    print(f"{Fore.BLUE}Linking OTU's Blocks...{Style.RESET_ALL}")
    #OTUs=root.findall(".//phs:otu_object", ns)
    # loop over otu_objects
    # otu = OTUs[0]
    for otu in OTUs:
        ClassOTU    =IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000022']
        ClassDATA   =IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000020']
        ClassTRAITS =IRIS['https://github.com/sergeitarasov/PhenoScript/PHS_0000021']
        
        #otu_block = ClassOTU(base_iri_text + '/_' + uuid_n(6))
        otu_block           = ClassOTU('https://temp/tmp')
        #otu_block.iri       = 'https://github.com/2323222344dsd'
        otu_block.iri       = base_iri_text + '/_' + uuid_n(6)
        data_block          = ClassDATA('https://temp/tmp')
        #data_block.iri      = 'https://github.com/2323222344dsdsdsdc'
        data_block.iri      = base_iri_text + '/_' + uuid_n(6)
        traits_block        = ClassTRAITS('https://temp/tmp')
        traits_block.iri    = base_iri_text + '/_' + uuid_n(6)
        #
        otu_block.label     = ClassOTU.label.first() +':'+ otu_block.iri.rsplit('/', 1)[-1]
        data_block.label    = ClassDATA.label.first() +':'+ data_block.iri.rsplit('/', 1)[-1]
        traits_block.label  = ClassTRAITS.label.first() +':'+ traits_block.iri.rsplit('/', 1)[-1]
        #
        otu_block.purl_source.append(this_Project)
        data_block.purl_source.append(this_Project)
        traits_block.purl_source.append(this_Project)
        #
        data_block.purl_source.append(otu_block)
        traits_block.purl_source.append(otu_block)
        #
        #add annotations
        # otu_block.created_by = "phenospy-" + phsVersion
        # otu_block.creation_date = datetime.datetime.now()
        #
        # get ophuList nodes and link them with DATA block
        ophuList = otu.findall(".//phs:ophu_list", ns)
        ophuNodes_noFil = ophuList[0].findall(".//phs:node[@phs:fromNegativeEdge='False']", ns)
        for node in ophuNodes_noFil:
            N1 = IRIS[node.get(phs+'node_id')]
            N1.purl_source.append(traits_block)
        #
        # get otu_properties nodes and link them with DATA block
        otu_props = otu.findall(".//phs:otu_properties", ns)
        otuNodes_noFil = otu_props[0].findall(".//phs:node[@phs:fromNegativeEdge='False']", ns)
        for node in otuNodes_noFil:
            N1 = IRIS[node.get(phs+'node_id')]
            N1.purl_source.append(data_block)
            #phs_original_assertion[N1, purl_source, data_block] = True


    #-----------------------
    # Save file
    #-----------------------
    print(f"{Fore.BLUE}Saving owl file: {Style.RESET_ALL}", owl_file)
    onto.save(file = owl_file, format = "rdfxml")
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
