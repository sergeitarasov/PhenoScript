## ---------------------------
##
## Phenoscript Parser
##
## 
##
## Author: Sergei Tarasov
##
## Date Created: 2021-08-23
##
## Sergei Tarasov, 2021
## Email: sergei.tarasov@helsinki.fi
##
## ---------------------------
##
## Notes:
##   
##
## ---------------------------


from pyparsing import *
from pyparsing import pyparsing_common as ppc
#from phs_xml import * 
#from pydoc import *


# Get odd mubers in range
def oddNum(start, end):
    xx=[]
    for num in range(start, end + 1):
    # checking condition
        if num % 2 != 0: # if odd: num % 2 != 0:
            #print(num, end = " ")
            xx.append(num)
    return xx

oddNum.__doc__ = """
Create odd numbers in a range
     - odd nums
"""

# Get even mubers in range
def evenNum(start, end):
    xx=[]
    for num in range(start, end + 1):
    # checking condition
        if num % 2 == 0: # if odd: num % 2 != 0:
            #print(num, end = " ")
            xx.append(num)
    return xx

# Group ophu elements into triplets and mark them with position
# groupTriplet(tokens=['n1', 'e1', 'n2@h1', 'e2', 'n3', 'e3', 'n4'])
# make a class for triples to recognize in the pyparser output

class TripleNode(ParseResults):
    pass

# class TripleNode(ParseResults):
#   def __init__(self, parse_res):
#     self.parse_res = parse_res
# 
# #TripleNode('sd')
# class TripleNode(ParseResults):
#     def __init__(self, parse_res):
#       self.parse_res = parse_res


# def groupTriplet(tokens):
#     out=[]
#     # we work with even nums since enumeration in python starts with 0
#     even_start=evenNum(0, len(tokens))
#     even_end=evenNum(0, len(tokens))
#     del even_start[-1]
#     del even_end[0]
#     # i=0
#     for i in range(0, len(even_start)):
#         triple=tokens[even_start[i]:(even_end[i]+1)]
#         #triple=['pos=1',triple[0], 'pos=2', triple[1], 'pos=3', triple[2] ]
#         triple=[{'pos': 1},triple[0], {'pos': 2}, triple[1], {'pos': 3}, triple[2] ]
#         triple=TripleNode(triple)
#         #type(triple)
#         out.append(triple)
#         #out.extend(triple)
#     return out

def groupTriplet(tokens):
    out=[]
    # we work with even nums since enumeration in python starts with 0
    even_start=evenNum(0, len(tokens))
    even_end=evenNum(0, len(tokens))
    del even_start[-1]
    del even_end[0]
    #print(even_start)
    #print(even_end)
    # i=0
    #print(tokens)
    for i in range(0, len(even_start)):
        triple=tokens[even_start[i]:(even_end[i]+1)]
        
        #---- check for errors. triple should be N E N. if not report an error
        #print('triple: ', triple[0]._ParseResults__name, triple[1]._ParseResults__name, triple[2]._ParseResults__name)
        #triple_entities=['node', 'edge', 'node']
        triple_entities=[triple[0]._ParseResults__name, triple[1]._ParseResults__name, triple[2]._ParseResults__name]
        trpl0=(triple_entities[0] not in {'node', 'node_nested', 'list_node'})
        trpl1=(triple_entities[1] not in {'edge'})
        trpl2=(triple_entities[2] not in {'node', 'node_nested', 'list_node'})
        
        #if (triple[0]._ParseResults__name!='node' or triple[1]._ParseResults__name!='edge' or triple[2]._ParseResults__name!='node'  ):
        if (trpl0 or trpl1 or trpl2):
            #print('ERROR')
            return('ERROR')
        #---
        
        #triple=['pos=1',triple[0], 'pos=2', triple[1], 'pos=3', triple[2] ]
        triple=[{'pos': 1, 'coord':even_start[i]+1},triple[0], {'pos': 2, 'coord':even_start[i]+2}, triple[1], {'pos': 3, 'coord':even_start[i]+3}, triple[2] ]
        triple=TripleNode(triple)
        #type(triple)
        out.append(triple)
        #out.extend(triple)
    return out



