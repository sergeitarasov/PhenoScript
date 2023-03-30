# -----------------------------------------------------------
# Core Phenoscript phs Parser
#
# (C) 2023 Sergei Tarasov
# email sergei.tarasov@helsinki.fi
# -----------------------------------------------------------
from phenospy.phs_various_fun import *
from pyparsing import *
from pyparsing import pyparsing_common as ppc


# Get odd mubers in range
def oddNum(start, end):
    xx = []
    for num in range(start, end + 1):
        # checking condition
        if num % 2 != 0:  # if odd: num % 2 != 0:
            # print(num, end = " ")
            xx.append(num)
    return xx


oddNum.__doc__ = """
Create odd numbers in a range
     - odd nums
"""


# Get even numbers in range
def evenNum(start, end):
    xx = []
    for num in range(start, end + 1):
        # checking condition
        if num % 2 == 0:  # if odd: num % 2 != 0:
            # print(num, end = " ")
            xx.append(num)
    return xx


# Group ophu elements into triplets and mark them with position
# groupTriplet(tokens=['n1', 'e1', 'n2@h1', 'e2', 'n3', 'e3', 'n4'])
# make a class for triples to recognize in the pyparser output

class TripleNode(ParseResults):
    pass

def groupTriplet(tokens):
    out = []
    # we work with even nums since enumeration in python starts with 0
    even_start = evenNum(0, len(tokens))
    even_end = evenNum(0, len(tokens))
    del even_start[-1]
    del even_end[0]
    # print(even_start)
    # print(even_end)
    # i=0
    # print(tokens)
    for i in range(0, len(even_start)):
        triple = tokens[even_start[i]:(even_end[i] + 1)]

        # ---- check for errors. triple should be N E N. if not report an error
        # print('triple: ', triple[0]._ParseResults__name, triple[1]._ParseResults__name, triple[2]._ParseResults__name)
        # triple_entities=['node', 'edge', 'node']
        triple_entities = [triple[0]._ParseResults__name, triple[1]._ParseResults__name, triple[2]._ParseResults__name]
        trpl0 = (triple_entities[0] not in {'node', 'node_nested', 'list_node'})
        trpl1 = (triple_entities[1] not in {'edge'})
        trpl2 = (triple_entities[2] not in {'node', 'node_nested', 'list_node'})

        # if (triple[0]._ParseResults__name!='node' or triple[1]._ParseResults__name!='edge' or triple[2]._ParseResults__name!='node'  ):
        if (trpl0 or trpl1 or trpl2):
            # print('ERROR')
            return ('ERROR')
        # ---

        # triple=['pos=1',triple[0], 'pos=2', triple[1], 'pos=3', triple[2] ]
        triple = [{'pos': 1, 'coord': even_start[i] + 1}, triple[0], {'pos': 2, 'coord': even_start[i] + 2}, triple[1],
                  {'pos': 3, 'coord': even_start[i] + 3}, triple[2]]
        triple = TripleNode(triple)
        # type(triple)
        out.append(triple)
        # out.extend(triple)
    return out


def transform4(string, location, tokens):
    out = groupTriplet(tokens)
    if (out == 'ERROR'):
        print('ERROR: the triplet syntax is not Node Edge Node, see line:', txt[1:location].count('\n') + 1,
              ' (location:', location, ')')
        exit('Syntax ERROR found')
    return out


def make_keyword(kwd_str, kwd_value):
    return Keyword(kwd_str).setParseAction(replaceWith(kwd_value))


# count read OTU objects
# var_countOTU=nodeIdGenerator(prefix='', starting_id=1)

global var_countOTU
var_countOTU = nodeIdGenerator(prefix='', starting_id=1)

# string='sdcc \n dsdc \n dsd \n'
# location=7
def countOTUobjects(string, location, tokens):
    # print('Reading:', string[location:(location+30)], '\n')
    # substr = string[location:len(string)]
    ednOfLine = string[location:len(string)].find('\n')
    ednOfLine = ednOfLine + location
    # print('- Reading', var_countOTU.makeId(), ':', string[location:ednOfLine], flush=True)
    print(f"{Fore.GREEN}- Reading OTU",  var_countOTU.makeId(), ':', f"{Style.RESET_ALL}", string[location:ednOfLine])
    return tokens


