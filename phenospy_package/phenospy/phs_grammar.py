# -----------------------------------------------------------
# Phenoscript Grammar
#
# (C) 2023 Sergei Tarasov
# email sergei.tarasov@helsinki.fi
# -----------------------------------------------------------
from pyparsing import *
from pyparsing import pyparsing_common as ppc
from phs_parser_fun import *


LPARAN, RPARAN, LBRACK, RBRACK, LBRACE, RBRACE, COLON, EQAL = map(Suppress, "()[]{}:=")

TRUE = make_keyword("true", True)
FALSE = make_keyword("false", False)
NULL = make_keyword("null", None)

# ed5=make_keyword("|>|", 'increased_in_magnitude_relative_to')
# ed6=make_keyword("|<|", 'decreased_in_magnitude_relative_to')
# ed7=make_keyword("|=|", 'has_count')

# ed1=make_keyword(">", 'has_part')
# ed3=make_keyword("<", 'part_of[iri="BFO_0000050"]')
# #ed2=make_keyword('>>', 'bearer_of')
# ed2=make_keyword('>>', 'has_characteristic')
# ed4=make_keyword('<<', 'inheres_in')

ed5 = make_keyword("|>|", '_vgv_')
ed6 = make_keyword("|<|", '_vlv_')
ed7 = make_keyword("|=|", '_vev_')

# new keywords
ed8 = make_keyword("->", '_hg_')
ed9 = make_keyword("<-", '_gh_')

ed1 = make_keyword(">", '_g_')
ed3 = make_keyword("<", '_l_')
ed2 = make_keyword('>>', '_gg_')
ed4 = make_keyword('<<', '_ll_')

# graph_word = Word(alphanums +"_", alphanums+"_")
# jsonNumber = ppc.number()
phsInt = ppc.integer()('num_int')
phsReal = ppc.real()('num_real')

graph_alphanum = Word(alphanums + "_" + "-")
# graph_alphanum = Word(alphanums +"_", alphanums+"_")

graph_word = (phsReal | phsInt | graph_alphanum)

# ----------- Node
# Node Properties: N[]
propertyWord = Word(alphanums + "_" + ":")  # in []
# jsonString = quotedString().setParseAction(removeQuotes)
jsonStr = quotedString().setParseAction(removeQuotes)
jsonString = (jsonStr | propertyWord)

jsonNumber = ppc.number()
# jsonElements = delimitedList(jsonValue)
# jsonArray = Group( LBRACK + pp.Optional(jsonElements) + RBRACK)

jsonValue = (jsonString | jsonNumber | TRUE | FALSE | NULL)
memberDef = Group(jsonString + EQAL + jsonValue)  # ("jsonMember")
props = Group(LBRACK + delimitedList(memberDef, delim=', ', combine=False) + RBRACK)("node_props")

# props=Group(LBRACK + graph_word  + RBRACK)("node_props")
# prop_element=graph_word + Literal('=') + graph_word
# props=Group(LPARAN + delimitedList(graph_word, delim=', ', combine=False) + RPARAN)("node_props")

# node id N@
# ID_props=Suppress('@')+graph_alphanum('id_props')
ID_props = Suppress(':') + graph_alphanum('id_props')

# Node
# node=Group(graph_word("node_name") + Optional(ID_props) + Optional(props) + NotAny('.') )("node")
node = Group(NotAny('.') + graph_word("node_name") + Optional(ID_props) + Optional(props))("node")
# ----------- Node

# Edge
neg_prop = Literal('!')("negative_prop")
# edge = Group(Optional(neg_prop) + graph_word("edge_name") + Suppress('.'))("edge")
# ------ NEW
# edge_word = Group(Optional(neg_prop) + graph_word("edge_name") + Suppress('.'))("edge")
edge_word = Group(Optional(neg_prop) + Suppress('.') + graph_word("edge_name"))("edge")
# edge_vals=(ed5 |ed6 |ed7 | ed2 | ed1 | ed4 | ed3)("edge_name")
edge_vals = (ed8 | ed9 | ed5 | ed6 | ed7 | ed2 | ed1 | ed4 | ed3)("edge_name")
edge_sign = Group(Optional(neg_prop) + edge_vals)("edge")
edge = (edge_word | edge_sign)
# -----

# Nested _node Ln=(N E N E N)
nested_node1 = LPARAN + OneOrMore(node | edge) + RPARAN
nested_node1.setParseAction(transform4)
nested_node = Group(nested_node1)("node_nested")

# List_node Ln=(N, N, N)
list_node = Group(LPARAN + delimitedList(node, delim=', ', combine=False) + RPARAN)(
    "list_node")  # if combine=True <node>ventral_region, s1, s2</node>

grammar = OneOrMore(edge | node | nested_node | list_node)
grammar.setParseAction(transform4)

# ----- Comment out
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
ophu_stat = Group(grammar + Suppress(";"))("ophu_statement")
ophu_list = Group(Suppress(Literal('OPHU_LIST')) + EQAL + LBRACE + OneOrMore(ophu_stat) + RBRACE)("ophu_list")
otu_list = Group(Suppress(Literal('OTU_DATA')) + EQAL + LBRACE + OneOrMore(ophu_stat) + RBRACE)("otu_properties")
otu_object = Group(Suppress(Literal('OTU')) + EQAL + LBRACE + otu_list + ophu_list + RBRACE)("otu_object")

otu_object.setParseAction(countOTUobjects)

grammar1 = Group(OneOrMore(otu_object))("otu_objects_list")

# comments are denoted by #
pyComment = pythonStyleComment
grammar1.ignore(pyComment)