#------ Parse Actions
# class Item:
#     def __init__(self, value):
#         self.value = value
# 
#     def __repr__(self):
#         return "{Item: %s}" % self.value
# 
# def transform(string, location, tokens):
#     return [Item(token) for token in tokens]

def transform4(string, location, tokens):
    out=groupTriplet(tokens)
    if (out=='ERROR'):
        print('ERROR: the triplet syntax is not Node Edge Node, see line:', txt[1:location].count('\n')+1, ' (location:', location , ')')
        exit('Syntax ERROR found')
    return out


def make_keyword(kwd_str, kwd_value):
    return Keyword(kwd_str).setParseAction(replaceWith(kwd_value))

# count read OTU objects
# var_countOTU=nodeIdGenerator(prefix='', starting_id=1)

#string='sdcc \n dsdc \n dsd \n'
#location=7
def countOTUobjects(string, location, tokens):
    #print('Reading:', string[location:(location+30)], '\n')
    #substr = string[location:len(string)]
    ednOfLine=string[location:len(string)].find('\n')
    ednOfLine=ednOfLine+location
    print('- Reading', var_countOTU.makeId(), ':', string[location:ednOfLine], flush=True)
    return tokens

# def make_edge_keyword(kwd_str):
#     maps={'>':'has_part', '>>':'bearer_of'}
#     #maps['>']
#     return Keyword(kwd_str).setParseAction(replaceWith(maps[kwd_str]))

#------ Parse Actions



#------ Parser
LPARAN, RPARAN, LBRACK, RBRACK, LBRACE, RBRACE, COLON, EQAL = map(Suppress, "()[]{}:=")

TRUE = make_keyword("true", True)
FALSE = make_keyword("false", False)
NULL = make_keyword("null", None)

ed5=make_keyword("|>|", 'increased_in_magnitude_relative_to')
ed6=make_keyword("|<|", 'decreased_in_magnitude_relative_to')
ed7=make_keyword("|=|", 'has_count')

ed1=make_keyword(">", 'has_part')
#ed3=make_keyword("<", 'part_of')
ed3=make_keyword("<", 'part_of[iri="BFO_0000050"]')
#ed2=make_keyword('>>', 'bearer_of')
ed2=make_keyword('>>', 'has_characteristic')
ed4=make_keyword('<<', 'inheres_in')


#graph_word = Word(alphanums +"_", alphanums+"_")
#jsonNumber = ppc.number()
phsInt=ppc.integer()('num_int')
phsReal=ppc.real()('num_real')

graph_alphanum = Word(alphanums + "_" + "-")
#graph_alphanum = Word(alphanums +"_", alphanums+"_")

graph_word=(phsReal | phsInt | graph_alphanum)

#----------- Node
# Node Properties: N[]
propertyWord=Word(alphanums + "_" + ":") # in []
#jsonString = quotedString().setParseAction(removeQuotes)
jsonStr = quotedString().setParseAction(removeQuotes)
jsonString = (jsonStr|propertyWord)

jsonNumber = ppc.number()
#jsonElements = delimitedList(jsonValue)
#jsonArray = Group( LBRACK + pp.Optional(jsonElements) + RBRACK)

jsonValue = (jsonString | jsonNumber | TRUE | FALSE | NULL)
memberDef = Group(jsonString + EQAL + jsonValue)#("jsonMember")
props=Group(LBRACK + delimitedList(memberDef, delim=', ', combine=False) + RBRACK)("node_props") 

#props=Group(LBRACK + graph_word  + RBRACK)("node_props")
#prop_element=graph_word + Literal('=') + graph_word
#props=Group(LPARAN + delimitedList(graph_word, delim=', ', combine=False) + RPARAN)("node_props") 

