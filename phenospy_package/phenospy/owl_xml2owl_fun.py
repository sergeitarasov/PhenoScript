# -----------------------------------------
# Settings for using owlready and Phenoscript
# -----------------------------------------
from phenospy.owl_owlready_config import *
from owlready2 import *
from urllib.parse import urlparse
# -----------------------------------------
# Functions
# -----------------------------------------


# make_Class(onto, iri, label)
def make_Class(onto, iri, label):
     # check existence
    chk = IRIS[iri]
    if chk is None:
        with onto:
            class new_term(Thing): pass
        new_term.iri = iri
        new_term.label = label
        if (new_term.iri != iri):
            print(f"{Fore.RED}Error: cannot set new class iri.{Style.RESET_ALL}")
            exit()

def make_ObjectProperty(onto, iri, label):
     # check existence
    chk = IRIS[iri]
    if chk is None:
        with onto:
            class new_term(ObjectProperty): pass
        new_term.iri = iri
        new_term.label = label
        if (new_term.iri != iri):
            print(f"{Fore.RED}Error: cannot set new class iri.{Style.RESET_ALL}")
            exit()

def make_DataProperty(onto, iri, label):
    # check existence
    chk = IRIS[iri]
    if chk is None:
        with onto:
            class new_dp(DataProperty): pass
        new_dp.iri = iri
        new_dp.label = label
        if (new_dp.iri != iri):
            print(f"{Fore.RED}Error: cannot set new class iri.{Style.RESET_ALL}")
            exit()

def make_AnnotationProperty(onto, iri, label):
    # check existence
    chk = IRIS[iri]
    if chk is None:
        with onto:
            class new_ap(AnnotationProperty): pass
        new_ap.iri = iri
        new_ap.label = label
        if (new_ap.iri != iri):
            print(f"{Fore.RED}Error: cannot set new class iri.{Style.RESET_ALL}")
            exit()


# - get classes
def make_all_classes(root, onto):
    terms_C = root.findall(".//phs:node[@phs:type_onto='C']", ns)
    dic_C = {}
    for i in terms_C:
        #print(i.get(phs + 'iri'), i.get(phs + 'label_original'))
        dic_C.update({i.get(phs + 'iri'): i.get(phs + 'label_original')})
    
    terms_C_props = root.findall(".//phs:node_property[@phs:value-type_onto='C']", ns)
    for i in terms_C_props:
        # print(i.get(phs + 'value-iri'), '>', i.get(phs + 'value-label_original'))
        dic_C.update({i.get(phs + 'value-iri'): i.get(phs + 'value-label_original')})

    for iri in dic_C:
        make_Class(onto, iri=iri, label=dic_C[iri])

    # - get OP
    terms_OP = root.findall(".//phs:edge[@phs:type_onto='OP']", ns)
    dic_OP = {}
    for i in terms_OP:
        dic_OP.update({i.get(phs + 'iri'): i.get(phs + 'label_original')})

    for iri in dic_OP:
        make_ObjectProperty(onto, iri=iri, label=dic_OP[iri])

    # - get DP
    terms_DP = root.findall(".//phs:edge[@phs:type_onto='DP']", ns)
    dic_DP = {}
    for i in terms_DP:
        dic_DP.update({i.get(phs + 'iri'): i.get(phs + 'label_original')})

    for iri in dic_DP:
        # print(iri, dic_DP[iri])
        make_DataProperty(onto, iri=iri, label=dic_DP[iri])
    # - get AP
    terms_AP = root.findall(".//phs:edge[@phs:type_onto='AP']", ns)
    dic_AP = {}
    for i in terms_AP:
        dic_AP.update({i.get(phs + 'iri'): i.get(phs + 'label_original')})

    for iri in dic_AP:
        # print(iri, dic_AP[iri])
        make_AnnotationProperty(onto, iri=iri, label=dic_AP[iri])


# given a list of xml nodes, select unique ones based on attribute attr
def xmlUniqueNodes(nodesXML, attr):
    # attr=phs + 'node_id'
    childID = []
    unique_childrenXML = []
    for child in nodesXML:
        i = child.get(attr)
        if i not in childID:
            childID.append(i)
            unique_childrenXML.append(child)
    return unique_childrenXML

# convert PhenoScript numeric node to porper numbers
def phsNumbersToOWL(str_value, type):
    if(type=='real'):
        out=float(str_value)
    elif(type=='int'):
        out=int(str_value)
    else:
        warnings.warn('Unknown numeric type, see: phsNumbersToOWL()')
    return out

# check is a string is URI
def is_valid_uri(uri_string):
    try:
        parsed_uri = urlparse(uri_string)
        return all([parsed_uri.scheme, parsed_uri.netloc])
    except ValueError:
        return False

#--------------------- Declare new datatype for ontology: xsd:anyURI
class anyURI(str):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __add__(self, other):
        if isinstance(other, str):
            return str(self.value) + other
        else:
            raise TypeError("Unsupported operand type")

def anyURI_parser(s):
    return anyURI(s)

def anyURI_unparser(x):
    return x.value


declare_datatype(anyURI, "http://www.w3.org/2001/XMLSchema#anyURI", anyURI_parser, anyURI_unparser)
#---------------------