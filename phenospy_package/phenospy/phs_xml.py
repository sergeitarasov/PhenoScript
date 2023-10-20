# -----------------------------------------------------------
# classes and functions to convert pyparsing output into xml
#
# (C) 2023 Sergei Tarasov
# email sergei.tarasov@helsinki.fi
# -----------------------------------------------------------
import xml.dom.minidom as xmldom
from datetime import datetime
from sys import exit

from phenospy.phs_parser_fun import *
from phenospy.phs_various_fun import *
from phenospy.snips_fun import *

# ------ This is the wrapper to make xml output nice

# former: def phenoscriptParse(phs_string, base_iri):
def phenoscriptToXML(phs_string):
    print(f"{Fore.BLUE}Converting Phenoscript to XML ...{Style.RESET_ALL}")
    # IRI for node: https://urn:uuid:4831b6e2-c326-11ed-a65d-acde48001122/_b3cbc5_12-5
    # IRI for nested node: https://urn:uuid:1312852a-c328-11ed-949a-acde48001122/_ecd5db_14_N3-3"
    # IRI for list node: https://urn:uuid:826c3694-c32a-11ed-96cb-acde48001122/_f34012_15-L3-1
    # For not personalized nodes: https://<base_iri>/<nid>-<self.coord_node>
    # For personalized nodes:     https://<base_iri>/node_dict['id_props']
    #   where node_dict['id_props'] is the tag, N:tag

    # -----------------------------------------
    # Make base iri. This function returns it
    # -----------------------------------------
    # https://urn:uuid:2348c8b6-c31c-11ed-876a-acde48001122
    # base_iri = 'https://' + 'urn:uuid:' + str(uuid.uuid1())
     # https://2348c8b6-c31c-11ed-876a-acde48001122
    base_iri = 'https://' +  str(uuid.uuid1())

    # identifier for to keep track on ophu statement and node coordinates
    global nid # _b3cbc5_N
    base_iri_labels = '_' + uuid_n(6) + '_'  # _b3cbc5_
    nid = nodeIdGenerator(prefix=base_iri_labels, starting_id=1)

    # Global var for keeping track on negative edges
    global varGlobalfromNegativeEdge
    varGlobalfromNegativeEdge = GlobalfromNegativeEdge()

    # IRIs for individuals: "https://urn:uuid:4831b6e2-c326-11ed-a65d-acde48001122/_b3cbc5_12-5"
    global phs_indv_iri
    phs_indv_iri = base_iri + '/'

    nn = '<Phenoscript xmlns:phs="https://github.com/sergeitarasov/PhenoScript">\n' + \
         makeNodes(phs_string[0], pos=1) + '</Phenoscript> '

    xml = xmldom.parseString(nn)
    xml_pretty_str = xml.toprettyxml(indent="\t", newl="\n", encoding=None)
    xx = "\n".join([ll.rstrip() for ll in xml_pretty_str.splitlines() if ll.strip()])
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    return xx, base_iri