# node id N@
#ID_props=Suppress('@')+graph_alphanum('id_props')
ID_props=Suppress(':')+graph_alphanum('id_props')

# Node
#node=Group(graph_word("node_name") + Optional(ID_props) + Optional(props) + NotAny('.') )("node")
node=Group(NotAny('.') + graph_word("node_name") + Optional(ID_props) + Optional(props))("node")
#----------- Node

# Edge
neg_prop=Literal('!')("negative_prop")
#edge = Group(Optional(neg_prop) + graph_word("edge_name") + Suppress('.'))("edge")
#------ NEW
#edge_word = Group(Optional(neg_prop) + graph_word("edge_name") + Suppress('.'))("edge")
edge_word = Group(Optional(neg_prop) + Suppress('.') + graph_word("edge_name"))("edge")
edge_vals=(ed5 |ed6 |ed7 | ed2 | ed1 | ed4 | ed3)("edge_name")
edge_sign=Group(Optional(neg_prop) + edge_vals)("edge")
edge=(edge_word | edge_sign)
#-----

# Nested _node Ln=(N E N E N)
nested_node1 = LPARAN + OneOrMore(node | edge) + RPARAN
nested_node1.setParseAction(transform4)
nested_node = Group(nested_node1)("node_nested")

# List_node Ln=(N, N, N)
list_node= Group(LPARAN + delimitedList(node, delim=', ', combine=False) + RPARAN)("list_node") # if combine=True <node>ventral_region, s1, s2</node>


grammar=OneOrMore(edge | node | nested_node| list_node)
grammar.setParseAction(transform4)

#----- Comment out
# query = "n0['id1'=1, 'id2'='val2'] e0. n5"
# 
# query = "n0@h1 e0. n5"
# query = "n0 has_part. n5;"
# query = "n0 > n5;"
# 
# query = "n1 e1. n2 e2. (n3 e4. n5);"
# query = "n1@1 e2 n3 e4. n5 e6. (n7 e8. n8)"
# out=grammar.parseString(query)
# print(out)
# 
# out[0][3].asDict()
# x=out[0][0]
# len(out[0])
# x['coord']
# grammar1
# makeNodes(node,  pos='NO')
# 
# nested_node1.parseString(query)
# print(out)
# nn=makeNodes(out, pos=1)
# print(nn)
# ([([{'pos': 1}, (['n0'], {'node_name': ['n0']}), {'pos': 2}, (['has_part'], {'edge_name': ['has_part']}), {'pos': 3}, (['n5'], {'node_name': ['n5']})], {})], {})
# ([([{'pos': 1}, (['n0'], {'node_name': ['n0']}), {'pos': 2}, (['has_part'], {'edge_name': ['has_part']}), {'pos': 3}, (['n5'], {'node_name': ['n5']})], {})], {})
# query = ">"
# edge.parseString(query)
# 
# graph_word.parseString(query)
# jsonNumber.parseString(query)
# node.parseString(query)

# #-----

# LPARAN, RPARAN, LBRACK, RBRACK, LBRACE, RBRACE, COLON, EQAL = map(Suppress, "()[]{}:=")
# list of ophu's and spp statements
ophu_stat=Group(grammar + Suppress(";"))("ophu_statement")
ophu_list = Group(Suppress(Literal('OPHU_LIST'))+ EQAL + LBRACE + OneOrMore(ophu_stat)+ RBRACE)("ophu_list")
otu_list = Group(Suppress(Literal('OTU_DATA'))+ EQAL + LBRACE + OneOrMore(ophu_stat)+ RBRACE)("otu_properties")
otu_object=Group(Suppress(Literal('OTU'))+ EQAL + LBRACE + otu_list + ophu_list + RBRACE)("otu_object")

otu_object.setParseAction(countOTUobjects)

grammar1=Group(OneOrMore(otu_object))("otu_objects_list")

# comments are denoted by #
pyComment = pythonStyleComment
grammar1.ignore(pyComment)


