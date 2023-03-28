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

# -----------------------------------------
# Keywords/Aliases
# 1. Aliases (keywords) are translated into _xxx_ alias during parsing
# to avoid broken tokens in xml
# 2. Aliases should be defined in JSON snippets
# see package-data/snippets-default.json
# -----------------------------------------

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

# -----------------------------------------

# graph_word = Word(alphanums +"_", alphanums+"_")
# jsonNumber = ppc.number()
phsInt = ppc.integer()('num_int')
phsReal = ppc.real()('num_real')

graph_alphanum = Word(alphanums + "_" + "-")

graph_word = (phsReal | phsInt | graph_alphanum)

# -----------------------------------------
# Node
# -----------------------------------------
# Node Properties: N[]
propertyWord = Word(alphanums + "_" + ":")  # in []
jsonStr = quotedString().setParseAction(removeQuotes)
jsonString = (jsonStr | propertyWord)


jsonNumber = ppc.number()

jsonValue = (jsonString | jsonNumber | TRUE | FALSE | NULL)
memberDef = Group(jsonString + EQAL + jsonValue)  # ("jsonMember")
props = Group(LBRACK + delimitedList(memberDef, delim=', ', combine=False) + RBRACK)("node_props")

# node id N:
ID_props = Suppress(':') + graph_alphanum('id_props')

# Node
# node=Group(graph_word("node_name") + Optional(ID_props) + Optional(props) + NotAny('.') )("node")
node = Group(NotAny('.') + graph_word("node_name") + Optional(ID_props) + Optional(props))("node")

# -----------------------------------------
# Edge
# -----------------------------------------
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

# -----------------------------------------
# Nested node (N E N E N)
# -----------------------------------------
nested_node1 = LPARAN + OneOrMore(node | edge) + RPARAN
nested_node1.setParseAction(transform4)
nested_node = Group(nested_node1)("node_nested")

# -----------------------------------------
# List_node (N, N, N)
# -----------------------------------------
list_node = Group(LPARAN + delimitedList(node, delim=', ', combine=False) + RPARAN)(
    "list_node")  # if combine=True <node>ventral_region, s1, s2</node>

grammar = OneOrMore(edge | node | nested_node | list_node)
grammar.setParseAction(transform4)

# -----------------------------------------
# OTU statements
# -----------------------------------------
ophu_stat = Group(grammar + Suppress(";"))("ophu_statement")
ophu_list = Group(Suppress(Literal('OPHU_LIST')) + EQAL + LBRACE + OneOrMore(ophu_stat) + RBRACE)("ophu_list")
otu_list = Group(Suppress(Literal('OTU_DATA')) + EQAL + LBRACE + OneOrMore(ophu_stat) + RBRACE)("otu_properties")
otu_object = Group(Suppress(Literal('OTU')) + EQAL + LBRACE + otu_list + ophu_list + RBRACE)("otu_object")

otu_object.setParseAction(countOTUobjects)

grammar1 = Group(OneOrMore(otu_object))("otu_objects_list")

# comments are denoted by #
pyComment = pythonStyleComment
grammar1.ignore(pyComment)