# varGlobalfromNegativeEdge=GlobalfromNegativeEdge()
# varGlobalfromNegativeEdge.updatefromNegativeEdge(True)
class GlobalfromNegativeEdge:
    def __init__(self):
        self.value = 'NA'

    def updatefromNegativeEdge(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


# ---------

class phsNode:
    def __init__(self, node_dict, triple_pos='NA', ophu_id='', coord_node='NA', fromNegativeEdge=False):
        self.node_name = node_dict['node_name']
        self.triple_pos = triple_pos  # can be 1,2,3
        # self.node_numeric = False
        self.coord_node = coord_node
        # fromNegativeEdge implies wther the edge that connects to this node has negative prop. assertion
        # this neded for presence/absence reasoning
        self.fromNegativeEdge = fromNegativeEdge

        # node props N[]
        if 'node_props' in node_dict:
            self.props_list = node_dict['node_props']
            self.props_list.insert(0, ['node_name', self.node_name])
        else:
            self.props_list = [['node_name', self.node_name]]

        # id_props is N:xxx, this personalization tag
        if 'id_props' in node_dict:
            self.node_id = phs_indv_iri + node_dict['id_props']
        else:
            # self.node_id = phsIndvIRI + node_id
            self.node_id = phs_indv_iri + str(ophu_id) + '-' + str(self.coord_node)

    def updateNodeID(self, value):
        self.node_id = value

    def nodePropsToXML(self):
        props_collection = []
        # i=1
        for i in range(0, len(self.props_list)):
            coll = '<phs:node_property phs:value="%s">%s</phs:node_property>\n' % (
                str(self.props_list[i][1]), self.props_list[i][0])
            props_collection.append(coll)
        props_collection = ''.join(props_collection)
        # add node name prop
        # props_collection='<phs:node_property phs:value="'+ self.node_name + '">name</phs:node_property>\n' + props_collection
        return props_collection

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        props_xml = self.nodePropsToXML()
        return '<phs:node phs:node_id="%s" phs:triple_pos="%s" phs:node_name="%s" phs:fromNegativeEdge="%s">\n%s</phs:node>\n' % (
            self.node_id, self.triple_pos, self.node_name, self.fromNegativeEdge, props_xml)

    def __repr__(self):
        return 'node_name:%s  node_id:%s' % (self.node_name, self.node_id)


# ------------
class phsNumericNode:
    def __init__(self, node_dict, triple_pos='NA'):
        self.node_name = node_dict['node_name']
        self.triple_pos = triple_pos  # can be 1,2,3

        # node props N[]
        if 'node_props' in node_dict:
            self.props_list = node_dict['node_props']
            self.props_list.insert(0, ['node_name', self.node_name])
        else:
            self.props_list = [['node_name', self.node_name]]

        # numeric node types e.g., 3.2 or 3
        if 'num_real' in node_dict:
            self.props_list.append(['numeric_type', 'real'])
            self.numeric_type = 'real'

        if 'num_int' in node_dict:
            self.props_list.append(['numeric_type', 'int'])
            self.numeric_type = 'int'

    def nodePropsToXML(self):
        props_collection = []
        # i=1
        for i in range(0, len(self.props_list)):
            coll = '<phs:node_property phs:value="%s">%s</phs:node_property>\n' % (
                str(self.props_list[i][1]), self.props_list[i][0])
            props_collection.append(coll)
        props_collection = ''.join(props_collection)
        return props_collection

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        props_xml = self.nodePropsToXML()
        return '<phs:numeric_node phs:triple_pos="%s" phs:node_name="%s" phs:numeric_type="%s">\n%s</phs:numeric_node>\n' % (
            self.triple_pos, self.node_name, self.numeric_type, props_xml)
        # return  '<phs:node phs:node_id="%s" phs:triple_pos="%s" phs:node_name="%s" phs:node_numeric="%s">\n%s</phs:node>\n' % (self.node_id, self.triple_pos, self.node_name, self.node_numeric, props_xml)

    def __repr__(self):
        return 'node_name:%s  node_id:%s' % (self.node_name, self.node_id)

# --------

# Quoted Node
class phsQuotedNode:
    def __init__(self, node_dict, triple_pos='NA'):
        self.node_name = node_dict['node_name']
        self.node_name = eval(self.node_name)  # removing double quotes
        self.triple_pos = triple_pos  # should be only 3
        if (self.triple_pos != 3):
            print(f"{Fore.RED}Error: a quoted node should be at triple position 3.{Style.RESET_ALL}")
            print(f"{Fore.RED}\tsome quoted node is at:{Style.RESET_ALL}", self.triple_pos)
            exit()

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        return '<phs:quoted_node phs:triple_pos="%s" phs:node_name="%s" />\n' % \
            (self.triple_pos, self.node_name)

    def __repr__(self):
        return 'node_name:%s  node_id:%s' % (self.node_name, self.node_id)


# ------
class phsEdge:
    def __init__(self, node_dict, triple_pos='NA'):
        self.node_name = node_dict['edge_name']
        self.triple_pos = triple_pos  # can be 1,2,3
        if 'negative_prop' in node_dict:
            self.negative_prop = 'True'
        else:
            self.negative_prop = 'False'

    def updateNegProp(self, value):
        self.negative_prop = value

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        # return '<phs:edge phs:triple_pos="%s" phs:negative_prop="%s">%s</phs:edge>\n' % (self.triple_pos, self.negative_prop, self.node_name)
        return '<phs:edge phs:triple_pos="%s" phs:negative_prop="%s" phs:edge_name="%s" />\n' % (
            self.triple_pos, self.negative_prop, self.node_name)

    def __repr__(self):
        return 'edge_name:%s' % (self.node_name)


# ----------------
class phsListNode:
    def __init__(self, node_dict, triple_pos='NA'):
        self.node_name = node_dict['node_name']
        self.triple_pos = triple_pos  # can be 1,2,3

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        return '<phs:list_node phs:triple_pos="%s"> %s </phs:list_node>\n' % (self.triple_pos, self.node_name)

    def __repr__(self):
        return 'node_name:%s' % (self.node_name)


# --------------
class phsNestedNode:
    def __init__(self, node_dict, triple_pos='NA'):
        self.node_name = 'node_nested'
        self.triple_pos = triple_pos  # can be 1,2,3

    def updateTriplePos(self, value):
        self.triple_pos = value

    def strXML(self):
        return '<phs:node_nested phs:triple_pos="%s"> %s </phs:node_nested>\n' % (self.triple_pos, self.node_name)

    def __repr__(self):
        return 'node_name:%s  node_id:%s' % (self.node_name, self.node_id)


# ------------- This functon parses pyparser ourput into xml

# makeNodes(phs_string[0], pos=1)
# print(phs_string[0][0][1][0])
# node=phs_string[0][0][1][0]
# node=node[0]
# node=node[5]
# makeNodes(node, pos=1)
# makeNodes(phs_string[0][0][1][0], pos=1)
# type(node_dict)
# node=phs_string[0][0][0][0][0]
# node=out[1][0][1][0]
# edge_xml=phsEdge(out[0][0][0][0][0][3])
# edge_xml.negative_prop

def makeNodes(node, pos, ophu_id='NA', coord='NA'):
    positional_dict = {'1': 1, '3': 2, '5': 3}

    if (node._ParseResults__name == 'edge' and isinstance(node, ParseResults)):
        # This is an edge
        node_dict = node.asDict()
        # node_xml=phsEdge(node_dict,  triple_pos=2)
        edge_xml = phsEdge(node_dict, triple_pos=2)
        # print(edge_xml.negative_prop)
        varGlobalfromNegativeEdge.updatefromNegativeEdge(edge_xml.negative_prop)
        return edge_xml.strXML()

    elif (node._ParseResults__name == 'node' and isinstance(node, ParseResults)):
        # This is a node that can be normal or numeric
        node_dict = node.asDict()

        # this is a numeric node for data properties
        if ('num_real' in node_dict) | ('num_int' in node_dict):
            node_xml = phsNumericNode(node_dict, triple_pos=pos)

        # this is quoted node
        elif ('node_quoted' in node_dict):
            node_xml = phsQuotedNode(node_dict, triple_pos=pos)

        # this is normal node
        else:
            # node_xml=phsNode(node_dict,  triple_pos=pos, node_id=nid.makeId())
            node_xml = phsNode(node_dict, triple_pos=pos, ophu_id=ophu_id, coord_node=coord,
                               fromNegativeEdge=varGlobalfromNegativeEdge)
        return node_xml.strXML()

    elif (node._ParseResults__name == 'node_nested' and isinstance(node, ParseResults)):
        # This is a nested node
        out_colection = []
        # i=0
        for i in range(0, len(node)):
            # coordimnates for nodes (e.g., _ophu_6_N5_5) within nested_node consist of: id_ophu_statement / N / coords of the nested node within ophu_statement (coord) / 
            # / coords of node within nested node (assigned by phsNode).
            nested_coord = ophu_id + '_N' + str(coord)
            # print('nested_coord ' + str(nested_coord))
            out_colection.append(makeNodes(node[i], pos='NO', ophu_id=nested_coord))
        out_colection = ''.join(out_colection)
        # '<phs:node_nested phs:triple_pos="%s"> %s </phs:node_nested>\n' % (self.triple_pos, self.node_name)
        out_colection = '<phs:nested_node phs:triple_pos="%s">\n%s</phs:nested_node>\n' % (str(pos), out_colection)
        return out_colection

    elif (node._ParseResults__name == 'list_node' and isinstance(node, ParseResults)):
        # This is a list node
        out_colection = []
        # i=0
        for i in range(0, len(node)):
            # coordimnates for nodes (e.g., _ophu_4_L9_2) within lis_node consist of: id_ophu_statement / L / coords of the list node within ophu_statement (coord) / 
            # coords of the node within the listed node
            # list_coord=str(coord)+'L'+str(i+1)
            list_coord = 'L' + str(coord) + '-' + str(i + 1)
            out_colection.append(makeNodes(node[i], pos='NO', ophu_id=ophu_id, coord=list_coord))
        out_colection = ''.join(out_colection)
        out_colection = '<phs:list_node phs:triple_pos="%s">\n%s</phs:list_node>\n' % (str(pos), out_colection)
        return out_colection

    elif (isinstance(node, TripleNode) and isinstance(node, ParseResults)):
        # This is a triple (N E N)
        out_colection = []
        varGlobalfromNegativeEdge.updatefromNegativeEdge(False)
        # i=5
        for i in [1, 3, 5]:
            # out_colection.append(makeNodes(node[i], pos=positional_dict[str(i)] ))
            # node[i-1]['coord']
            out_colection.append(
                makeNodes(node[i], pos=positional_dict[str(i)], ophu_id=ophu_id, coord=node[i - 1]['coord']))
        out_colection = ''.join(out_colection)
        out_colection = '<phs:triple_node>\n%s</phs:triple_node>\n' % (out_colection)
        return out_colection

    elif (not bool(node._ParseResults__name) and not isinstance(node, TripleNode) and isinstance(node, ParseResults)):
        # This is the collection of triples
        out_colection = []
        # i=1
        for i in range(0, len(node)):
            # print(i)
            out_colection.append(makeNodes(node[i], pos='NO', ophu_id=ophu_id))
        out_colection = ''.join(out_colection)
        return out_colection

    elif (not isinstance(node, TripleNode) and isinstance(node, ParseResults)):
        # This is any other node
        out_colection = []
        # out_colection= node[0]
        xml_element = str(node._ParseResults__name)

        # ----
        ophu_stat_id = ''
        # each ophu_statement gets an id to use for naming individuals
        if (xml_element == "ophu_statement"):
            ophu_stat_id = nid.makeId()
            # print(ophu_stat_id)
        # ----
        # i=0
        # node=node[0]
        for i in range(0, len(node)):
            out_colection.append(makeNodes(node[i], pos='NO', ophu_id=ophu_stat_id))

        out_colection = ''.join(out_colection)
        out_colection = '<phs:' + xml_element + '>\n' + out_colection + '</phs:' + xml_element + '>\n'
        # out_colection='<phs:‰s>\n%s</phs:‰s>\n' % (xml_element, out_colection, xml_element)
        return out_colection

    else:
        print("makeNodes(): INVALID INPUT")
